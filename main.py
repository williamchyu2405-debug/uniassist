import os
import json
import sqlite3
import hashlib
import secrets
from collections import defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional
import anthropic
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Request, Header, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pdfplumber
from pptx import Presentation
import base64

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Bulletproof .env loader — handles broken/old dotenv packages
def _load_env_file():
    import pathlib
    env_path = pathlib.Path(__file__).parent / ".env"
    if not env_path.exists():
        return
    try:
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                if line.startswith('.') or line.startswith('/'):
                    continue  # Skip lines like './start.sh'
                k, _, v = line.partition('=')
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass

_load_env_file()


def _normalize_topic(topic: str) -> str:
    """Shorten verbose AI-generated topics to 2-3 word broad categories.
    E.g. 'Acidity and pKa of Carboxylic Acids' → 'Carboxylic Acids'"""
    if not topic or len(topic) <= 25:
        return topic  # already short
    # Common patterns: "X of Y" → keep Y; "X and Y of Z" → keep Z
    # Strategy: take the last noun phrase (after last 'of'/'in'/'for') or first 2-3 words
    for sep in [' of ', ' in ', ' for ', ' during ']:
        if sep in topic:
            tail = topic.split(sep)[-1].strip()
            if len(tail) <= 30:
                return tail
    # Fallback: first 3 words
    words = topic.split()
    # Drop leading filler words
    fillers = {'the', 'a', 'an', 'and', 'or'}
    cleaned = [w for w in words if w.lower() not in fillers]
    return ' '.join(cleaned[:3])


# Optional passcode that must be entered before the app loads.
# Set ACCESS_CODE=yourcode in .env — anyone opening the URL must enter it first.
ACCESS_CODE = os.getenv("ACCESS_CODE", "").strip()

app = FastAPI(title="MedVault")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


from fastapi.responses import JSONResponse

@app.middleware("http")
async def access_guard(request: Request, call_next):
    """Block all API routes unless the correct access code is provided.
    Accepts the code as either the X-Access-Code header (app) or the
    ?ac= query param (bookmarklet — keeps the request 'simple' so no CORS preflight is needed)."""
    if not ACCESS_CODE:
        return await call_next(request)
    path  = request.url.path
    method = request.method
    # Always pass through: HTML root, static assets, CORS preflight, and the info endpoint itself
    if (path == "/" or path == "/bookmarklet" or path.startswith("/static") or path.startswith("/images")
            or method == "OPTIONS" or path == "/api/access-check"):
        return await call_next(request)
    provided = (request.headers.get("X-Access-Code", "")
                or request.query_params.get("ac", ""))
    if provided != ACCESS_CODE:
        return JSONResponse({"detail": "access_code_required"}, status_code=403)
    return await call_next(request)


@app.get("/api/access-check")
def access_check_get():
    """Tells the client whether an access code is required (no auth needed to call this)."""
    return {"required": bool(ACCESS_CODE)}


@app.post("/api/access-check")
async def access_check_post(request: Request):
    """Validate an access code. This endpoint is exempt from the middleware,
    so we check the code manually here."""
    if not ACCESS_CODE:
        return {"ok": True}
    provided = (request.headers.get("X-Access-Code", "")
                or request.query_params.get("ac", ""))
    if provided != ACCESS_CODE:
        return JSONResponse({"detail": "Incorrect access code"}, status_code=403)
    return {"ok": True}

MODEL = "claude-sonnet-4-6"
HAIKU = "claude-haiku-4-5-20251001"
GEN_CONTENT_CHARS = 24000   # ~6k tokens; fits a full multi-slide module clip (cached, so cheap on repeat generators)

# ── Storage paths — override with env vars for cloud deployment ───────────────
# Locally (no DATA_DIR):  data/study.db, uploads/, static/material_images/
# Railway (DATA_DIR=/data): /data/data/study.db, /data/uploads/, /data/material_images/
_DATA_DIR_ENV = os.getenv("DATA_DIR", "").strip()
if _DATA_DIR_ENV:
    _DATA_ROOT = Path(_DATA_DIR_ENV)
    IMAGES_DIR = _DATA_ROOT / "material_images"   # served via /images/ route
else:
    _DATA_ROOT = Path(".")
    IMAGES_DIR = Path("static/material_images")   # served by StaticFiles + /images/ route

DB_PATH    = str(_DATA_ROOT / "data" / "study.db")
UPLOAD_DIR = _DATA_ROOT / "uploads"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)
(_DATA_ROOT / "data").mkdir(parents=True, exist_ok=True)
Path("static").mkdir(exist_ok=True)


def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY not set in .env file")
    return anthropic.Anthropic(api_key=api_key)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ── Password hashing (stdlib PBKDF2 — no extra dependencies) ────────────────

def hash_password(password: str) -> str:
    """Hash a password with a random salt. Returns 'salt$hash' hex string."""
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    return salt + "$" + h.hex()

def verify_password(password: str, stored: str) -> bool:
    """Verify a password against a 'salt$hash' string."""
    if not stored or "$" not in stored:
        return False
    salt, _, expected = stored.partition("$")
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 260000)
    return secrets.compare_digest(h.hex(), expected)


def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS user_materials (
            user_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, material_id)
        );
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            visibility TEXT DEFAULT 'private',
            filename TEXT NOT NULL,
            original_name TEXT NOT NULL,
            subject TEXT DEFAULT 'Medicine',
            content TEXT,
            file_type TEXT,
            images TEXT DEFAULT '[]',
            uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            user_id INTEGER,
            topic TEXT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            times_seen INTEGER DEFAULT 0,
            times_correct INTEGER DEFAULT 0,
            last_seen DATETIME,
            next_review TEXT DEFAULT NULL,
            srs_interval INTEGER DEFAULT 1,
            ease_factor REAL DEFAULT 2.5,
            review_count INTEGER DEFAULT 0,
            FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS flashcard_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flashcard_id INTEGER,
            material_id INTEGER,
            user_id INTEGER,
            topic TEXT,
            correct INTEGER DEFAULT 0,
            reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            user_id INTEGER,
            topic TEXT,
            question TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            difficulty TEXT DEFAULT 'medium',
            FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            material_id INTEGER,
            user_id INTEGER,
            topic TEXT,
            user_answer TEXT,
            is_correct INTEGER,
            attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS revision_slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            user_id INTEGER,
            title TEXT,
            content TEXT,
            slide_order INTEGER DEFAULT 0,
            FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS exam_dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            exam_date DATE,
            notes TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS mind_maps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            material_id INTEGER,
            user_id INTEGER,
            title TEXT,
            data TEXT,
            FOREIGN KEY (material_id) REFERENCES materials(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_id TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    # ── Backward-compat migrations for existing databases ─────────────────
    # (These are no-ops on new databases where CREATE TABLE already includes these columns)
    for stmt in [
        "ALTER TABLE materials ADD COLUMN images TEXT DEFAULT '[]'",
        "ALTER TABLE quiz_questions ADD COLUMN difficulty TEXT DEFAULT 'medium'",
        "ALTER TABLE flashcards ADD COLUMN next_review TEXT DEFAULT NULL",
        "ALTER TABLE flashcards ADD COLUMN srs_interval INTEGER DEFAULT 1",
        "ALTER TABLE flashcards ADD COLUMN ease_factor REAL DEFAULT 2.5",
        "ALTER TABLE flashcards ADD COLUMN review_count INTEGER DEFAULT 0",
        "ALTER TABLE quiz_attempts ADD COLUMN material_id INTEGER",
        # Multi-user columns
        "ALTER TABLE materials ADD COLUMN user_id INTEGER",
        "ALTER TABLE materials ADD COLUMN visibility TEXT DEFAULT 'private'",
        "ALTER TABLE flashcards ADD COLUMN user_id INTEGER",
        "ALTER TABLE flashcard_log ADD COLUMN user_id INTEGER",
        "ALTER TABLE quiz_questions ADD COLUMN user_id INTEGER",
        "ALTER TABLE quiz_attempts ADD COLUMN user_id INTEGER",
        "ALTER TABLE revision_slides ADD COLUMN user_id INTEGER",
        "ALTER TABLE mind_maps ADD COLUMN user_id INTEGER",
        "ALTER TABLE exam_dates ADD COLUMN user_id INTEGER",
        "ALTER TABLE chat_messages ADD COLUMN user_id INTEGER",
        # Organisation
        "ALTER TABLE materials ADD COLUMN sort_order INTEGER DEFAULT 0",
        # Auth columns
        "ALTER TABLE users ADD COLUMN password_hash TEXT",
        # Auto-linking: related topics on flashcards and quiz questions
        "ALTER TABLE flashcards ADD COLUMN related_topics TEXT DEFAULT '[]'",
        "ALTER TABLE quiz_questions ADD COLUMN related_topics TEXT DEFAULT '[]'",
        # Chemistry: SMILES notation for structure rendering
        "ALTER TABLE flashcards ADD COLUMN smiles TEXT DEFAULT NULL",
        "ALTER TABLE quiz_questions ADD COLUMN smiles TEXT DEFAULT NULL",
    ]:
        try:
            conn.execute(stmt)
            conn.commit()
        except Exception:
            pass  # Column already exists

    # Sessions table for token-based auth
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    # Quiz battles
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quiz_battles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            question_ids TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS battle_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            battle_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            score INTEGER DEFAULT 0,
            total INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            finished_at DATETIME,
            FOREIGN KEY (battle_id) REFERENCES quiz_battles(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(battle_id, user_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS graph_hidden_nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            node_id TEXT NOT NULL,
            hidden_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, node_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS graph_hidden_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            target TEXT NOT NULL,
            hidden_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, source, target)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS graph_custom_edges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source TEXT NOT NULL,
            target TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, source, target)
        )
    """)
    conn.commit()

    # ── Performance indexes (CREATE INDEX IF NOT EXISTS = safe to re-run) ──
    for idx in [
        "CREATE INDEX IF NOT EXISTS idx_flashcards_user    ON flashcards(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_flashcards_review  ON flashcards(user_id, next_review)",
        "CREATE INDEX IF NOT EXISTS idx_fc_log_user        ON flashcard_log(user_id, reviewed_at)",
        "CREATE INDEX IF NOT EXISTS idx_quiz_attempts_user ON quiz_attempts(user_id, attempted_at)",
        "CREATE INDEX IF NOT EXISTS idx_materials_user     ON materials(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_user_materials     ON user_materials(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_slides_material    ON revision_slides(material_id, user_id)",
        "CREATE INDEX IF NOT EXISTS idx_mm_material        ON mind_maps(material_id, user_id)",
    ]:
        conn.execute(idx)
    conn.commit()

    # ── One-time topic cleanup: normalize verbose AI-generated topic names ─────
    long_topics = conn.execute("SELECT DISTINCT topic FROM quiz_attempts WHERE LENGTH(topic) > 25").fetchall()
    for row in long_topics:
        old = row[0]
        new = _normalize_topic(old)
        if new != old:
            conn.execute("UPDATE quiz_attempts SET topic = ? WHERE topic = ?", (new, old))
            conn.execute("UPDATE quiz_questions SET topic = ? WHERE topic = ?", (new, old))
    if long_topics:
        conn.commit()

    # Also fix flashcard_log topics
    long_fc = conn.execute("SELECT DISTINCT topic FROM flashcard_log WHERE topic IS NOT NULL AND LENGTH(topic) > 25").fetchall()
    for row in long_fc:
        old = row[0]
        new = _normalize_topic(old)
        if new != old:
            conn.execute("UPDATE flashcard_log SET topic = ? WHERE topic = ?", (new, old))
    if long_fc:
        conn.commit()

    # ── One-time backfill: claim pre-multi-user data for a default profile ─────
    # If data exists but no profiles do yet, create a "Me" profile and assign all
    # existing materials/cards/quizzes/etc. to it so nothing is lost on upgrade.
    user_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    material_count = conn.execute("SELECT COUNT(*) FROM materials").fetchone()[0]
    if user_count == 0 and material_count > 0:
        conn.execute("INSERT INTO users (username) VALUES ('Me')")
        uid = conn.execute("SELECT id FROM users WHERE username = 'Me'").fetchone()[0]
        for tbl in ["materials", "flashcards", "flashcard_log", "quiz_questions",
                    "quiz_attempts", "revision_slides", "mind_maps", "exam_dates", "chat_messages"]:
            conn.execute(f"UPDATE {tbl} SET user_id = ? WHERE user_id IS NULL", (uid,))
        for r in conn.execute("SELECT id FROM materials").fetchall():
            conn.execute("INSERT OR IGNORE INTO user_materials (user_id, material_id) VALUES (?,?)", (uid, r[0]))
        conn.commit()

    conn.close()


init_db()


# ── Text extraction ──────────────────────────────────────────────────────────

def extract_pdf(path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n\n"
    except Exception as e:
        text = f"[PDF extraction error: {e}]"
    return text.strip()


def extract_pptx(path: str) -> str:
    text = ""
    try:
        prs = Presentation(path)
        for i, slide in enumerate(prs.slides, 1):
            text += f"--- Slide {i} ---\n"
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text += shape.text.strip() + "\n"
            if slide.has_notes_slide:
                notes = slide.notes_slide.notes_text_frame.text.strip()
                if notes:
                    text += f"[Notes: {notes}]\n"
            text += "\n"
    except Exception as e:
        text = f"[PPTX extraction error: {e}]"
    return text.strip()


def extract_image(path: str) -> str:
    try:
        client = get_client()
        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")
        ext = Path(path).suffix.lower()
        mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}.get(ext, "image/jpeg")
        msg = client.messages.create(
            model=HAIKU, max_tokens=2000,  # Haiku has vision — far cheaper than Sonnet for transcription
            messages=[{"role": "user", "content": [
                {"type": "image", "source": {"type": "base64", "media_type": mime, "data": data}},
                {"type": "text", "text": "Transcribe and describe all text, diagrams, tables, and key information from this medical/health study image in full detail."}
            ]}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"[Image extraction error: {e}]"


def extract_pdf_images(path: str, mat_id: int) -> list:
    """Extract embedded images from a PDF and save to IMAGES_DIR."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    urls = []
    try:
        with pdfplumber.open(path) as pdf:
            idx = 0
            for page in pdf.pages[:20]:
                for img_meta in (page.images or [])[:2]:
                    try:
                        x0 = float(img_meta.get('x0', 0))
                        top = float(img_meta.get('top', 0))
                        x1 = float(img_meta.get('x1', page.width))
                        bottom = float(img_meta.get('bottom', page.height))
                        if (x1 - x0) < 80 or (bottom - top) < 80:
                            continue
                        cropped = page.crop((x0, top, x1, bottom))
                        fname = f"mat{mat_id}_{idx}.png"
                        cropped.to_image(resolution=120).save(str(IMAGES_DIR / fname))
                        urls.append(f"/images/{fname}")
                        idx += 1
                        if idx >= 8:
                            return urls
                    except Exception:
                        continue
    except Exception:
        pass
    return urls


def extract_pptx_images(path: str, mat_id: int) -> list:
    """Extract embedded pictures from a PPTX and save to IMAGES_DIR."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    urls = []
    try:
        prs = Presentation(path)
        idx = 0
        for slide in prs.slides:
            for shape in slide.shapes:
                try:
                    if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                        image = shape.image
                        ext = (image.ext or 'png').lower()
                        if ext not in ('png', 'jpg', 'jpeg'):
                            ext = 'png'
                        fname = f"mat{mat_id}_{idx}.{ext}"
                        (IMAGES_DIR / fname).write_bytes(image.blob)
                        urls.append(f"/images/{fname}")
                        idx += 1
                        if idx >= 10:
                            return urls
                except Exception:
                    continue
    except Exception:
        pass
    return urls


def _salvage_json_array(text: str):
    """Recover the complete objects from a JSON array that was cut off mid-way
    (e.g. the model hit max_tokens, leaving a truncated trailing object).
    Returns a list of the objects that DID parse, or None if nothing usable."""
    start = text.find("[")
    if start == -1:
        return None
    objs, depth, obj_start = [], 0, None
    in_str = esc = False
    for i in range(start + 1, len(text)):
        ch = text[i]
        if in_str:
            if esc:            esc = False
            elif ch == "\\":   esc = True
            elif ch == '"':    in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                obj_start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and obj_start is not None:
                try:
                    objs.append(json.loads(text[obj_start:i + 1]))
                except json.JSONDecodeError:
                    pass
                obj_start = None
    return objs or None


def parse_json_response(text: str):
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # The model may have been truncated at max_tokens, leaving invalid JSON.
        # Salvage every complete object so we keep the questions that DID arrive
        # instead of discarding the whole batch.
        salvaged = _salvage_json_array(text)
        if salvaged:
            return salvaged
        raise


# ── Efficient generation (prompt caching) ──────────────────────────────────────

def gen_source_block(mat) -> str:
    """Identical source-material text for every generator on a given material.
    Sent as the first content block and cache-tagged, so generating slides then
    flashcards/quiz/mindmap on the same material within ~5 min reuses the cache."""
    return (
        "SOURCE STUDY MATERIAL\n"
        f"Title: {mat['original_name']}\n"
        f"Subject: {mat['subject']}\n\n"
        f"{(mat['content'] or '')[:GEN_CONTENT_CHARS]}"
    )


def generate_json(mat, instructions: str, model: str = HAIKU, max_tokens: int = 4000) -> str:
    """One-shot generation. The (large, reusable) source material is the first block and
    is marked for prompt caching; the (small, varying) task instructions follow it.
    Repeat calls on the same material hit the cache and cost ~10% on the cached portion."""
    resp = get_client().messages.create(
        model=model, max_tokens=max_tokens,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": gen_source_block(mat), "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": instructions},
        ]}],
    )
    return resp.content[0].text


# ── Auth / identity (password-based with session tokens) ───────────────────────

SESSION_TTL_DAYS = 30  # sessions last 30 days

def _create_session(db, user_id: int) -> str:
    """Create a new session token for a user, clean up expired sessions."""
    token = secrets.token_hex(32)
    expires = (datetime.utcnow() + timedelta(days=SESSION_TTL_DAYS)).strftime("%Y-%m-%d %H:%M:%S")
    db.execute("INSERT INTO sessions (token, user_id, expires_at) VALUES (?,?,?)", (token, user_id, expires))
    # Prune old sessions while we're here
    db.execute("DELETE FROM sessions WHERE expires_at < ?", (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),))
    db.commit()
    return token

def get_current_user(request: Request) -> int:
    """Resolve the active user from either:
    1. Authorization: Bearer <token>  (new session-token auth)
    2. X-User-Id header               (legacy — kept for bookmarklet/console clipper)
    """
    # Try session token first
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:].strip()
        if token:
            db = get_db()
            row = db.execute(
                "SELECT user_id FROM sessions WHERE token = ? AND expires_at > ?",
                (token, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
            ).fetchone()
            db.close()
            if row:
                return row["user_id"]
            raise HTTPException(401, "Session expired — please log in again")

    # Fallback: legacy X-User-Id header (bookmarklet, old clients)
    x_user_id = request.headers.get("X-User-Id")
    if x_user_id:
        try:
            uid = int(x_user_id)
        except (TypeError, ValueError):
            raise HTTPException(401, "Invalid profile")
        db = get_db()
        row = db.execute("SELECT id FROM users WHERE id = ?", (uid,)).fetchone()
        db.close()
        if not row:
            raise HTTPException(401, "Profile not found")
        return uid

    raise HTTPException(401, "Not logged in")


def user_can_access(db, mid: int, user_id: int) -> bool:
    """True if the material is owned by the user, in their library, or public."""
    row = db.execute("SELECT user_id, visibility FROM materials WHERE id = ?", (mid,)).fetchone()
    if not row:
        return False
    if row["user_id"] == user_id or row["visibility"] == "public":
        return True
    lib = db.execute(
        "SELECT 1 FROM user_materials WHERE user_id = ? AND material_id = ?", (user_id, mid)
    ).fetchone()
    return lib is not None


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.get("/bookmarklet")
def bookmarklet_page():
    return FileResponse("static/bookmarklet.html")



@app.get("/api/profiles")
def list_profiles():
    """Public list of profiles (names + avatars only). No passwords exposed."""
    db = get_db()
    rows = db.execute("SELECT id, username, created_at FROM users ORDER BY created_at").fetchall()
    db.close()
    return [{"id": r["id"], "username": r["username"], "has_password": True} for r in rows]


@app.post("/api/register")
async def register(request: Request):
    """Create a new account with username + password. Returns a session token."""
    body = await request.json()
    username = (body.get("username") or "").strip()[:40]
    password = body.get("password", "")
    if not username:
        raise HTTPException(400, "Username required")
    if len(password) < 4:
        raise HTTPException(400, "Password must be at least 4 characters")
    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        db.close()
        raise HTTPException(409, "That name is taken — pick another")
    pw_hash = hash_password(password)
    cur = db.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, pw_hash))
    uid = cur.lastrowid
    db.commit()
    token = _create_session(db, uid)
    db.close()
    return {"id": uid, "username": username, "token": token}


@app.post("/api/login")
async def login(request: Request):
    """Log in with username + password. Returns a session token."""
    body = await request.json()
    username = (body.get("username") or "").strip()
    password = body.get("password", "")
    if not username or not password:
        raise HTTPException(400, "Username and password required")
    db = get_db()
    row = db.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username,)).fetchone()
    if not row:
        db.close()
        raise HTTPException(401, "Wrong username or password")
    # Legacy profile with no password — let them set one
    if not row["password_hash"]:
        pw_hash = hash_password(password)
        db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (pw_hash, row["id"]))
        db.commit()
        token = _create_session(db, row["id"])
        db.close()
        return {"id": row["id"], "username": row["username"], "token": token, "password_set": True}
    if not verify_password(password, row["password_hash"]):
        db.close()
        raise HTTPException(401, "Wrong username or password")
    token = _create_session(db, row["id"])
    db.close()
    return {"id": row["id"], "username": row["username"], "token": token}


@app.post("/api/logout")
async def logout(request: Request):
    """Invalidate the current session token."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:].strip()
        if token:
            db = get_db()
            db.execute("DELETE FROM sessions WHERE token = ?", (token,))
            db.commit()
            db.close()
    return {"ok": True}


@app.post("/api/profiles")
async def create_profile_legacy(request: Request):
    """Legacy endpoint — creates profile with a default password for old clients."""
    body = await request.json()
    username = (body.get("username") or "").strip()[:40]
    password = body.get("password") or "1234"
    if not username:
        raise HTTPException(400, "Username required")
    if len(password) < 4:
        password = "1234"
    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    if existing:
        db.close()
        raise HTTPException(409, "That name is taken — pick another")
    pw_hash = hash_password(password)
    cur = db.execute("INSERT INTO users (username, password_hash) VALUES (?,?)", (username, pw_hash))
    uid = cur.lastrowid
    db.commit()
    token = _create_session(db, uid)
    db.close()
    return {"id": uid, "username": username, "token": token}


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), subject: str = Form(default="Medicine"),
                      user_id: int = Depends(get_current_user)):
    ext = Path(file.filename).suffix.lower()
    allowed = {".pdf", ".pptx", ".ppt", ".png", ".jpg", ".jpeg", ".webp"}
    if ext not in allowed:
        raise HTTPException(400, f"Unsupported file type: {ext}")

    safe = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    path = UPLOAD_DIR / safe
    content = await file.read()
    path.write_bytes(content)

    if ext == ".pdf":
        text, ftype = extract_pdf(str(path)), "pdf"
    elif ext in {".pptx", ".ppt"}:
        text, ftype = extract_pptx(str(path)), "pptx"
    else:
        text, ftype = extract_image(str(path)), "image"

    if len(text) < 50:
        text = "[Minimal text — AI will process the content directly]"

    db = get_db()
    cur = db.execute(
        "INSERT INTO materials (user_id, filename, original_name, subject, content, file_type, images) VALUES (?,?,?,?,?,?,?)",
        (user_id, safe, file.filename, subject, text, ftype, '[]')
    )
    mid = cur.lastrowid
    db.execute("INSERT OR IGNORE INTO user_materials (user_id, material_id) VALUES (?,?)", (user_id, mid))
    db.commit()

    # Extract images now that we have the material ID
    image_urls: list = []
    if ext == ".pdf":
        image_urls = extract_pdf_images(str(path), mid)
    elif ext in {".pptx", ".ppt"}:
        image_urls = extract_pptx_images(str(path), mid)
    else:
        # Direct image upload — copy to IMAGES_DIR so it's URL-accessible
        img_fname = f"mat{mid}_0{ext}"
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        (IMAGES_DIR / img_fname).write_bytes(content)
        image_urls = [f"/images/{img_fname}"]

    if image_urls:
        db.execute("UPDATE materials SET images = ? WHERE id = ?", (json.dumps(image_urls), mid))
        db.commit()

    db.close()
    return {"id": mid, "name": file.filename, "subject": subject, "type": ftype,
            "chars": len(text), "images": len(image_urls)}


@app.get("/api/materials")
def list_materials(user_id: int = Depends(get_current_user)):
    """Materials in the current profile's library — their own uploads plus public
    materials they've added from other people."""
    db = get_db()
    rows = db.execute(
        """SELECT m.id, m.original_name, m.subject, m.file_type, m.uploaded_at,
                  LENGTH(m.content) as chars, m.images, m.visibility,
                  COALESCE(m.sort_order, 0) as sort_order,
                  m.user_id as owner_id, u.username as owner_name
           FROM materials m
           JOIN user_materials um ON um.material_id = m.id
           LEFT JOIN users u ON u.id = m.user_id
           WHERE um.user_id = ?
           ORDER BY COALESCE(m.sort_order, 0) ASC, m.uploaded_at DESC""",
        (user_id,)
    ).fetchall()
    db.close()
    result = []
    for r in rows:
        d = dict(r)
        d['is_owner'] = (d.get('owner_id') == user_id)
        try:
            d['images'] = json.loads(d.get('images') or '[]')
        except Exception:
            d['images'] = []
        result.append(d)
    return result


@app.get("/api/discover")
def discover_materials(user_id: int = Depends(get_current_user)):
    """Public materials shared by other profiles that aren't already in my library."""
    db = get_db()
    rows = db.execute(
        """SELECT m.id, m.original_name, m.subject, m.file_type, m.uploaded_at,
                  LENGTH(m.content) as chars, u.username as owner_name
           FROM materials m
           LEFT JOIN users u ON u.id = m.user_id
           WHERE m.visibility = 'public' AND m.user_id != ?
             AND m.id NOT IN (SELECT material_id FROM user_materials WHERE user_id = ?)
           ORDER BY m.uploaded_at DESC""",
        (user_id, user_id)
    ).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.post("/api/materials/{mid}/visibility")
async def set_visibility(mid: int, request: Request, user_id: int = Depends(get_current_user)):
    body = await request.json()
    vis = body.get("visibility")
    if vis not in ("public", "private"):
        raise HTTPException(400, "visibility must be 'public' or 'private'")
    db = get_db()
    mat = db.execute("SELECT user_id FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        db.close()
        raise HTTPException(404, "Material not found")
    if mat["user_id"] != user_id:
        db.close()
        raise HTTPException(403, "Only the owner can change visibility")
    db.execute("UPDATE materials SET visibility = ? WHERE id = ?", (vis, mid))
    db.commit()
    db.close()
    return {"ok": True, "visibility": vis}


@app.post("/api/materials/{mid}/add")
def add_material(mid: int, user_id: int = Depends(get_current_user)):
    """Add a public material to my library and COPY the owner's generated content
    (slides, flashcards, quiz, mind map) as my own starting point — SRS reset, no AI used."""
    db = get_db()
    mat = db.execute("SELECT user_id, visibility FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        db.close()
        raise HTTPException(404, "Material not found")
    if mat["user_id"] == user_id:
        db.close()
        raise HTTPException(400, "That's already your material")
    if mat["visibility"] != "public":
        db.close()
        raise HTTPException(403, "This material isn't shared")

    already = db.execute(
        "SELECT 1 FROM user_materials WHERE user_id = ? AND material_id = ?", (user_id, mid)
    ).fetchone()
    if already:
        db.close()
        return {"ok": True, "already": True}

    owner = mat["user_id"]
    db.execute("INSERT OR IGNORE INTO user_materials (user_id, material_id) VALUES (?,?)", (user_id, mid))

    # Copy the owner's slides
    for r in db.execute(
        "SELECT title, content, slide_order FROM revision_slides WHERE material_id = ? AND user_id = ? ORDER BY slide_order",
        (mid, owner)
    ).fetchall():
        db.execute(
            "INSERT INTO revision_slides (material_id, user_id, title, content, slide_order) VALUES (?,?,?,?,?)",
            (mid, user_id, r["title"], r["content"], r["slide_order"])
        )

    # Copy the owner's flashcards — reset SRS so the borrower starts fresh
    for r in db.execute(
        "SELECT topic, question, answer FROM flashcards WHERE material_id = ? AND user_id = ?",
        (mid, owner)
    ).fetchall():
        db.execute(
            "INSERT INTO flashcards (material_id, user_id, topic, question, answer) VALUES (?,?,?,?,?)",
            (mid, user_id, r["topic"], r["question"], r["answer"])
        )

    # Copy the owner's quiz questions
    for r in db.execute(
        "SELECT topic, question, options, correct_answer, explanation, difficulty FROM quiz_questions WHERE material_id = ? AND user_id = ?",
        (mid, owner)
    ).fetchall():
        db.execute(
            "INSERT INTO quiz_questions (material_id, user_id, topic, question, options, correct_answer, explanation, difficulty) VALUES (?,?,?,?,?,?,?,?)",
            (mid, user_id, r["topic"], r["question"], r["options"], r["correct_answer"], r["explanation"], r["difficulty"])
        )

    # Copy the owner's mind map
    mm = db.execute(
        "SELECT title, data FROM mind_maps WHERE material_id = ? AND user_id = ?", (mid, owner)
    ).fetchone()
    if mm:
        db.execute(
            "INSERT INTO mind_maps (material_id, user_id, title, data) VALUES (?,?,?,?)",
            (mid, user_id, mm["title"], mm["data"])
        )

    db.commit()
    db.close()
    return {"ok": True}


@app.delete("/api/materials/{mid}")
def delete_material(mid: int, user_id: int = Depends(get_current_user)):
    db = get_db()
    mat = db.execute("SELECT user_id FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        db.close()
        raise HTTPException(404, "Material not found")
    # Remove the current profile's own derived content + their library link
    for tbl in ["flashcard_log", "flashcards", "quiz_questions", "quiz_attempts", "revision_slides", "mind_maps"]:
        db.execute(f"DELETE FROM {tbl} WHERE material_id = ? AND user_id = ?", (mid, user_id))
    db.execute("DELETE FROM user_materials WHERE material_id = ? AND user_id = ?", (mid, user_id))
    # If the owner removes it and nobody else still has it, delete the material itself
    if mat["user_id"] == user_id:
        others = db.execute("SELECT COUNT(*) as c FROM user_materials WHERE material_id = ?", (mid,)).fetchone()["c"]
        if others == 0:
            db.execute("DELETE FROM materials WHERE id = ?", (mid,))
    db.commit()
    db.close()
    return {"ok": True}


@app.patch("/api/materials/{mid}")
async def update_material(mid: int, request: Request, user_id: int = Depends(get_current_user)):
    """Rename a material or change its subject. Owner-only."""
    db = get_db()
    mat = db.execute("SELECT user_id FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        db.close(); raise HTTPException(404, "Material not found")
    if mat["user_id"] != user_id:
        db.close(); raise HTTPException(403, "Only the owner can rename")
    body = await request.json()
    fields, params = [], []
    if "name" in body:
        fields.append("original_name = ?"); params.append(body["name"].strip()[:200])
    if "subject" in body:
        fields.append("subject = ?");        params.append(body["subject"].strip()[:100])
    if not fields:
        db.close(); return {"ok": True}
    params.append(mid)
    db.execute(f"UPDATE materials SET {', '.join(fields)} WHERE id = ?", params)
    db.commit(); db.close()
    return {"ok": True}


@app.post("/api/materials/reorder")
async def reorder_materials(request: Request, user_id: int = Depends(get_current_user)):
    """Save a new sort_order for each material. Body: [{id, sort_order}, ...]"""
    body = await request.json()  # list of {id: int, sort_order: int}
    db = get_db()
    for item in body:
        try:
            mid = int(item["id"]); order = int(item["sort_order"])
        except (KeyError, ValueError, TypeError):
            continue
        # Only update materials the user owns
        db.execute(
            "UPDATE materials SET sort_order = ? WHERE id = ? AND user_id = ?",
            (order, mid, user_id)
        )
    db.commit(); db.close()
    return {"ok": True}


@app.get("/api/materials/{mid}/content")
def get_material_content(mid: int, user_id: int = Depends(get_current_user)):
    """Raw extracted text for a material — pure DB read, NO Claude tokens.
    Used by the 'Copy for Claude' widget to bundle context for the web chat."""
    db = get_db()
    if not user_can_access(db, mid, user_id):
        db.close()
        raise HTTPException(403, "No access to this material")
    mat = db.execute(
        "SELECT original_name, subject, content FROM materials WHERE id = ?", (mid,)
    ).fetchone()
    db.close()
    if not mat:
        raise HTTPException(404, "Material not found")
    return {"name": mat["original_name"], "subject": mat["subject"], "content": mat["content"] or ""}


@app.get("/api/context/export")
def export_context(material_id: Optional[int] = None, user_id: int = Depends(get_current_user)):
    """Bundle a student's study context (material text + weak topics + missed questions +
    stats) so it can be copied into the Claude.ai web chat. Pure DB reads — NO API tokens."""
    db = get_db()
    bundle: dict = {}

    if material_id and user_can_access(db, material_id, user_id):
        mat = db.execute(
            "SELECT original_name, subject, content FROM materials WHERE id = ?", (material_id,)
        ).fetchone()
        if mat:
            bundle["material"] = {
                "name": mat["original_name"], "subject": mat["subject"],
                "content": mat["content"] or "",
            }

    # Overall quiz accuracy
    qs = dict(db.execute("SELECT COUNT(*) as t, SUM(is_correct) as c FROM quiz_attempts WHERE user_id = ?", (user_id,)).fetchone())
    bundle["total_questions"] = qs["t"] or 0
    bundle["accuracy"] = round(((qs["c"] or 0) / max(qs["t"] or 1, 1)) * 100, 1)

    # Weakest topics by accuracy
    bundle["weak_topics"] = [dict(r) for r in db.execute(
        """SELECT topic, COUNT(*) as attempts, SUM(is_correct) as correct,
                  ROUND(CAST(SUM(is_correct) AS REAL)/COUNT(*)*100) as pct
           FROM quiz_attempts WHERE user_id = ? GROUP BY topic ORDER BY pct ASC, attempts DESC LIMIT 8""",
        (user_id,)
    ).fetchall()]

    # Recently missed questions (for targeted help)
    bundle["missed"] = [dict(r) for r in db.execute(
        """SELECT q.question, q.correct_answer, q.explanation, a.topic
           FROM quiz_attempts a JOIN quiz_questions q ON a.question_id = q.id
           WHERE a.is_correct = 0 AND a.user_id = ? ORDER BY a.attempted_at DESC LIMIT 10""",
        (user_id,)
    ).fetchall()]

    # Flashcards due today
    today = date.today().isoformat()
    bundle["due_today"] = db.execute(
        "SELECT COUNT(*) as c FROM flashcards WHERE user_id = ? AND (next_review IS NULL OR next_review <= ?)",
        (user_id, today)
    ).fetchone()["c"]

    db.close()
    return bundle


@app.post("/api/import-web")
async def import_web(request: Request):
    # Sent as text/plain to avoid a CORS preflight from the uni portal page.
    # The bookmarklet includes the active profile id in the payload (no header available cross-origin).
    raw = await request.body()
    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        raise HTTPException(400, "Invalid payload")

    title = (data.get("title") or "Web import").strip()[:200]
    text = (data.get("text") or "").strip()
    subject = (data.get("subject") or "Medicine").strip()
    url = (data.get("url") or "").strip()

    if len(text) < 20:
        raise HTTPException(400, "No usable text found on the page")

    db = get_db()
    # Resolve owner: explicit user_id in payload, else the first profile (single-user fallback)
    uid = data.get("user_id")
    try:
        uid = int(uid) if uid is not None else None
    except (TypeError, ValueError):
        uid = None
    if uid is None or not db.execute("SELECT 1 FROM users WHERE id = ?", (uid,)).fetchone():
        first = db.execute("SELECT id FROM users ORDER BY id LIMIT 1").fetchone()
        uid = first["id"] if first else None
    if uid is None:
        db.close()
        raise HTTPException(400, "No profile exists yet — create one in MedVault first")

    content = f"[Imported from: {url}]\n\n{text}"
    cur = db.execute(
        "INSERT INTO materials (user_id, filename, original_name, subject, content, file_type) VALUES (?,?,?,?,?,?)",
        (uid, f"web_{datetime.now().strftime('%Y%m%d_%H%M%S')}", title, subject, content, "web")
    )
    mid = cur.lastrowid
    db.execute("INSERT OR IGNORE INTO user_materials (user_id, material_id) VALUES (?,?)", (uid, mid))
    db.commit()
    db.close()
    return {"id": mid, "name": title, "chars": len(content)}


@app.post("/api/import-web-form")
async def import_web_form(request: Request):
    """Form-based import — fallback for portals whose CSP blocks fetch/XHR.
    The clipper submits a hidden <form> with the payload in a textarea field.
    Returns an HTML confirmation page (opens in a new tab)."""
    form = await request.form()
    raw = form.get("payload", "")
    try:
        data = json.loads(raw)
    except Exception:
        return HTMLResponse("<h2>Import failed</h2><p>Invalid payload.</p>", status_code=400)

    title = (data.get("title") or "Web import").strip()[:200]
    text = (data.get("text") or "").strip()
    subject = (data.get("subject") or "Medicine").strip()
    url = (data.get("url") or "").strip()

    if len(text) < 20:
        return HTMLResponse("<h2>Import failed</h2><p>No usable text found on the page.</p>", status_code=400)

    db = get_db()
    uid = data.get("user_id")
    try:
        uid = int(uid) if uid is not None else None
    except (TypeError, ValueError):
        uid = None
    if uid is None or not db.execute("SELECT 1 FROM users WHERE id = ?", (uid,)).fetchone():
        first = db.execute("SELECT id FROM users ORDER BY id LIMIT 1").fetchone()
        uid = first["id"] if first else None
    if uid is None:
        db.close()
        return HTMLResponse("<h2>Import failed</h2><p>No profile exists yet.</p>", status_code=400)

    content = f"[Imported from: {url}]\n\n{text}"
    cur = db.execute(
        "INSERT INTO materials (user_id, filename, original_name, subject, content, file_type) VALUES (?,?,?,?,?,?)",
        (uid, f"web_{datetime.now().strftime('%Y%m%d_%H%M%S')}", title, subject, content, "web")
    )
    mid = cur.lastrowid
    db.execute("INSERT OR IGNORE INTO user_materials (user_id, material_id) VALUES (?,?)", (uid, mid))
    db.commit()
    db.close()

    html = f"""<!DOCTYPE html>
<html><head><title>MedVault Import</title>
<style>body{{font-family:system-ui;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;background:#f0fdf4}}
.card{{background:#fff;border-radius:12px;padding:2rem;box-shadow:0 4px 12px rgba(0,0,0,.1);text-align:center;max-width:400px}}
h2{{color:#16a34a;margin:0 0 .5rem}}p{{color:#555;margin:.3rem 0}}.close{{margin-top:1rem;color:#999;font-size:.9rem}}</style></head>
<body><div class="card"><h2>✅ Imported!</h2>
<p><strong>{title}</strong></p>
<p>{len(content):,} characters from {data.get("pages", 1)} slide(s)</p>
<p class="close">You can close this tab and go back to your portal.</p></div></body></html>"""
    return HTMLResponse(html)


# ── Slides ───────────────────────────────────────────────────────────────────

@app.post("/api/generate/slides/{mid}")
def generate_slides(mid: int, force: bool = False, user_id: int = Depends(get_current_user)):
    db = get_db()
    if not user_can_access(db, mid, user_id):
        db.close()
        raise HTTPException(403, "No access to this material")
    mat = db.execute("SELECT * FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        raise HTTPException(404, "Material not found")

    # Memory: reuse existing slides without an AI call unless regeneration is forced
    existing = db.execute("SELECT COUNT(*) as c FROM revision_slides WHERE material_id = ? AND user_id = ?", (mid, user_id)).fetchone()["c"]
    if existing > 0 and not force:
        rows = db.execute(
            "SELECT content FROM revision_slides WHERE material_id = ? AND user_id = ? ORDER BY slide_order", (mid, user_id)
        ).fetchall()
        slides = []
        for r in rows:
            try:
                slides.append(json.loads(r["content"]))
            except Exception:
                pass
        db.close()
        return {"count": existing, "existing": True, "slides": slides}

    # Load any images extracted from this material
    image_urls: list = []
    try:
        image_urls = json.loads(mat['images'] or '[]')
    except Exception:
        pass

    # Build image context block for the prompt
    image_block = ""
    image_note = ""
    if image_urls:
        img_list = "\n".join(f"  {i+1}. {u}" for i, u in enumerate(image_urls))
        image_block = f"\n\nIMAGES EXTRACTED FROM THIS MATERIAL (you may reference these in diagram slides):\n{img_list}\n"
        image_note = (
            '\nFor "diagram" slides: if one of the images above directly illustrates the topic, '
            'add "image_url": "<url>" to the object and set "nodes": [], "connections": []. '
            'The image will be displayed in the diagram panel instead of a generated SVG.'
        )

    instructions = f"""You are a medical education designer creating revision slides.

STRICT RULE: Base EVERY slide exclusively on information explicitly stated in the SOURCE STUDY MATERIAL above. Do NOT introduce assumed knowledge, background context, or facts not present in the source text. If information is not in the source, omit it.
{image_block}
Generate 16-22 slides using these 7 TYPES. Mix types — never use same type more than 3× in a row.

TYPE SCHEMAS (exact field names required):

"overview" — module intro:
{{"type":"overview","topic":"string","title":"string","subtitle":"string","key_themes":["theme1","theme2","theme3","theme4"]}}

"concept" — core definition:
{{"type":"concept","topic":"string","title":"string","definition":"one clear sentence from the material","key_points":["point from material","point from material","point from material"],"icon":"relevant emoji","color":"teal|blue|purple|green|amber|red"}}

"diagram" — spatial or relational structure:{image_note}
{{"type":"diagram","topic":"string","title":"string","diagram_type":"flow|cycle|hierarchy","nodes":[{{"id":"1","label":"short label","description":"brief"}}],"connections":[{{"from":"1","to":"2"}}],"caption":"describe what the diagram shows","clinical_pearl":"string or null"}}

"comparison" — two contrasting concepts:
{{"type":"comparison","topic":"string","title":"string","left":{{"label":"Term A","color":"blue","points":["...","...","..."]}},"right":{{"label":"Term B","color":"red","points":["...","...","..."]}},"key_difference":"one sentence"}}

"process" — step-by-step sequence:
{{"type":"process","topic":"string","title":"string","steps":[{{"number":1,"title":"step name","description":"what happens — from the source"}}],"clinical_pearl":"string or null"}}

"mnemonic" — memory aid:
{{"type":"mnemonic","topic":"string","title":"string","mnemonic":"WORD","expansion":[{{"letter":"W","meaning":"Word — full explanation"}}],"context":"Full explanation of WHAT this topic is and WHY this mnemonic applies — not just 'use this to remember'"}}

"clinical" — real-world application:
{{"type":"clinical","topic":"string","title":"string","scenario":"clinical sentence drawn from the material","question":"question about this scenario","answer":"answer based on the material","teaching_point":"key takeaway from the material"}}

RULES:
- Every fact must be sourced from the content above — no assumed knowledge
- Use comparison for contrasting pairs found in the source
- Use mnemonic only when the source contains or strongly implies a memory aid
- Mnemonic context MUST explain the full topic concept, not just say 'use this to remember'
- Vary concept slide colors
- Return ONLY the JSON array, no markdown, no extra text"""

    text = generate_json(mat, instructions, model=HAIKU, max_tokens=8000)
    try:
        slides = parse_json_response(text)
    except Exception:
        slides = [{"type":"concept","title":"Generation Error","topic":"Error","definition":"Could not generate slides.","key_points":["Please try again"],"icon":"⚠️","color":"red"}]

    db.execute("DELETE FROM revision_slides WHERE material_id = ? AND user_id = ?", (mid, user_id))
    for i, s in enumerate(slides):
        db.execute(
            "INSERT INTO revision_slides (material_id, user_id, title, content, slide_order) VALUES (?,?,?,?,?)",
            (mid, user_id, s.get("title", f"Slide {i+1}"), json.dumps(s), i)
        )
    db.commit()
    db.close()
    return {"count": len(slides), "slides": slides}


@app.get("/api/slides")
def get_slides(material_id: Optional[int] = None, user_id: int = Depends(get_current_user)):
    db = get_db()
    q = "SELECT rs.*, m.original_name FROM revision_slides rs JOIN materials m ON rs.material_id = m.id"
    rows = db.execute(q + " WHERE rs.material_id = ? AND rs.user_id = ? ORDER BY slide_order", (material_id, user_id)).fetchall() \
        if material_id else db.execute(q + " WHERE rs.user_id = ? ORDER BY rs.material_id, slide_order", (user_id,)).fetchall()
    db.close()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["content"] = json.loads(d["content"])
        except Exception:
            pass
        result.append(d)
    return result


# ── Flashcards ───────────────────────────────────────────────────────────────

@app.post("/api/generate/flashcards/{mid}")
def generate_flashcards(mid: int, force: bool = False, user_id: int = Depends(get_current_user)):
    db = get_db()
    if not user_can_access(db, mid, user_id):
        db.close()
        raise HTTPException(403, "No access to this material")
    mat = db.execute("SELECT * FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        raise HTTPException(404, "Material not found")
    # Return existing cards without an AI call unless forced
    existing = db.execute("SELECT COUNT(*) as c FROM flashcards WHERE material_id = ? AND user_id = ?", (mid, user_id)).fetchone()["c"]
    if existing > 0 and not force:
        db.close()
        return {"count": existing, "existing": True}

    # Auto-linking: gather topics from user's OTHER materials for cross-references
    other_topics = db.execute("""
        SELECT DISTINCT q.topic FROM quiz_questions q
        JOIN user_materials um ON um.material_id = q.material_id
        WHERE um.user_id = ? AND q.material_id != ? AND q.topic IS NOT NULL
        LIMIT 20
    """, (user_id, mid)).fetchall()
    related_str = ", ".join(_normalize_topic(r["topic"]) for r in other_topics) if other_topics else ""
    cross_link = ""
    if related_str:
        cross_link = f"""
CROSS-LINKING: The student is also studying these topics: {related_str}.
Where relevant, connect flashcard content to these other topics the student is learning.
For example, reference how a concept applies across subjects, or note clinical/practical links.
Add a "related" field with 1-2 related topic names when there's a genuine connection."""

    # Detect subject to tailor flashcard style
    subject = (mat["subject"] or "").lower()
    content_sample = (mat["content"] or "")[:500].lower()
    is_quantitative = any(kw in subject or kw in content_sample for kw in
        ["chemistry", "chem", "physics", "pharmacology", "biochem", "calcul", "equation", "molar", "reaction"])

    fc_chem_block = ""
    if is_quantitative:
        fc_chem_block = """
QUANTITATIVE CONTENT — include where the material supports it:
- Calculation cards: "Calculate the pH of a 0.1M solution of acetic acid (Ka = 1.8 × 10⁻⁵)"
- When a card involves a specific molecule, include its SMILES notation in a "smiles" field
- Example SMILES: ethanol = "CCO", acetic acid = "CC(=O)O", benzene = "c1ccccc1"
- Only include "smiles" when the structure is directly relevant"""
    else:
        fc_chem_block = """
SUBJECT-APPROPRIATE — match the card style to the subject:
- Anatomy: "Which nerve passes through X?" / clinical correlations / spatial reasoning
- Physiology: mechanism questions, "What happens when X increases?"
- Pathology: "A biopsy shows X. What is the most likely diagnosis?"
- Do NOT include calculations or chemical structures unless the material explicitly covers them"""

    instructions = f"""You are a university-level educator writing CONCISE flashcards for EXAM PREPARATION.

Create flashcards that test UNDERSTANDING and APPLICATION. Good question styles:
- Application: "Why does X cause Y?" or "What happens when..."
- Compare/contrast: "How does X differ from Y?"
- Clinical: 1-sentence vignette → ask for key mechanism or finding
- Problem-solving: brief scenario requiring reasoning
{fc_chem_block}

AVOID simple definition cards like "What is X?" → "X is...". Every card should require THINKING.

⚠️ BREVITY RULE — ANSWERS MUST BE SHORT:
- Maximum 2-3 sentences OR up to 4 bullet points (use • character)
- State the KEY FACT first, then brief mechanism if needed
- NO long paragraphs, NO preamble, NO padding
- Target 25-40 words per answer

Return ONLY a JSON array of 15-20 flashcards:
[{{
  "topic": "Broad topic (2-3 words max, e.g. 'Organic Chemistry', 'Cell Biology', 'Pharmacology')",
  "question": "University exam-style question (1-2 sentences max)",
  "answer": "Short answer — 2-3 sentences or ≤4 bullet points. Key fact + brief mechanism only.",
  "related": ["Related Topic 1"],
  "smiles": "SMILES string ONLY if a chemical structure is relevant, otherwise omit entirely"
}}]

IMPORTANT: The "topic" must be a BROAD subject category (2-3 words), NOT a specific question description.
{cross_link}"""

    text = generate_json(mat, instructions, model=HAIKU, max_tokens=6000)
    try:
        cards = parse_json_response(text)
    except Exception:
        cards = [{"topic": "Error", "question": "Could not generate flashcards", "answer": "Please try again"}]

    db.execute("DELETE FROM flashcards WHERE material_id = ? AND user_id = ?", (mid, user_id))
    for c in cards:
        related = json.dumps(c.get("related", []))
        smiles = c.get("smiles") or None
        db.execute(
            "INSERT INTO flashcards (material_id, user_id, topic, question, answer, related_topics, smiles) VALUES (?,?,?,?,?,?,?)",
            (mid, user_id, c.get("topic", "General"), c.get("question", ""), c.get("answer", ""), related, smiles)
        )
    db.commit()
    db.close()
    return {"count": len(cards)}


@app.get("/api/flashcards")
def get_flashcards(material_id: Optional[int] = None, adaptive: bool = False, due_only: bool = False,
                   user_id: int = Depends(get_current_user)):
    db = get_db()
    today = date.today().isoformat()
    conditions, params = ["f.user_id = ?"], [user_id]
    if material_id:
        conditions.append("f.material_id = ?")
        params.append(material_id)
    if due_only:
        conditions.append("(f.next_review IS NULL OR f.next_review <= ?)")
        params.append(today)
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    if due_only:
        order = "COALESCE(f.next_review, '1970-01-01') ASC"  # most overdue first
    elif adaptive:
        order = "CASE WHEN f.times_seen = 0 THEN 0 ELSE CAST(f.times_correct AS REAL)/f.times_seen END ASC"
    else:
        order = "f.id"
    base = "SELECT f.*, m.original_name FROM flashcards f JOIN materials m ON f.material_id = m.id"
    rows = db.execute(f"{base} {where} ORDER BY {order}", params).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.post("/api/flashcards/{cid}/result")
async def flashcard_result(cid: int, request: Request, user_id: int = Depends(get_current_user)):
    body = await request.json()
    correct = body.get("correct", False)
    db = get_db()
    card = db.execute("SELECT * FROM flashcards WHERE id = ? AND user_id = ?", (cid, user_id)).fetchone()
    if not card:
        db.close()
        raise HTTPException(404, "Card not found")
    # SM-2 spaced repetition algorithm
    ease   = float(card["ease_factor"]  or 2.5)
    interval = int(card["srs_interval"] or 1)
    count  = int(card["review_count"]   or 0)
    quality = 4 if correct else 1  # binary: correct=4, wrong=1
    if quality >= 3:  # correct
        if count == 0:
            new_interval = 1
        elif count == 1:
            new_interval = 6
        else:
            new_interval = max(1, round(interval * ease))
        new_ease  = max(1.3, ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_count = count + 1
    else:  # incorrect — reset streak, small ease penalty
        new_interval = 1
        new_ease     = max(1.3, ease - 0.2)
        new_count    = 0
    next_review = (date.today() + timedelta(days=new_interval)).isoformat()
    db.execute(
        """UPDATE flashcards SET
           times_seen=times_seen+1, times_correct=times_correct+?,
           last_seen=?, srs_interval=?, ease_factor=?, review_count=?, next_review=?
           WHERE id=?""",
        (1 if correct else 0, datetime.now().isoformat(),
         new_interval, round(new_ease, 4), new_count, next_review, cid)
    )
    # Log every review so the dashboard activity chart includes flashcard study
    db.execute(
        "INSERT INTO flashcard_log (flashcard_id, material_id, user_id, topic, correct) VALUES (?,?,?,?,?)",
        (cid, card["material_id"], user_id, card["topic"], 1 if correct else 0)
    )
    db.commit()
    db.close()
    return {"ok": True, "next_review": next_review, "interval_days": new_interval}


@app.get("/api/srs/stats")
def get_srs_stats(user_id: int = Depends(get_current_user)):
    db = get_db()
    today    = date.today().isoformat()
    week_end = (date.today() + timedelta(days=7)).isoformat()
    due      = db.execute("SELECT COUNT(*) as c FROM flashcards WHERE user_id = ? AND (next_review IS NULL OR next_review <= ?)", (user_id, today)).fetchone()["c"]
    new_c    = db.execute("SELECT COUNT(*) as c FROM flashcards WHERE user_id = ? AND review_count = 0", (user_id,)).fetchone()["c"]
    mature   = db.execute("SELECT COUNT(*) as c FROM flashcards WHERE user_id = ? AND srs_interval > 21", (user_id,)).fetchone()["c"]
    # "Coming up" = scheduled strictly after today, within 7 days (not today's cards)
    upcoming = db.execute(
        "SELECT COUNT(*) as c FROM flashcards WHERE user_id = ? AND next_review > ? AND next_review <= ?",
        (user_id, today, week_end)
    ).fetchone()["c"]
    db.close()
    return {"due_today": due, "new_cards": new_c, "mature": mature, "upcoming_week": upcoming}


# ── Quiz ─────────────────────────────────────────────────────────────────────

DIFF_INSTRUCTIONS = {
    'easy': """Generate EASY questions only — direct factual recall.
- Single concept per question; answer is clearly stated in the material
- No multi-step reasoning or clinical vignettes required
- Set "difficulty": "easy" on every question""",
    'medium': """Generate MEDIUM difficulty questions — application and mechanism understanding.
- Require understanding relationships and mechanisms, not just bare recall
- Short clinical scenarios (1–2 sentences) where helpful; two-step reasoning
- Set "difficulty": "medium" on every question""",
    'hard': """Generate HARD questions — complex clinical reasoning, board-exam style.
- Detailed clinical vignettes requiring multi-concept integration
- Student must identify mechanism AND clinical implication together
- Highly plausible distractors; no obvious answer
- Set "difficulty": "hard" on every question""",
    'mixed': """Generate a MIX of difficulties — label every question:
- ~30% easy  ("difficulty":"easy")  — direct recall
- ~40% medium ("difficulty":"medium") — application/mechanism, short vignettes
- ~30% hard  ("difficulty":"hard")  — complex reasoning, detailed scenarios"""
}

@app.post("/api/generate/quiz/{mid}")
def generate_quiz(mid: int, difficulty: str = "mixed", force: bool = False,
                  user_id: int = Depends(get_current_user)):
    db = get_db()
    if not user_can_access(db, mid, user_id):
        db.close()
        raise HTTPException(403, "No access to this material")
    mat = db.execute("SELECT * FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        raise HTTPException(404, "Material not found")

    # Memory: reuse existing questions without an AI call when they match the requested
    # difficulty, unless regeneration is forced.
    if not force:
        diffs = [r["difficulty"] for r in db.execute(
            "SELECT difficulty FROM quiz_questions WHERE material_id = ? AND user_id = ?", (mid, user_id)
        ).fetchall()]
        if diffs:
            uniq = set(d or "medium" for d in diffs)
            matches = (uniq == {difficulty}) if difficulty != "mixed" else (len(uniq) > 1)
            if matches:
                db.close()
                return {"count": len(diffs), "existing": True}

    diff_prompt = DIFF_INSTRUCTIONS.get(difficulty, DIFF_INSTRUCTIONS['mixed'])

    # Auto-linking: gather topics from other materials
    other_topics = db.execute("""
        SELECT DISTINCT q.topic FROM quiz_questions q
        JOIN user_materials um ON um.material_id = q.material_id
        WHERE um.user_id = ? AND q.material_id != ? AND q.topic IS NOT NULL
        LIMIT 20
    """, (user_id, mid)).fetchall()
    related_str = ", ".join(_normalize_topic(r["topic"]) for r in other_topics) if other_topics else ""
    cross_link = ""
    if related_str:
        cross_link = f"""
CROSS-LINKING: The student is also studying: {related_str}.
Where relevant, test how concepts from THIS material connect to those other topics.
Add a "related" field with 1-2 related topic names when there's a genuine connection."""

    # Detect subject to tailor question style
    subject = (mat["subject"] or "").lower()
    content_sample = (mat["content"] or "")[:500].lower()
    is_quantitative = any(kw in subject or kw in content_sample for kw in
        ["chemistry", "chem", "physics", "pharmacology", "biochem", "calcul", "equation", "molar", "reaction"])

    chem_block = ""
    if is_quantitative:
        chem_block = """
QUANTITATIVE CONTENT DETECTED — include these where the material supports it:
- CALCULATION questions: pH, molarity, dilution, reaction yield, equilibrium constants, molar mass, stoichiometry, dosage calculations
- For calculation questions, show values in the stem and have options be specific numerical answers (with units)
- When a question involves a specific molecule, include its SMILES notation in a "smiles" field for structure rendering
- Example SMILES: ethanol = "CCO", acetic acid = "CC(=O)O", benzene = "c1ccccc1"
- Only include "smiles" when the structure is directly relevant to the question"""
    else:
        chem_block = """
SUBJECT-APPROPRIATE QUESTIONS — match the question style to the subject:
- Anatomy: spatial relationships, clinical correlations ("damage to X nerve would cause..."), identify structures by description
- Physiology: mechanisms, feedback loops, "what happens when..."
- Pathology: disease presentations, histological findings, differential diagnosis
- Medicine: clinical vignettes with diagnosis/management decisions
- Do NOT include calculation questions or chemical structures unless the material explicitly covers quantitative content"""

    instructions = f"""You are a UNIVERSITY EXAM question writer. Create questions that match the style and difficulty of real university exams from the SOURCE STUDY MATERIAL above.

QUESTION STYLE — adapt to the subject matter:
- Test APPLICATION and REASONING, not just recall
- Include questions that require INTEGRATING multiple concepts
- Make distractors plausible — they should be common misconceptions or near-correct answers
- Write at the level of a final-year university exam or board exam
{chem_block}

DIFFICULTY INSTRUCTIONS:
{diff_prompt}

Return ONLY a JSON array of 12-15 questions:
[{{
  "topic": "Broad topic (2-3 words max, e.g. 'Organic Chemistry', 'Cell Biology', 'Pharmacology')",
  "difficulty": "easy|medium|hard",
  "question": "University exam-style question appropriate to the subject",
  "options": ["A. Option", "B. Option", "C. Option", "D. Option"],
  "correct_answer": "A",
  "explanation": "Step-by-step reasoning. For calculations, show formula → substitution → answer with units.",
  "related": ["Related Topic"],
  "smiles": "SMILES string ONLY if a chemical structure is relevant, otherwise omit entirely"
}}]

IMPORTANT: The "topic" must be a BROAD subject category (2-3 words), NOT a specific question description.
{cross_link}

Never repeat the same question. Every question must require THINKING, not just memory."""

    text = generate_json(mat, instructions, model=HAIKU, max_tokens=8000)
    try:
        qs = parse_json_response(text)
    except Exception:
        qs = [{"topic": "Error", "difficulty": "medium", "question": "Could not generate quiz", "options": ["A. Error", "B. Error", "C. Error", "D. Error"], "correct_answer": "A", "explanation": "Please try again"}]

    db.execute("DELETE FROM quiz_questions WHERE material_id = ? AND user_id = ?", (mid, user_id))
    for q in qs:
        fallback_diff = difficulty if difficulty != 'mixed' else 'medium'
        related = json.dumps(q.get("related", []))
        smiles = q.get("smiles") or None
        db.execute(
            "INSERT INTO quiz_questions (material_id, user_id, topic, difficulty, question, options, correct_answer, explanation, related_topics, smiles) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (mid, user_id, q.get("topic", "General"), q.get("difficulty", fallback_diff),
             q.get("question", ""), json.dumps(q.get("options", [])),
             q.get("correct_answer", "A"), q.get("explanation", ""), related, smiles)
        )
    db.commit()
    db.close()
    return {"count": len(qs)}


@app.get("/api/quiz")
def get_quiz(material_id: Optional[int] = None, user_id: int = Depends(get_current_user)):
    db = get_db()
    # Get weak topics for adaptive ordering (this user's own attempts)
    weak = [r["topic"] for r in db.execute(
        "SELECT topic FROM quiz_attempts WHERE user_id = ? GROUP BY topic ORDER BY CAST(SUM(is_correct) AS REAL)/COUNT(*) ASC LIMIT 3",
        (user_id,)
    ).fetchall()]

    base = "SELECT q.*, m.original_name FROM quiz_questions q JOIN materials m ON q.material_id = m.id"
    rows = db.execute(base + " WHERE q.material_id = ? AND q.user_id = ?", (material_id, user_id)).fetchall() \
        if material_id else db.execute(base + " WHERE q.user_id = ?", (user_id,)).fetchall()
    db.close()

    result = []
    for r in rows:
        d = dict(r)
        try:
            d["options"] = json.loads(d["options"])
        except Exception:
            d["options"] = []
        result.append(d)

    # Adaptive: weak topics first
    if weak:
        result.sort(key=lambda q: weak.index(q.get("topic", "")) if q.get("topic") in weak else len(weak))
    return result


@app.post("/api/quiz/{qid}/answer")
async def submit_answer(qid: int, request: Request, user_id: int = Depends(get_current_user)):
    body = await request.json()
    answer = body.get("answer", "").strip()
    db = get_db()
    q = db.execute("SELECT * FROM quiz_questions WHERE id = ? AND user_id = ?", (qid, user_id)).fetchone()
    if not q:
        raise HTTPException(404, "Question not found")
    correct = answer and answer[0].upper() == q["correct_answer"].strip()[0].upper()
    db.execute(
        "INSERT INTO quiz_attempts (question_id, material_id, user_id, topic, user_answer, is_correct) VALUES (?,?,?,?,?,?)",
        (qid, q["material_id"], user_id, q["topic"], answer, 1 if correct else 0)
    )
    db.commit()
    db.close()
    return {"correct": correct, "correct_answer": q["correct_answer"], "explanation": q["explanation"]}


# ── Leaderboard & Quiz Battles ────────────────────────────────────────────────

@app.get("/api/leaderboard")
def get_leaderboard(user_id: int = Depends(get_current_user)):
    db = get_db()
    rows = db.execute("""
        SELECT u.id, u.username,
               COUNT(a.id) as total_attempts,
               COALESCE(SUM(a.is_correct), 0) as total_correct,
               CASE WHEN COUNT(a.id) > 0
                    THEN ROUND(CAST(SUM(a.is_correct) AS REAL) / COUNT(a.id) * 100, 1)
                    ELSE 0 END as accuracy,
               COUNT(DISTINCT DATE(a.attempted_at)) as active_days
        FROM users u
        LEFT JOIN quiz_attempts a ON a.user_id = u.id
        GROUP BY u.id
        ORDER BY total_correct DESC, accuracy DESC
    """).fetchall()

    # Calculate streaks for each user
    leaderboard = []
    for i, r in enumerate(rows):
        # Get streak: consecutive days with quiz activity ending today or yesterday
        dates = db.execute(
            "SELECT DISTINCT DATE(attempted_at) as d FROM quiz_attempts WHERE user_id = ? ORDER BY d DESC",
            (r["id"],)
        ).fetchall()
        streak = 0
        if dates:
            from datetime import date, timedelta
            today = date.today()
            expected = today
            for row in dates:
                d = date.fromisoformat(row["d"])
                if d == expected:
                    streak += 1
                    expected -= timedelta(days=1)
                elif d == expected - timedelta(days=1) and streak == 0:
                    # Allow streak to start from yesterday
                    streak = 1
                    expected = d - timedelta(days=1)
                else:
                    break

        leaderboard.append({
            "rank": i + 1,
            "user_id": r["id"],
            "username": r["username"],
            "total_correct": r["total_correct"],
            "total_attempts": r["total_attempts"],
            "accuracy": r["accuracy"],
            "streak": streak,
            "active_days": r["active_days"],
            "is_me": r["id"] == user_id,
        })
    db.close()
    return leaderboard


@app.post("/api/battles")
async def create_battle(request: Request, user_id: int = Depends(get_current_user)):
    """Create a quiz battle. Picks questions from a topic for everyone to answer."""
    body = await request.json()
    topic = (body.get("topic") or "").strip()
    num_questions = min(int(body.get("num_questions", 10)), 20)

    db = get_db()
    # Find questions matching the topic (from any user's materials — shared battle)
    questions = db.execute(
        "SELECT id FROM quiz_questions WHERE topic LIKE ? ORDER BY RANDOM() LIMIT ?",
        (f"%{topic}%", num_questions)
    ).fetchall()

    if len(questions) < 3:
        db.close()
        raise HTTPException(400, f"Not enough questions for topic '{topic}'. Need at least 3, found {len(questions)}. Generate more quizzes first!")

    qids = ",".join(str(q["id"]) for q in questions)
    cur = db.execute(
        "INSERT INTO quiz_battles (creator_id, topic, question_ids) VALUES (?,?,?)",
        (user_id, topic, qids)
    )
    battle_id = cur.lastrowid
    # Auto-join creator
    db.execute(
        "INSERT INTO battle_participants (battle_id, user_id, total) VALUES (?,?,?)",
        (battle_id, user_id, len(questions))
    )
    db.commit()

    creator = db.execute("SELECT username FROM users WHERE id = ?", (user_id,)).fetchone()
    db.close()
    return {"id": battle_id, "topic": topic, "num_questions": len(questions), "creator": creator["username"]}


@app.get("/api/battles")
def list_battles(user_id: int = Depends(get_current_user)):
    db = get_db()
    battles = db.execute("""
        SELECT b.id, b.topic, b.status, b.created_at, b.question_ids,
               u.username as creator_name, b.creator_id
        FROM quiz_battles b JOIN users u ON b.creator_id = u.id
        ORDER BY b.created_at DESC LIMIT 20
    """).fetchall()

    result = []
    for b in battles:
        participants = db.execute("""
            SELECT bp.user_id, u.username, bp.score, bp.total, bp.completed
            FROM battle_participants bp JOIN users u ON bp.user_id = u.id
            WHERE bp.battle_id = ?
            ORDER BY bp.score DESC
        """, (b["id"],)).fetchall()

        num_qs = len(b["question_ids"].split(","))
        result.append({
            "id": b["id"],
            "topic": b["topic"],
            "status": b["status"],
            "created_at": b["created_at"],
            "creator": b["creator_name"],
            "num_questions": num_qs,
            "participants": [
                {"user_id": p["user_id"], "username": p["username"],
                 "score": p["score"], "total": p["total"], "completed": bool(p["completed"]),
                 "is_me": p["user_id"] == user_id}
                for p in participants
            ],
            "i_joined": any(p["user_id"] == user_id for p in participants),
            "i_completed": any(p["user_id"] == user_id and p["completed"] for p in participants),
        })
    db.close()
    return result


@app.post("/api/battles/{bid}/join")
def join_battle(bid: int, user_id: int = Depends(get_current_user)):
    db = get_db()
    battle = db.execute("SELECT * FROM quiz_battles WHERE id = ?", (bid,)).fetchone()
    if not battle:
        db.close()
        raise HTTPException(404, "Battle not found")
    existing = db.execute(
        "SELECT 1 FROM battle_participants WHERE battle_id = ? AND user_id = ?", (bid, user_id)
    ).fetchone()
    if existing:
        db.close()
        return {"ok": True, "message": "Already joined"}
    num_qs = len(battle["question_ids"].split(","))
    db.execute(
        "INSERT INTO battle_participants (battle_id, user_id, total) VALUES (?,?,?)",
        (bid, user_id, num_qs)
    )
    db.commit()
    db.close()
    return {"ok": True}


@app.get("/api/battles/{bid}/questions")
def get_battle_questions(bid: int, user_id: int = Depends(get_current_user)):
    """Get the questions for a battle (must have joined)."""
    db = get_db()
    participant = db.execute(
        "SELECT * FROM battle_participants WHERE battle_id = ? AND user_id = ?", (bid, user_id)
    ).fetchone()
    if not participant:
        db.close()
        raise HTTPException(403, "Join the battle first")
    if participant["completed"]:
        db.close()
        raise HTTPException(400, "You already completed this battle")

    battle = db.execute("SELECT * FROM quiz_battles WHERE id = ?", (bid,)).fetchone()
    qids = battle["question_ids"].split(",")
    placeholders = ",".join("?" * len(qids))
    questions = db.execute(
        f"SELECT id, topic, question, options, difficulty FROM quiz_questions WHERE id IN ({placeholders})",
        qids
    ).fetchall()
    db.close()

    return [{
        "id": q["id"],
        "topic": q["topic"],
        "question": q["question"],
        "options": json.loads(q["options"]) if isinstance(q["options"], str) else q["options"],
        "difficulty": q["difficulty"],
    } for q in questions]


@app.post("/api/battles/{bid}/submit")
async def submit_battle(bid: int, request: Request, user_id: int = Depends(get_current_user)):
    """Submit all battle answers at once. Body: {answers: {question_id: chosen_answer, ...}}"""
    body = await request.json()
    answers = body.get("answers", {})

    db = get_db()
    participant = db.execute(
        "SELECT * FROM battle_participants WHERE battle_id = ? AND user_id = ?", (bid, user_id)
    ).fetchone()
    if not participant:
        db.close()
        raise HTTPException(403, "Join the battle first")
    if participant["completed"]:
        db.close()
        raise HTTPException(400, "Already submitted")

    battle = db.execute("SELECT * FROM quiz_battles WHERE id = ?", (bid,)).fetchone()
    qids = battle["question_ids"].split(",")
    placeholders = ",".join("?" * len(qids))
    questions = db.execute(
        f"SELECT id, correct_answer, topic, material_id, explanation FROM quiz_questions WHERE id IN ({placeholders})",
        qids
    ).fetchall()

    score = 0
    results = []
    for q in questions:
        given = answers.get(str(q["id"]), "")
        correct = given == q["correct_answer"]
        if correct:
            score += 1
        results.append({
            "question_id": q["id"],
            "your_answer": given,
            "correct_answer": q["correct_answer"],
            "correct": correct,
            "explanation": q["explanation"],
        })
        # Also record in quiz_attempts for leaderboard stats
        db.execute(
            "INSERT INTO quiz_attempts (question_id, material_id, user_id, topic, user_answer, is_correct) VALUES (?,?,?,?,?,?)",
            (q["id"], q["material_id"], user_id, q["topic"], given, 1 if correct else 0)
        )

    db.execute(
        "UPDATE battle_participants SET score = ?, completed = 1, finished_at = CURRENT_TIMESTAMP WHERE battle_id = ? AND user_id = ?",
        (score, bid, user_id)
    )
    db.commit()

    # Return updated standings
    standings = db.execute("""
        SELECT u.username, bp.score, bp.total, bp.completed
        FROM battle_participants bp JOIN users u ON bp.user_id = u.id
        WHERE bp.battle_id = ? ORDER BY bp.score DESC
    """, (bid,)).fetchall()

    db.close()
    return {
        "score": score,
        "total": len(questions),
        "results": results,
        "standings": [{"username": s["username"], "score": s["score"],
                       "total": s["total"], "completed": bool(s["completed"])} for s in standings],
    }


# ── Tutor (streaming) ────────────────────────────────────────────────────────

@app.post("/api/chat")
async def chat(request: Request, user_id: int = Depends(get_current_user)):
    body = await request.json()
    message = body.get("message", "")
    mode = body.get("mode", "explain")
    session_id = body.get("session_id", "default")
    mid = body.get("material_id")

    db = get_db()
    history = list(reversed(db.execute(
        "SELECT role, content FROM chat_messages WHERE session_id = ? AND user_id = ? ORDER BY timestamp DESC LIMIT 12",
        (session_id, user_id)
    ).fetchall()))

    mat_ctx = ""
    if mid and user_can_access(db, mid, user_id):
        mat = db.execute("SELECT original_name, content FROM materials WHERE id = ?", (mid,)).fetchone()
        if mat:
            mat_ctx = f"\n\nContext from '{mat['original_name']}':\n{mat['content'][:3000]}"

    db.execute("INSERT INTO chat_messages (user_id, session_id, role, content) VALUES (?,?,?,?)", (user_id, session_id, "user", message))
    db.commit()
    db.close()

    if mode == "socratic":
        system_text = f"""You are a Socratic medical tutor. Guide the student to discover answers through questions rather than giving them directly. Ask one focused question at a time. Be encouraging but intellectually challenging. Use clinical scenarios. Keep responses to 2-3 sentences + one guiding question.{mat_ctx}"""
    else:
        system_text = f"""You are an expert medical tutor for a health sciences student. Give clear, accurate explanations with clinical context. Use mnemonics and bullet points. Relate concepts to clinical practice. Be thorough but concise.{mat_ctx}"""

    # Cache the system block (contains the material context) so each follow-up turn in a
    # multi-turn conversation reuses it at ~10% cost instead of re-sending it in full.
    system = [{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}]

    messages = [{"role": r["role"], "content": r["content"]} for r in history]
    messages.append({"role": "user", "content": message})

    def stream():
        full = ""
        try:
            with get_client().messages.stream(model=MODEL, max_tokens=1500, system=system, messages=messages) as s:
                for chunk in s.text_stream:
                    full += chunk
                    yield f"data: {json.dumps({'text': chunk})}\n\n"
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT INTO chat_messages (user_id, session_id, role, content) VALUES (?,?,?,?)", (user_id, session_id, "assistant", full))
            conn.commit()
            conn.close()
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@app.delete("/api/chat/{session_id}")
def clear_chat(session_id: str, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("DELETE FROM chat_messages WHERE session_id = ? AND user_id = ?", (session_id, user_id))
    db.commit()
    db.close()
    return {"ok": True}


# ── Progress ─────────────────────────────────────────────────────────────────

@app.get("/api/progress")
def get_progress(user_id: int = Depends(get_current_user)):
    db = get_db()

    # ── Quiz stats ─────────────────────────────────────────────────────────
    qs = dict(db.execute("SELECT COUNT(*) as t, SUM(is_correct) as c FROM quiz_attempts WHERE user_id = ?", (user_id,)).fetchone())
    quiz_topics = [dict(r) for r in db.execute(
        """SELECT topic, COUNT(*) as attempts, SUM(is_correct) as correct,
                  CAST(SUM(is_correct) AS REAL)/COUNT(*) as accuracy
           FROM quiz_attempts WHERE user_id = ? GROUP BY topic ORDER BY accuracy ASC""",
        (user_id,)
    ).fetchall()]

    # ── Flashcard stats ────────────────────────────────────────────────────
    fc = dict(db.execute(
        "SELECT COUNT(*) as total, SUM(times_seen) as reviews, SUM(times_correct) as correct FROM flashcards WHERE user_id = ?",
        (user_id,)
    ).fetchone())
    fc_topics = [dict(r) for r in db.execute(
        """SELECT topic, COUNT(*) as attempts, SUM(correct) as correct
           FROM flashcard_log WHERE user_id = ? AND topic IS NOT NULL GROUP BY topic""",
        (user_id,)
    ).fetchall()]

    # ── Daily activity — last 7 days ───────────────────────────────────────
    daily_quiz = [dict(r) for r in db.execute(
        """SELECT DATE(attempted_at) as date, COUNT(*) as attempts, SUM(is_correct) as correct
           FROM quiz_attempts WHERE user_id = ? AND attempted_at >= DATE('now','-7 days')
           GROUP BY DATE(attempted_at) ORDER BY date""",
        (user_id,)
    ).fetchall()]
    daily_fc = [dict(r) for r in db.execute(
        """SELECT DATE(reviewed_at) as date, COUNT(*) as reviews, SUM(correct) as correct
           FROM flashcard_log WHERE user_id = ? AND reviewed_at >= DATE('now','-7 days')
           GROUP BY DATE(reviewed_at) ORDER BY date""",
        (user_id,)
    ).fetchall()]

    # ── Combined topic mastery (quiz + flashcard, no API needed) ───────────
    # Normalize long topic names so chart labels stay readable
    topic_agg = defaultdict(lambda: {"attempts": 0, "correct": 0})
    for r in quiz_topics:
        t = _normalize_topic(r["topic"])
        topic_agg[t]["attempts"] += r["attempts"]
        topic_agg[t]["correct"]  += int(r["correct"] or 0)
    for r in fc_topics:
        t = _normalize_topic(r["topic"])
        topic_agg[t]["attempts"] += r["attempts"]
        topic_agg[t]["correct"]  += int(r["correct"] or 0)
    combined_topics = sorted(
        [{"topic": t, "attempts": d["attempts"], "correct": d["correct"],
          "accuracy": d["correct"] / d["attempts"] if d["attempts"] else 0}
         for t, d in topic_agg.items()],
        key=lambda x: x["accuracy"]
    )

    # ── Counts ─────────────────────────────────────────────────────────────
    mats   = db.execute("SELECT COUNT(*) as c FROM user_materials WHERE user_id = ?", (user_id,)).fetchone()["c"]
    fcs    = db.execute("SELECT COUNT(*) as c FROM flashcards WHERE user_id = ?", (user_id,)).fetchone()["c"]
    slides = db.execute("SELECT COUNT(*) as c FROM revision_slides WHERE user_id = ?", (user_id,)).fetchone()["c"]
    db.close()

    return {
        "quiz": {
            "total":    qs["t"] or 0,
            "correct":  qs["c"] or 0,
            "accuracy": round(((qs["c"] or 0) / max(qs["t"] or 1, 1)) * 100, 1),
            "by_topic": [
                {**t, "topic": _normalize_topic(t["topic"])} for t in quiz_topics
            ],
        },
        "flashcards":      fc,
        "daily":           daily_quiz,
        "daily_fc":        daily_fc,
        "combined_topics": combined_topics,
        "counts":          {"materials": mats, "flashcards": fcs, "slides": slides},
    }


# ── Knowledge Graph ──────────────────────────────────────────────────────────

@app.get("/api/knowledge-graph")
def knowledge_graph(user_id: int = Depends(get_current_user)):
    """Build a graph of materials ↔ topics with performance data."""
    db = get_db()

    # Get user's materials
    mats = db.execute("""
        SELECT m.id, m.original_name, m.subject, m.file_type, LENGTH(m.content) as chars
        FROM materials m JOIN user_materials um ON um.material_id = m.id
        WHERE um.user_id = ?
    """, (user_id,)).fetchall()

    # Get topics from quiz questions linked to each material
    mat_topics = db.execute("""
        SELECT DISTINCT q.material_id, q.topic
        FROM quiz_questions q
        WHERE q.user_id = ? AND q.topic IS NOT NULL
    """, (user_id,)).fetchall()

    # Get topic performance
    topic_perf = db.execute("""
        SELECT topic, COUNT(*) as attempts, SUM(is_correct) as correct,
               CAST(SUM(is_correct) AS REAL)/COUNT(*) as accuracy
        FROM quiz_attempts WHERE user_id = ? GROUP BY topic
    """, (user_id,)).fetchall()
    perf_map = {_normalize_topic(r["topic"]): {
        "attempts": r["attempts"], "correct": r["correct"] or 0,
        "accuracy": round((r["accuracy"] or 0) * 100, 1)
    } for r in topic_perf}

    # Get flashcard topics per material
    fc_topics = db.execute("""
        SELECT DISTINCT material_id, topic FROM flashcards
        WHERE user_id = ? AND topic IS NOT NULL
    """, (user_id,)).fetchall()

    # Get user's graph customizations
    hidden_nodes = set(r["node_id"] for r in db.execute(
        "SELECT node_id FROM graph_hidden_nodes WHERE user_id = ?", (user_id,)
    ).fetchall())
    hidden_edges = set((r["source"], r["target"]) for r in db.execute(
        "SELECT source, target FROM graph_hidden_edges WHERE user_id = ?", (user_id,)
    ).fetchall())
    custom_edges = [(r["source"], r["target"]) for r in db.execute(
        "SELECT source, target FROM graph_custom_edges WHERE user_id = ?", (user_id,)
    ).fetchall()]

    db.close()

    # Build nodes and edges
    nodes = []
    edges = []
    topic_set = {}  # normalized_topic → node_id
    mat_node_ids = {}

    # Material nodes
    for m in mats:
        nid = f"mat_{m['id']}"
        if nid in hidden_nodes:
            continue
        mat_node_ids[m["id"]] = nid
        nodes.append({
            "id": nid, "type": "material", "label": m["original_name"][:30],
            "subject": m["subject"], "file_type": m["file_type"],
            "size": max(8, min(20, (m["chars"] or 0) / 5000 + 8)),
        })

    # Collect UNIQUE topic→material links (deduplicate across quiz + flashcard)
    all_links = set()
    for r in mat_topics:
        t = _normalize_topic(r["topic"])
        if t and r["material_id"] in mat_node_ids:
            all_links.add((r["material_id"], t))
    for r in fc_topics:
        t = _normalize_topic(r["topic"])
        if t and r["material_id"] in mat_node_ids:
            all_links.add((r["material_id"], t))

    # Edge dedup set — prevents any duplicate edges
    edge_set = set()
    def add_edge(src, tgt, **extra):
        key = tuple(sorted([src, tgt]))
        if key in edge_set:
            return False
        if key in hidden_edges or (src, tgt) in hidden_edges or (tgt, src) in hidden_edges:
            return False
        edge_set.add(key)
        edges.append({"source": src, "target": tgt, **extra})
        return True

    # Topic nodes + edges to materials
    for mid, topic in all_links:
        if topic not in topic_set:
            tid = f"topic_{len(topic_set)}"
            if tid in hidden_nodes:
                topic_set[topic] = tid
                continue
            topic_set[topic] = tid
            perf = perf_map.get(topic, {"attempts": 0, "correct": 0, "accuracy": 0})
            nodes.append({
                "id": tid, "type": "topic", "label": topic,
                "accuracy": perf["accuracy"], "attempts": perf["attempts"],
                "size": max(6, min(16, perf["attempts"] / 2 + 6)),
            })
        tid = topic_set[topic]
        node_ids_set = set(n["id"] for n in nodes)
        src, tgt = mat_node_ids[mid], tid
        if src in node_ids_set and tgt in node_ids_set:
            add_edge(src, tgt)

    # Subject nodes — group materials by subject
    subjects = {}
    for m in mats:
        subj = m["subject"] or "General"
        mid = m["id"]
        if mid not in mat_node_ids:
            continue
        if subj not in subjects:
            sid = f"subj_{len(subjects)}"
            if sid in hidden_nodes:
                subjects[subj] = sid
                continue
            subjects[subj] = sid
            nodes.append({"id": sid, "type": "subject", "label": subj, "size": 22})
        add_edge(subjects[subj], mat_node_ids[mid])

    # Custom user-created edges
    node_ids_set = set(n["id"] for n in nodes)
    for src, tgt in custom_edges:
        if src in node_ids_set and tgt in node_ids_set:
            add_edge(src, tgt, custom=True)

    # Auto-link similar topics (word-overlap ≥ 0.3) — no self-links
    topic_nodes_list = [n for n in nodes if n["type"] == "topic"]
    for i in range(len(topic_nodes_list)):
        wi = set(topic_nodes_list[i]["label"].lower().split())
        for j in range(i + 1, len(topic_nodes_list)):
            wj = set(topic_nodes_list[j]["label"].lower().split())
            inter = len(wi & wj)
            union = len(wi | wj)
            if union > 0 and inter / union >= 0.3:
                add_edge(topic_nodes_list[i]["id"], topic_nodes_list[j]["id"], similarity=True)

    return {"nodes": nodes, "edges": edges}


# ── Knowledge Graph Modifications ─────────────────────────────────────────────

class GraphNodeAction(BaseModel):
    node_id: str

class GraphEdgeAction(BaseModel):
    source: str
    target: str

@app.post("/api/knowledge-graph/hide-node")
def graph_hide_node(body: GraphNodeAction, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("INSERT OR IGNORE INTO graph_hidden_nodes (user_id, node_id) VALUES (?, ?)",
               (user_id, body.node_id))
    # Also hide all edges to/from this node
    db.execute("DELETE FROM graph_custom_edges WHERE user_id = ? AND (source = ? OR target = ?)",
               (user_id, body.node_id, body.node_id))
    db.commit(); db.close()
    return {"ok": True}

@app.post("/api/knowledge-graph/restore-node")
def graph_restore_node(body: GraphNodeAction, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("DELETE FROM graph_hidden_nodes WHERE user_id = ? AND node_id = ?",
               (user_id, body.node_id))
    db.commit(); db.close()
    return {"ok": True}

@app.post("/api/knowledge-graph/hide-edge")
def graph_hide_edge(body: GraphEdgeAction, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("INSERT OR IGNORE INTO graph_hidden_edges (user_id, source, target) VALUES (?, ?, ?)",
               (user_id, body.source, body.target))
    # Also remove if it was a custom edge
    db.execute("DELETE FROM graph_custom_edges WHERE user_id = ? AND source = ? AND target = ?",
               (user_id, body.source, body.target))
    db.commit(); db.close()
    return {"ok": True}

@app.post("/api/knowledge-graph/add-edge")
def graph_add_edge(body: GraphEdgeAction, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("INSERT OR IGNORE INTO graph_custom_edges (user_id, source, target) VALUES (?, ?, ?)",
               (user_id, body.source, body.target))
    # Remove from hidden if it was hidden before
    db.execute("DELETE FROM graph_hidden_edges WHERE user_id = ? AND source = ? AND target = ?",
               (user_id, body.source, body.target))
    db.commit(); db.close()
    return {"ok": True}

@app.post("/api/knowledge-graph/reset")
def graph_reset(user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("DELETE FROM graph_hidden_nodes WHERE user_id = ?", (user_id,))
    db.execute("DELETE FROM graph_hidden_edges WHERE user_id = ?", (user_id,))
    db.execute("DELETE FROM graph_custom_edges WHERE user_id = ?", (user_id,))
    db.commit(); db.close()
    return {"ok": True}


# ── Exam dates & study plan ───────────────────────────────────────────────────

class ExamIn(BaseModel):
    subject: str
    exam_date: str
    notes: Optional[str] = ""


@app.post("/api/exam-dates")
def add_exam(e: ExamIn, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("INSERT INTO exam_dates (user_id, subject, exam_date, notes) VALUES (?,?,?,?)", (user_id, e.subject, e.exam_date, e.notes))
    db.commit()
    db.close()
    return {"ok": True}


@app.get("/api/exam-dates")
def list_exams(user_id: int = Depends(get_current_user)):
    db = get_db()
    rows = db.execute("SELECT * FROM exam_dates WHERE user_id = ? ORDER BY exam_date", (user_id,)).fetchall()
    db.close()
    return [dict(r) for r in rows]


@app.delete("/api/exam-dates/{eid}")
def delete_exam(eid: int, user_id: int = Depends(get_current_user)):
    db = get_db()
    db.execute("DELETE FROM exam_dates WHERE id = ? AND user_id = ?", (eid, user_id))
    db.commit()
    db.close()
    return {"ok": True}


@app.post("/api/generate/studyplan")
async def gen_study_plan(request: Request, user_id: int = Depends(get_current_user)):
    body = await request.json()
    exam_date = body.get("exam_date", "")
    subject = body.get("subject", "Medicine")

    db = get_db()
    weak = [dict(r) for r in db.execute(
        "SELECT topic, CAST(SUM(is_correct) AS REAL)/COUNT(*) as acc FROM quiz_attempts WHERE user_id = ? GROUP BY topic ORDER BY acc ASC LIMIT 5",
        (user_id,)
    ).fetchall()]
    mats = [r["original_name"] for r in db.execute(
        """SELECT m.original_name FROM materials m
           JOIN user_materials um ON um.material_id = m.id WHERE um.user_id = ?""",
        (user_id,)
    ).fetchall()]
    db.close()

    days_left = 30
    if exam_date:
        try:
            days_left = max(1, (date.fromisoformat(exam_date) - date.today()).days)
        except Exception:
            pass

    weak_str = ", ".join([f"{r['topic']} ({round(r['acc']*100)}%)" for r in weak]) or "No data yet — start quizzing!"
    mats_str = ", ".join(mats) or "No materials uploaded yet"

    resp = get_client().messages.create(
        model=MODEL, max_tokens=2500,
        messages=[{"role": "user", "content": f"""Create a personalised medical study plan.

Subject: {subject}
Days until exam: {days_left}
Materials: {mats_str}
Weak topics: {weak_str}

Generate a plan for {min(days_left, 14)} days. Return ONLY JSON:
{{
  "overview": "Brief 2-sentence strategy",
  "daily_hours": 3,
  "days": [{{
    "day": 1,
    "focus": "Main topic",
    "tasks": ["Task 1", "Task 2", "Task 3"],
    "priority": "high"
  }}]
}}

Prioritise weak topics. Mix flashcard review, active recall, and new content."""}]
    )

    try:
        return parse_json_response(resp.content[0].text)
    except Exception:
        return {"overview": "Could not generate plan", "daily_hours": 3, "days": []}


# ── Mind maps ────────────────────────────────────────────────────────────────

@app.post("/api/generate/mindmap/{mid}")
def generate_mindmap(mid: int, force: bool = False, user_id: int = Depends(get_current_user)):
    db = get_db()
    if not user_can_access(db, mid, user_id):
        db.close()
        raise HTTPException(403, "No access to this material")
    mat = db.execute("SELECT * FROM materials WHERE id = ?", (mid,)).fetchone()
    if not mat:
        raise HTTPException(404, "Material not found")

    # Memory: reuse the existing mind map without an AI call unless forced
    if not force:
        row = db.execute("SELECT data FROM mind_maps WHERE material_id = ? AND user_id = ?", (mid, user_id)).fetchone()
        if row:
            db.close()
            try:
                return json.loads(row["data"])
            except Exception:
                pass
            db = get_db()  # reopen if the stored data was unparseable

    instructions = """Create a mind map from the SOURCE STUDY MATERIAL above.

Return ONLY valid JSON matching this exact structure — no markdown, no extra keys:
{
  "id": "root",
  "label": "Short topic name",
  "children": [
    {
      "id": "b1",
      "label": "Branch name",
      "children": [
        {"id": "l1_1", "label": "Leaf label", "children": []},
        {"id": "l1_2", "label": "Leaf label", "children": []}
      ]
    }
  ]
}

Rules:
- 4–6 main branches
- 2–4 leaves per branch
- Root label: 1–3 words (the topic name)
- Branch labels: 2–4 words (a key concept or category)
- Leaf labels: 2–5 words (a specific fact, term, or sub-concept)
- Never use colons or slashes inside labels — split into two separate leaves instead
- All ids must be unique strings"""

    text = generate_json(mat, instructions, model=HAIKU, max_tokens=3000)
    try:
        data = parse_json_response(text)
    except Exception:
        data = {"id": "root", "label": mat["original_name"], "children": [{"id": "e1", "label": "Error — try again", "children": []}]}

    db.execute("DELETE FROM mind_maps WHERE material_id = ? AND user_id = ?", (mid, user_id))
    db.execute("INSERT INTO mind_maps (material_id, user_id, title, data) VALUES (?,?,?,?)", (mid, user_id, mat["original_name"], json.dumps(data)))
    db.commit()
    db.close()
    return data


@app.get("/api/mindmaps")
def get_mindmaps(material_id: Optional[int] = None, user_id: int = Depends(get_current_user)):
    db = get_db()
    base = "SELECT mm.*, m.original_name FROM mind_maps mm JOIN materials m ON mm.material_id = m.id"
    rows = db.execute(base + " WHERE mm.material_id = ? AND mm.user_id = ?", (material_id, user_id)).fetchall() \
        if material_id else db.execute(base + " WHERE mm.user_id = ?", (user_id,)).fetchall()
    db.close()
    result = []
    for r in rows:
        d = dict(r)
        try:
            d["data"] = json.loads(d["data"])
        except Exception:
            pass
        result.append(d)
    return result


# ── Network info ─────────────────────────────────────────────────────────────

@app.get("/api/network-info")
def network_info():
    """Returns LAN IPs and the current Cloudflare tunnel URL (read from the tunnel log)."""
    import socket, re
    ips: list[str] = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and ip not in ("127.0.0.1", "0.0.0.0"):
            ips.append(ip)
    except Exception:
        pass
    try:
        hostname = socket.gethostname()
        for info in socket.getaddrinfo(hostname, None):
            ip = info[4][0]
            if ":" in ip:
                continue
            if ip.startswith(("192.168.", "10.", "172.")) and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    # Read the current Cloudflare tunnel URL from the log file
    tunnel_url: Optional[str] = None
    log_path = Path("data/tunnel.log")
    if log_path.exists():
        try:
            text = log_path.read_text(errors="ignore")
            # Find the last trycloudflare.com URL in the log
            matches = re.findall(r'https://[a-z0-9-]+\.trycloudflare\.com', text)
            if matches:
                tunnel_url = matches[-1]
        except Exception:
            pass

    return {"ips": ips, "port": 8000, "tunnel_url": tunnel_url}


# ── Serve material images ─────────────────────────────────────────────────────
# Images are stored in IMAGES_DIR (either static/material_images locally, or
# /data/material_images on Railway). All new image URLs use /images/{filename}.
# Old /static/material_images/ URLs still work locally via the StaticFiles mount.

@app.get("/images/{filename}")
def serve_image(filename: str):
    """Serve a material image from IMAGES_DIR (works locally and on Railway)."""
    # Reject any path-traversal attempts — only allow a bare filename inside IMAGES_DIR
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(404, "Image not found")
    p = (IMAGES_DIR / filename).resolve()
    if IMAGES_DIR.resolve() not in p.parents or not p.is_file():
        raise HTTPException(404, "Image not found")
    return FileResponse(str(p))


# ── Serve static ─────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory="static"), name="static")


def _print_startup():
    import socket
    print("\n  MedVault — Your Medical Study Vault")
    print("  " + "─" * 42)
    print("  Local   → http://localhost:8000")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and ip not in ("127.0.0.1", "0.0.0.0"):
            print(f"  Network → http://{ip}:8000  (share with classmates)")
    except Exception:
        pass
    print("  Press Ctrl+C to stop\n")


if __name__ == "__main__":
    import uvicorn
    _print_startup()
    uvicorn.run(app, host="0.0.0.0", port=8000)

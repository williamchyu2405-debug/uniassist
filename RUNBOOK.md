# MedVault — Railway (Free tier) deploy runbook

Get the full app online, password-locked, on Railway's **Free** plan (~$0/mo with App
Sleeping). Zero-API: the guide quizzes work with no Anthropic credits.

The steps that touch your account/billing (push, dashboard, volume, App Sleeping) are
**yours** — Claude prepped everything in the repo but can't click those for you.

---

## What goes online vs stays local
- **Online:** the app (quiz / flashcards / dashboard / knowledge graph) behind your
  `ACCESS_CODE`, plus the **public gallery** at `/guides` (12 guides) which stays open
  by design (shareable). 12 guide quiz banks (334 Q) seed with zero API calls.
- **Stays LOCAL only (never deployed):** the 3 copyright-noticed guides
  (Bone Physiology II, Muscle Physiology I, Ventilation) — their HTML is gitignored
  (`static/guides/private/`) and their quiz banks live in the gitignored
  `guide_quizzes.local.json`. The repo is **public**, so this keeps that content off
  GitHub and off the deploy. You keep studying all 15 on localhost.

---

## One-time setup

### 1. Push the code (you)
Claude committed everything locally but **cannot push** (blocked). From the repo:
```bash
git push origin main
```

### 2. Create / point the Railway project at the repo
- Railway → **New Project → Deploy from GitHub repo → `williamchyu2405-debug/uniassist`**
  (or reuse your old MedVault project and just redeploy the latest commit).
- Build is automatic: `railway.toml` uses **nixpacks** (installs `requirements.txt`) and
  starts `uvicorn main:app --host 0.0.0.0 --port $PORT`. No Dockerfile needed.

### 3. Add a persistent Volume (so the DB survives restarts)
- Service → **Variables/Settings → Volumes → New Volume**, mount path **`/data`**.

### 4. Set service Variables
| Variable | Value | Why |
|---|---|---|
| `DATA_DIR` | `/data` | writes `study.db` + uploads onto the volume |
| `ACCESS_CODE` | *a passphrase you pick* | gates the app. **Never blank on a public URL.** Don't reuse the old exposed code. |
| `ANTHROPIC_API_KEY` | *(leave unset)* | unset = zero-API mode; quizzes still work |

### 5. Deploy, then turn on App Sleeping (this is what keeps it ~free)
- Let it build + deploy.
- Service → **Settings → Serverless / App Sleeping → ON.**
  The app sleeps after ~10 min idle (you only pay storage while asleep); first visit
  after idle has a ~1s cold start. Verified: MedVault has no background traffic, so it
  will actually sleep. Left always-on instead, Free's $1/mo credit runs out mid-month
  and the app pauses without warning.

### 6. Populate the database (pick one)
- **B — fresh seed (recommended, simplest, zero-API):** run once
  ```bash
  railway run python seed_on_boot.py        # creates user "william" + seeds the 12 guide banks
  ```
  (or Service → ⋮ → *Run a command* → `python seed_on_boot.py`). Idempotent.
- **A — bring your exact local history + uploaded materials:** Railway has no direct
  volume upload, and `study.db` is gitignored (public repo — don't commit it). If you
  want your real state online, tell Claude and it'll add a one-time authenticated
  `/api/admin/import-db` endpoint you can upload through. (Your DB is only ~508 KB.)

### 7. First login
Open the URL → enter `ACCESS_CODE` → log in as `william`. If the account has no
password yet, the first login sets it. Open **/guides**, hit any guide's **Quiz**.

---

## Redeploying after future changes
`git push origin main` → Railway auto-rebuilds (~30–60s) → hard-refresh (Cmd+Shift+R).

## If you'd rather never think about the $1 ceiling
Upgrade to **Hobby ($5/mo)**: always-on, 5 GB storage, no App-Sleeping cold starts.
Same repo/volume — just change the plan.

## Troubleshooting
- **App is empty / no quizzes:** run step 6B, or just click a guide's Quiz (it self-seeds).
- **"Server error" on AI features:** expected with no `ANTHROPIC_API_KEY` — those need
  credits; guide quizzes/gallery don't.
- **Locked out / forgot code:** change `ACCESS_CODE` in Variables → redeploy.
- **Data vanished after redeploy:** the Volume isn't mounted at `/data`, or `DATA_DIR`
  isn't `/data`. Fix both (step 3–4).

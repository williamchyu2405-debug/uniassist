// ── Themes — Deep-focus accent variants ───────────────────────────────────
// The shell is always dark slate (#0f172a) and the canvas always light; a
// theme only swaps the accent ramp: brand (vivid, shell/actions), brandStrong
// (hover), brandDeep (accent text/icons on light), brandSoft (tint washes).
const THEMES = {
  deepfocus: {
    name:'Deep Focus', brand:'#22d3ee', brandStrong:'#06b6d4', brandDeep:'#0891b2',
    brandSoft:'rgba(34,211,238,0.14)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#155e75 100%)',
  },
  sapphire: {
    name:'Sapphire', brand:'#60a5fa', brandStrong:'#3b82f6', brandDeep:'#2563eb',
    brandSoft:'rgba(96,165,250,0.14)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#1e3a8a 100%)',
  },
  emerald: {
    name:'Emerald', brand:'#34d399', brandStrong:'#10b981', brandDeep:'#059669',
    brandSoft:'rgba(52,211,153,0.14)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#065f46 100%)',
  },
  aurora: {
    name:'Aurora', brand:'#a78bfa', brandStrong:'#8b5cf6', brandDeep:'#7c3aed',
    brandSoft:'rgba(167,139,250,0.14)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#4c1d95 100%)',
  },
  ember: {
    name:'Ember', brand:'#fbbf24', brandStrong:'#f59e0b', brandDeep:'#d97706',
    brandSoft:'rgba(251,191,36,0.14)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#92400e 100%)',
  },
  titanium: {
    name:'Titanium', brand:'#94a3b8', brandStrong:'#64748b', brandDeep:'#475569',
    brandSoft:'rgba(148,163,184,0.16)',
    heroBg:'linear-gradient(135deg,#0f172a 0%,#1e293b 55%,#334155 100%)',
  },
};
const THEME_SHELL = '#0f172a';
const THEME_CANVAS = '#f8fafc';

// ── State ─────────────────────────────────────────────────────────────────
const S = {
  page: 'dashboard',
  userId: null, username: null,
  materials: [],
  slides: [],    slideIdx: 0,
  flashcards: [], fcIdx: 0, fcFlipped: false, fcCorrect: 0,
  quiz: [],       qIdx: 0,  qCorrect: 0, qAnswered: false,
  quizResults: [], quizDifficulty: 'adaptive',
  tutorMode: 'explain',
  sessionId: Math.random().toString(36).slice(2),
  examDates: [],
  mistakes: [],
  charts: {},
};

// ── SMILES structure rendering ───────────────────────────────────────────
function renderSmiles(smiles, container) {
  if (!smiles || !window.SmilesDrawer) return;
  const canvas = document.createElement('canvas');
  canvas.width = 300; canvas.height = 200;
  canvas.style.cssText = 'max-width:100%;height:auto;display:block;margin:8px auto;background:#fff;border-radius:8px;border:1px solid #e2e8f0;';
  container.appendChild(canvas);
  try {
    const drawer = new SmilesDrawer.SmiDrawer({ width: 300, height: 200 });
    drawer.draw(smiles, canvas, 'light');
  } catch(e) { canvas.remove(); }
}

function renderSmilesInEl(smiles, parentEl, position) {
  let smilesDiv = parentEl.querySelector('.smiles-structure');
  // No structure for this card — clear any leftover from the previous one,
  // otherwise the molecule lingers onto the next (non-chem) question/card.
  if (!smiles) { if (smilesDiv) smilesDiv.remove(); return; }
  if (!smilesDiv) {
    smilesDiv = document.createElement('div');
    smilesDiv.className = 'smiles-structure';
    if (position === 'prepend') parentEl.prepend(smilesDiv);
    else parentEl.appendChild(smilesDiv);
  }
  smilesDiv.innerHTML = '';
  renderSmiles(smiles, smilesDiv);
}

// ── API helper ────────────────────────────────────────────────────────────
// Central fetch wrapper. Network / HTTP failures surface as an error toast here
// (#10) so page code can't silently swallow them — pass { quiet: true } for
// genuinely-optional background calls (badge refreshes, SRS pings, telemetry-ish
// writes) that shouldn't nag. Auth walls (401/403) show their gate, never a toast.
async function api(method, path, body, fetchOpts = {}) {
  const opts = { method, headers: {} };
  const token = localStorage.getItem('ua_token');
  if (token)         opts.headers['Authorization']  = 'Bearer ' + token;
  else if (S.userId) opts.headers['X-User-Id']      = S.userId;   // legacy fallback
  const ac = sessionStorage.getItem('ua_access_code');
  if (ac)            opts.headers['X-Access-Code']  = ac;
  if (body && !(body instanceof FormData)) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(body);
  } else if (body instanceof FormData) {
    opts.body = body;
  }
  let res;
  try {
    res = await fetch(path, opts);
  } catch (e) {
    const msg = 'Can’t reach the server — check it’s running and try again';
    if (!fetchOpts.quiet) toast(msg, 'error');
    throw new Error(msg);
  }
  if (res.status === 403) {
    const err = await res.json().catch(() => ({}));
    if (err.detail === 'access_code_required') {
      showAccessGate();
      throw new Error('Enter the access code to continue');
    }
  }
  if (res.status === 401) {
    showProfileGate();
    throw new Error('Please choose a profile to continue');
  }
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    const msg = err.detail || 'Request failed';
    if (!fetchOpts.quiet) toast(msg, 'error');
    throw new Error(msg);
  }
  return res.json();
}

function loading(show, text = 'Generating with AI…') {
  document.getElementById('loading-overlay').classList.toggle('hidden', !show);
  document.getElementById('loading-text').textContent = text;
}

// ── Skeleton loaders (#6) ─────────────────────────────────────────────────
// Shimmer placeholders shown while a load* fetch is in flight.

// List-row skeletons (materials / discover style)
function skelRows(n = 3) {
  return Array.from({ length: n }, () => `
    <div class="flex items-center gap-3 p-3 rounded-xl border border-slate-100" aria-hidden="true">
      <div class="skeleton w-9 h-9 rounded-lg flex-shrink-0"></div>
      <div class="flex-1 space-y-2">
        <div class="skeleton h-3" style="width:55%"></div>
        <div class="skeleton h-3" style="width:32%"></div>
      </div>
    </div>`).join('');
}

// One large block (flashcard / quiz card / chart placeholder)
function skelBlock(height = 300, extra = '') {
  return `<div class="max-w-2xl mx-auto ${extra}" aria-hidden="true"><div class="skeleton rounded-2xl" style="height:${height}px"></div></div>`;
}

// Overlay / remove a shimmer on a chart canvas (parent must be position:relative)
function setChartSkeleton(canvasId, show) {
  const wrap = document.getElementById(canvasId)?.parentElement;
  if (!wrap) return;
  let sk = wrap.querySelector('.chart-skeleton');
  if (show && !sk) {
    sk = document.createElement('div');
    sk.className = 'chart-skeleton skeleton';
    sk.setAttribute('aria-hidden', 'true');
    wrap.appendChild(sk);
  } else if (!show && sk) sk.remove();
}

// Toggle shimmer on the dashboard stat numbers
function setStatSkeletons(ids, show) {
  ids.forEach(id => document.getElementById(id)?.classList.toggle('skeleton', show));
}

// ── Empty states (#7) — icon + one-line prompt, consistent voice ──────────
function emptyState(icon, title, hint = '', compact = false) {
  return `<div class="empty-state${compact ? ' compact' : ''}">
    <div class="es-icon" aria-hidden="true">${icon}</div>
    <div class="es-title">${title}</div>
    ${hint ? `<div class="es-hint">${hint}</div>` : ''}
  </div>`;
}

let _lastToast = { msg: '', t: 0 };
function toast(msg, type = 'info') {
  // Anti-spam: an identical message within 2.5s is dropped — covers api()'s
  // centralized error toast overlapping a caller's own toast(e.message), and
  // parallel requests failing with the same network error.
  const now = Date.now();
  if (msg === _lastToast.msg && now - _lastToast.t < 2500) return;
  _lastToast = { msg, t: now };
  const icons = { info: 'ℹ️', success: '✓', error: '✕' };
  const bgs = { info: 'rgba(41,37,36,0.85)', success: 'rgba(87,83,78,0.85)', error: 'rgba(220,38,38,0.85)' };
  const el = document.createElement('div');
  el.style.cssText = `position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);background:${bgs[type]};color:white;padding:12px 24px;border-radius:14px;font-size:0.85rem;font-weight:500;box-shadow:0 8px 40px rgba(0,0,0,0.2);z-index:100;opacity:0;transition:all 0.35s cubic-bezier(0.4,0,0.2,1);display:flex;align-items:center;gap:8px;font-family:Inter,sans-serif;backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.1)`;
  el.innerHTML = `<span style="font-size:1rem;font-weight:700">${icons[type]}</span> ${msg}`;
  document.body.appendChild(el);
  requestAnimationFrame(() => { el.style.opacity = '1'; el.style.transform = 'translateX(-50%) translateY(0)'; });
  setTimeout(() => { el.style.opacity = '0'; el.style.transform = 'translateX(-50%) translateY(20px)'; setTimeout(() => el.remove(), 350); }, 3200);
}

// ── Navigation ────────────────────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  const target = document.getElementById(`page-${id}`);
  target.classList.remove('hidden');
  target.style.animation = 'none';
  target.offsetHeight; // trigger reflow
  target.style.animation = '';
  document.querySelectorAll('.nav-link').forEach(l => {
    l.classList.toggle('active', l.dataset.page === id);
  });
  const titles = { dashboard:'Dashboard', materials:'Materials', discover:'Discover', slides:'Revision Slides',
    flashcards:'Flashcards', quiz:'Quiz', tutor:'AI Tutor', writing:'Writing Coach', russian:'Russian', graph:'Knowledge Graph', compete:'Compete', settings:'Settings' };
  document.getElementById('page-title').textContent = titles[id] || id;
  S.page = id;
  closeMobileSidebar();   // navigating closes the small-screen drawer (no-op on desktop)
  if (id === 'dashboard')  loadDashboard();
  if (id === 'materials')  loadMaterials();
  if (id === 'discover')   initDiscoverPage();
  if (id === 'slides')     initSlidesPage();
  if (id === 'flashcards') initFcPage();
  if (id === 'quiz')       initQuizPage();
  if (id === 'tutor')      initTutorPage();
  if (id === 'writing')    initWritingPage();
  if (id === 'russian')    initRussianPage();
  if (id === 'graph')      initGraphPage();
  if (id === 'compete')    initCompetePage();
  if (id === 'settings')   initSettingsPage();
}

document.querySelectorAll('.nav-link').forEach(l => {
  l.addEventListener('click', e => { e.preventDefault(); showPage(l.dataset.page); });
});

// ── Keyboard shortcuts ────────────────────────────────────────────────────
document.addEventListener('keydown', function(e) {
  // Don't fire when user is typing in an input/textarea/select
  const tag = document.activeElement?.tagName?.toLowerCase();
  if (tag === 'input' || tag === 'textarea' || tag === 'select') return;

  // Escape dismisses transient surfaces: mobile drawer, snack, drill panel (#8/#9)
  if (e.key === 'Escape') {
    closeMobileSidebar();
    if (typeof hideClaudeSnack === 'function') hideClaudeSnack();
    const dp = document.getElementById('wr-drill-panel');
    if (dp && !dp.classList.contains('hidden')) wrCloseDrills();
  }

  // Enter/Space activates a focused flip card (div[role="button"]) — keyboard
  // parity for the flashcard and grammar-drill click targets (#8)
  if ((e.key === 'Enter' || e.code === 'Space')
      && document.activeElement?.classList?.contains('card-3d-wrap')
      && !(S.page === 'flashcards' && e.code === 'Space')) {   // Space already handled below
    e.preventDefault();
    document.activeElement.click();
    return;
  }

  // Arrow keys move between Writing tabs when a tab button has focus (#8)
  if ((e.key === 'ArrowRight' || e.key === 'ArrowLeft')
      && document.activeElement?.classList?.contains('wr-tab-btn')) {
    const tabs = ['practice', 'tips', 'wordbank', 'progress'];
    const cur = tabs.findIndex(t => document.getElementById('wr-tab-btn-' + t) === document.activeElement);
    if (cur !== -1) {
      e.preventDefault();
      const next = (cur + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
      document.getElementById('wr-tab-btn-' + tabs[next]).focus();
      wrShowTab(tabs[next]);
      return;
    }
  }

  if (S.page === 'flashcards') {
    if (e.code === 'Space' && !e.repeat) {
      e.preventDefault();
      if (!S.fcFlipped) {
        flipCard();
      } else {
        fcResult(true); // Space after reveal = mark as got it
      }
    }
    if (e.code === 'ArrowRight' && S.fcFlipped) { e.preventDefault(); fcResult(true);  }
    if (e.code === 'ArrowLeft'  && S.fcFlipped) { e.preventDefault(); fcResult(false); }
  }

  if (S.page === 'slides') {
    if (e.code === 'ArrowRight' || e.code === 'ArrowDown')  { e.preventDefault(); nextSlide(); }
    if (e.code === 'ArrowLeft'  || e.code === 'ArrowUp')    { e.preventDefault(); prevSlide(); }
  }

  // Quiz: after answering, → / Enter / Space advances to the next question.
  const qv = document.getElementById('quiz-viewer');
  if (qv && !qv.classList.contains('hidden') && S.qAnswered) {
    if (e.key === 'ArrowRight' || e.key === 'Enter' || e.code === 'Space') {
      e.preventDefault();
      nextQuestion();
    }
  }
});

// ── Dashboard ─────────────────────────────────────────────────────────────
async function loadDashboard() {
  // Personalize the welcome hero
  const welcomeEl = document.getElementById('welcome-name');
  if (welcomeEl && S.username) {
    const hour = new Date().getHours();
    const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening';
    welcomeEl.textContent = `${greeting}, ${S.username}`;
  }
  // Skeletons on first paint only (values still '—'); revisits keep live numbers
  const dashStatIds = ['stat-materials','stat-flashcards','stat-accuracy','stat-questions',
                       'srs-due-today','srs-new','srs-mature','srs-week'];
  const dashFirstLoad = document.getElementById('stat-materials')?.textContent.trim() === '—';
  if (dashFirstLoad) {
    setStatSkeletons(dashStatIds, true);
    setChartSkeleton('chart-topics', true);
    setChartSkeleton('chart-activity', true);
  }
  try {
    // Fire both calls in parallel
    const [p, s] = await Promise.all([
      api('GET', '/api/progress'),
      api('GET', '/api/srs/stats'),
    ]);

    document.getElementById('stat-materials').textContent  = p.counts.materials;
    const _onb = document.getElementById('dash-onboard');   // first-run guide when empty
    if (_onb) _onb.classList.toggle('hidden', (p.counts.materials || 0) > 0);
    document.getElementById('stat-flashcards').textContent = p.counts.flashcards;
    document.getElementById('stat-accuracy').textContent   = p.quiz.total ? p.quiz.accuracy + '%' : '—';
    document.getElementById('stat-questions').textContent  = p.quiz.total || 0;

    const topics = (p.combined_topics && p.combined_topics.length) ? p.combined_topics : p.quiz.by_topic;
    renderMaterialChart(p.by_material || []);
    renderActivityChart(p.daily, p.daily_fc || []);
    renderWeakTopics(p.weak_topics, topics);
    renderSRSStats(s);
    loadMistakes();
  } catch(e) {
    console.error(e);   // api() has already toasted the failure (#10)
  } finally {
    setStatSkeletons(dashStatIds, false);
    setChartSkeleton('chart-topics', false);
    setChartSkeleton('chart-activity', false);
  }
}

async function loadMistakes() {
  try {
    const r = await api('GET', '/api/quiz/mistakes', null, { quiet: true });
    renderMistakes(r.mistakes || []);
  } catch(e) { /* non-fatal background refresh */ }
}

function renderMistakes(mistakes) {
  const list = document.getElementById('mistakes-list');
  const badge = document.getElementById('mistakes-count');
  const retake = document.getElementById('retake-mistakes-btn');
  if (!list) return;
  S.mistakes = mistakes;  // cache for the retake quiz
  if (!mistakes.length) {
    list.innerHTML = emptyState('🎯', 'No mistakes to review', 'Miss a quiz question and it collects here for a retake.', true);
    if (badge) badge.classList.add('hidden');
    if (retake) retake.classList.add('hidden');
    return;
  }
  if (badge) { badge.textContent = mistakes.length; badge.classList.remove('hidden'); }
  if (retake) retake.classList.remove('hidden');

  const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  list.innerHTML = mistakes.map((m, i) => {
    const opts = (m.options || []).map(o => {
      const letter = (String(o).match(/^\s*([A-D])/) || [])[1];
      const isCorrect = letter && letter === (m.correct_answer || '').trim()[0];
      const isYours   = letter && letter === (m.user_answer || '').trim()[0];
      let cls = 'text-slate-500';
      let tag = '';
      if (isCorrect) { cls = 'text-green-600 font-semibold'; tag = ' ✓'; }
      else if (isYours) { cls = 'text-red-500 line-through'; tag = ' ✗ your answer'; }
      return `<div class="${cls}">${esc(o)}${tag}</div>`;
    }).join('');
    const diffColor = m.difficulty === 'hard' ? 'bg-red-100 text-red-600'
                    : m.difficulty === 'easy' ? 'bg-green-100 text-green-600'
                    : 'bg-amber-100 text-amber-600';
    return `
      <div class="border border-slate-200 rounded-lg overflow-hidden">
        <button class="w-full text-left px-4 py-3 flex items-start justify-between gap-3 hover:bg-slate-50"
                onclick="this.nextElementSibling.classList.toggle('hidden')">
          <span class="font-medium text-slate-700 flex-1">${esc(m.question)}</span>
          <span class="shrink-0 flex items-center gap-2">
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full ${diffColor}">${esc(m.difficulty || 'medium')}</span>
            <span class="text-xs text-slate-400">${esc(m.topic || '')}</span>
          </span>
        </button>
        <div class="hidden px-4 pb-4 space-y-2">
          <div class="space-y-1 text-sm">${opts}</div>
          ${m.explanation ? `<div class="text-xs text-slate-500 bg-slate-50 rounded p-3 leading-relaxed"><span class="font-semibold text-slate-600">Why:</span> ${esc(m.explanation)}</div>` : ''}
        </div>
      </div>`;
  }).join('');
}

// Take all current mistakes as a quiz. Answering one correctly logs a correct
// attempt, which removes it from the mistakes list (the endpoint excludes any
// question later answered right); miss it again and it stays.
async function startMistakesQuiz() {
  let ms = S.mistakes;
  if (!ms || !ms.length) {
    try { ms = (await api('GET', '/api/quiz/mistakes')).mistakes || []; } catch(e) { ms = []; }
  }
  if (!ms.length) { toast('No mistakes to review — nice!', 'info'); return; }

  // Map mistake rows into the quiz player's question shape.
  S.quiz = ms.map(m => ({
    id: m.question_id,
    question: m.question,
    options: m.options || [],
    correct_answer: m.correct_answer,
    topic: m.topic,
    difficulty: m.difficulty || 'medium',
    related_topics: m.related_topics || '[]',
  }));
  S.qIdx = 0; S.qCorrect = 0; S.qAnswered = false; S.quizResults = [];

  showPage('quiz');
  document.getElementById('quiz-done').classList.add('hidden');
  document.getElementById('quiz-review').classList.add('hidden');
  document.getElementById('quiz-explanation').classList.add('hidden');
  document.getElementById('quiz-empty').classList.add('hidden');
  document.getElementById('quiz-viewer').classList.remove('hidden');
  showQuestion();
  toast(`Reviewing ${S.quiz.length} mistake${S.quiz.length > 1 ? 's' : ''} — get them right to clear them`, 'info');
}

// Standalone fetch+render (used after flashcard sessions, from study-plan page, etc.)
async function loadSRSStats()      { try { renderSRSStats(await api('GET', '/api/srs/stats', null, { quiet: true })); } catch(e) {} }
async function loadExamCountdown() { try { renderExamCountdown(await api('GET', '/api/exam-dates', null, { quiet: true })); } catch(e) {} }

function renderSRSStats(s) {
  document.getElementById('srs-due-today').textContent = s.due_today;
  document.getElementById('srs-new').textContent       = s.new_cards;
  document.getElementById('srs-mature').textContent    = s.mature;
  document.getElementById('srs-week').textContent      = s.upcoming_week;
  const badge = document.getElementById('fc-due-badge');
  if (badge) {
    if (s.due_today > 0) {
      badge.textContent = `${s.due_today} card${s.due_today !== 1 ? 's' : ''} due today`;
      badge.classList.remove('hidden');
    } else {
      badge.classList.add('hidden');
    }
  }
}

function studyDueCards() {
  // Navigate to flashcards with due-only mode pre-enabled across ALL materials
  const toggle = document.getElementById('fc-due-only');
  if (toggle) toggle.checked = true;
  const sel = document.getElementById('fc-material-select');
  if (sel) sel.value = '';  // "All materials" — show due cards from everything
  showPage('flashcards');
  loadFlashcards();
}

// Trim long material names ("Module 7: Cardiovascular System | MHHS1002…") to a chip label.
function shortMaterialName(name) {
  let s = String(name || '').split('|')[0].trim();      // drop the unit-code tail
  s = s.replace(/\.(pdf|pptx|png|jpe?g)$/i, '');          // drop file extension
  if (s.length > 26) s = s.slice(0, 24) + '…';
  return s;
}

function renderMaterialChart(byMaterial) {
  const el = document.getElementById('chart-topics');
  const empty = document.getElementById('chart-topics-empty');
  const data0 = (byMaterial || []).filter(m => (m.attempts || 0) >= 1);
  if (!data0.length) {
    if (S.charts.topics) { S.charts.topics.destroy(); S.charts.topics = null; }
    empty.classList.remove('hidden');
    return;
  }
  empty.classList.add('hidden');
  if (S.charts.topics) S.charts.topics.destroy();

  // Weakest material first; show up to 8.
  const ranked = data0.slice().sort((a, b) =>
    (a.accuracy || 0) - (b.accuracy || 0) || (b.attempts || 0) - (a.attempts || 0)).slice(0, 8);
  const labels = ranked.map(m => shortMaterialName(m.material));
  const data   = ranked.map(m => Math.round((m.accuracy || 0) * 100));
  const atts   = ranked.map(m => m.attempts || 0);
  const corrs  = ranked.map(m => Number(m.correct || 0));
  const colors = data.map(v => v < 50 ? '#ef4444' : v < 75 ? '#f59e0b' : '#10b981');

  S.charts.topics = new Chart(el, {
    type: 'bar',
    data: { labels, datasets: [{ data, backgroundColor: colors, borderRadius: 6, borderSkipped: false, minBarLength: 4 }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: {
          title: items => ranked[items[0].dataIndex] ? shortMaterialName(ranked[items[0].dataIndex].material) : '',
          label: ctx => `${ctx.parsed.y}% correct  (${corrs[ctx.dataIndex]}/${atts[ctx.dataIndex]})`
        } }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 10 }, maxRotation: 30, minRotation: 0 } },
        y: { min: 0, max: 100, ticks: { callback: v => v+'%', font: { size: 11 } }, grid: { color: '#f1f5f9' } }
      }
    }
  });
}

function renderActivityChart(daily, daily_fc) {
  const el = document.getElementById('chart-activity');
  if (S.charts.activity) S.charts.activity.destroy();

  // Fill in last 7 days
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date(); d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0,10));
  }
  const qmap = {}, fcmap = {};
  (daily     || []).forEach(r => qmap[r.date]  = r);
  (daily_fc  || []).forEach(r => fcmap[r.date] = r);

  const labels   = days.map(d => new Date(d+'T12:00').toLocaleDateString('en-GB',{weekday:'short',day:'numeric'}));
  const quizAtt  = days.map(d => qmap[d]?.attempts  || 0);
  const quizCorr = days.map(d => qmap[d]?.correct   || 0);
  const fcRevs   = days.map(d => fcmap[d]?.reviews  || 0);

  // Investor/markets-style: clean thin lines, one subtle area fill under the
  // headline metric (Quiz Correct), points hidden until hover.
  const ctx2 = el.getContext('2d');
  const areaFill = () => {
    const gr = ctx2.createLinearGradient(0, 0, 0, el.height || 240);
    gr.addColorStop(0, 'rgba(8,145,178,0.16)');
    gr.addColorStop(1, 'rgba(8,145,178,0)');
    return gr;
  };
  const line = (label, data, color, opts = {}) => ({
    label, data,
    borderColor: color,
    backgroundColor: opts.fill ? areaFill() : 'transparent',
    borderWidth: opts.width || 1.6,
    tension: 0.35,
    fill: !!opts.fill,
    pointRadius: 0,
    pointHoverRadius: 4,
    pointBackgroundColor: '#fff',
    pointBorderColor: color,
    pointBorderWidth: 2,
    borderDash: opts.dashed ? [4, 4] : [],
  });

  S.charts.activity = new Chart(el, {
    type: 'line',
    data: {
      labels,
      datasets: [
        line('Quiz Correct',   quizCorr, '#0891b2', { fill: true, width: 2.2 }), // headline, filled
        line('Quiz Attempted', quizAtt,  '#94a3b8', { dashed: true }),           // faint reference
        line('Cards Reviewed', fcRevs,   '#f59e0b', {}),                          // amber line
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { font: { size: 11 }, boxWidth: 18, usePointStyle: false, padding: 16 } },
        tooltip: { mode: 'index', intersect: false, padding: 10, cornerRadius: 6,
          backgroundColor: 'rgba(15,23,42,0.92)', titleFont: { size: 11 }, bodyFont: { size: 12 },
          displayColors: false }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#94a3b8' }, border: { color: 'rgba(226,232,240,0.8)' } },
        y: { beginAtZero: true, ticks: { precision: 0, font: { size: 10 }, color: '#cbd5e1', maxTicksLimit: 5 },
             grid: { color: 'rgba(241,245,249,0.9)' }, border: { display: false } }
      }
    }
  });
}

function renderWeakTopics(weakTopics, fallbackTopics) {
  const el = document.getElementById('weak-topics-list');

  // Preferred path: the server's reliability-aware list (Laplace-smoothed,
  // min 3 attempts, already sorted weakest-first with sample-size tie-break).
  if (Array.isArray(weakTopics)) {
    if (!weakTopics.length) {
      el.innerHTML = emptyState('🧭', 'Not enough data yet', 'A topic needs at least 3 quiz attempts before it can be ranked — keep quizzing.', true);
      return;
    }
    el.innerHTML = weakTopics.slice(0, 5).map(t => {
      const pct = Math.round((t.accuracy || 0) * 100);
      const att = t.attempts || 0, corr = t.correct || 0;
      const col = pct < 50 ? 'bg-red-100 text-red-700' : pct < 75 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700';
      return `<div class="flex items-center justify-between gap-2 py-0.5">
        <span class="text-slate-600 truncate flex-1">${sEsc(t.topic)}</span>
        <span class="text-xs text-slate-400 flex-shrink-0" title="raw sample — smoothed score ${Math.round((t.smoothed_accuracy || 0) * 100)}%">${corr}/${att}</span>
        <span class="text-xs font-semibold px-2 py-0.5 rounded-full ${col} flex-shrink-0">${pct}%</span>
      </div>`;
    }).join('');
    return;
  }

  // Fallback (older API without weak_topics): raw accuracy ranking.
  const practised = (fallbackTopics || []).filter(t => (t.attempts || 0) >= 1);
  if (!practised.length) {
    el.innerHTML = emptyState('🧭', 'No quiz data yet', 'Take a few quizzes and your weak areas will surface here.', true);
    return;
  }
  const ranked = practised.slice().sort((a, b) =>
    (a.accuracy || 0) - (b.accuracy || 0) || (b.attempts || 0) - (a.attempts || 0));
  el.innerHTML = ranked.slice(0, 5).map(t => {
    const pct = Math.round((t.accuracy || 0) * 100);
    const att = t.attempts || 0, corr = t.correct || 0;
    const col = pct < 50 ? 'bg-red-100 text-red-700' : pct < 75 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700';
    return `<div class="flex items-center justify-between gap-2 py-0.5">
      <span class="text-slate-600 truncate flex-1">${sEsc(t.topic)}</span>
      <span class="text-xs text-slate-400 flex-shrink-0">${corr}/${att}</span>
      <span class="text-xs font-semibold px-2 py-0.5 rounded-full ${col} flex-shrink-0">${pct}%</span>
    </div>`;
  }).join('');
}

function renderExamCountdown(exams) {
  S.examDates = exams;
  const el = document.getElementById('exam-countdown-list');
  if (!el) return;  // card removed from the dashboard
  if (!exams || !exams.length) { el.textContent = 'No exams added yet — go to Study Plan to add one.'; return; }
  const today = new Date(); today.setHours(0,0,0,0);
  el.innerHTML = exams.slice(0,4).map(e => {
    const d = new Date(e.exam_date+'T12:00');
    const days = Math.round((d - today) / 86400000);
    const col = days < 7 ? 'text-red-600 font-bold' : days < 14 ? 'text-amber-600 font-semibold' : 'text-emerald-700 font-medium';
    return `<div class="flex items-center justify-between">
      <span class="text-slate-600">${e.subject}</span>
      <span class="${col} text-xs">${days < 0 ? 'Past' : days === 0 ? 'Today!' : days + ' days'}</span>
    </div>`;
  }).join('');
}

// ── Materials ─────────────────────────────────────────────────────────────
let _matsLastFetched = 0;

async function loadMaterials(force = false) {
  try {
    // Skip re-fetch if we already have data and it's < 10 s old (navigation cache)
    if (!force && S.materials.length && (Date.now() - _matsLastFetched) < 10000) {
      renderMaterials();
      populateMaterialSelects();
      return;
    }
    // Skeleton rows while fetching, but only on a cold cache (no flash on refresh)
    if (!S.materials.length) {
      const listEl = document.getElementById('materials-list');
      if (listEl) listEl.innerHTML = skelRows(3);
    }
    S.materials = await api('GET', '/api/materials');
    _matsLastFetched = Date.now();
    renderMaterials();
    populateMaterialSelects();
  } catch(e) {
    console.error(e);      // api() has already toasted (#10)
    renderMaterials();     // clear skeletons back to the empty state
  }
}

// Drag-and-drop state
let _dragSrc = null;

function renderMaterials() {
  const el = document.getElementById('materials-list');
  if (!S.materials.length) {
    el.innerHTML = emptyState('📚', 'No materials yet',
      'Drop a PDF or PPTX above — MedVault turns it into flashcards, quizzes and slides.');
    return;
  }

  // Group by subject, preserving sort_order within each group
  const groups = {};
  S.materials.forEach(m => {
    const subj = m.subject || 'Uncategorised';
    if (!groups[subj]) groups[subj] = [];
    groups[subj].push(m);
  });

  const icons = { pdf: '📄', pptx: '📊', image: '🖼️', web: '🌐' };

  el.innerHTML = Object.entries(groups).map(([subj, mats]) => `
    <div class="mat-group mb-4">
      <div class="flex items-center gap-2 mb-2">
        <span class="text-xs font-bold uppercase tracking-widest text-slate-400">${sEsc(subj)}</span>
        <div class="flex-1 h-px bg-slate-100"></div>
        <span class="text-xs text-slate-500">${mats.length} file${mats.length !== 1 ? 's' : ''}</span>
      </div>
      <div class="mat-group-items space-y-2" data-subject="${sEsc(subj)}">
        ${mats.map(m => materialCard(m, icons)).join('')}
      </div>
    </div>`).join('');

  // Wire up drag-and-drop for owned materials
  el.querySelectorAll('.mat-card[data-owned="true"]').forEach(card => {
    card.addEventListener('dragstart', e => {
      _dragSrc = card;
      card.classList.add('opacity-40');
      e.dataTransfer.effectAllowed = 'move';
    });
    card.addEventListener('dragend', () => {
      card.classList.remove('opacity-40');
      _dragSrc = null;
      saveMaterialOrder();
    });
    card.addEventListener('dragover', e => {
      e.preventDefault(); e.dataTransfer.dropEffect = 'move';
      if (_dragSrc && _dragSrc !== card) {
        const parent = card.parentNode;
        const cards  = [...parent.querySelectorAll('.mat-card')];
        const srcIdx = cards.indexOf(_dragSrc);
        const dstIdx = cards.indexOf(card);
        if (srcIdx < dstIdx) parent.insertBefore(_dragSrc, card.nextSibling);
        else                 parent.insertBefore(_dragSrc, card);
      }
    });
  });
}

function materialCard(m, icons) {
  const ownerTag = m.is_owner
    ? `<button class="gen-btn" onclick="toggleVisibility(${m.id}, '${m.visibility}')" title="Toggle sharing">${m.visibility === 'public' ? '🌐 Public' : '🔒 Private'}</button>`
    : `<span class="text-xs text-slate-400 italic self-center">shared by ${sEsc(m.owner_name || 'someone')}</span>`;

  const dragHandle = m.is_owner
    ? `<div class="drag-handle flex-shrink-0 cursor-grab text-slate-300 hover:text-slate-500 px-1 self-center" title="Drag to reorder">
         <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path d="M8 6a2 2 0 110-4 2 2 0 010 4zm0 8a2 2 0 110-4 2 2 0 010 4zm0 8a2 2 0 110-4 2 2 0 010 4zm8-16a2 2 0 110-4 2 2 0 010 4zm0 8a2 2 0 110-4 2 2 0 010 4zm0 8a2 2 0 110-4 2 2 0 010 4z"/></svg>
       </div>`
    : '';

  return `
  <div class="mat-card flex items-start gap-2 p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-white transition-colors"
       data-id="${m.id}" data-owned="${m.is_owner}" draggable="${m.is_owner}">
    ${dragHandle}
    <div class="text-xl flex-shrink-0 mt-0.5 select-none">${icons[m.file_type] || '📁'}</div>
    <div class="flex-1 min-w-0">
      <div class="font-medium text-slate-700 text-sm leading-snug flex items-center gap-1">
        ${m.is_owner
          ? `<span class="mat-name cursor-pointer hover:text-emerald-700" onclick="startInlineEdit(${m.id},'name',this)" title="Click to rename">${sEsc(m.original_name)}</span><svg class="w-3 h-3 text-slate-300 hover:text-emerald-600 cursor-pointer flex-shrink-0" onclick="startInlineEdit(${m.id},'name',this.previousElementSibling)" fill="none" stroke="currentColor" viewBox="0 0 24 24" title="Rename"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>`
          : `<span>${sEsc(m.original_name)}</span>`}
      </div>
      <div class="text-xs text-slate-400 mt-0.5 flex items-center gap-1 flex-wrap">
        ${m.is_owner
          ? `<span class="mat-subject cursor-pointer hover:text-emerald-700" onclick="startInlineEdit(${m.id},'subject',this)" title="Click to change category">${sEsc(m.subject)}</span><svg class="w-3 h-3 text-slate-300 hover:text-emerald-600 cursor-pointer flex-shrink-0" onclick="startInlineEdit(${m.id},'subject',this.previousElementSibling)" fill="none" stroke="currentColor" viewBox="0 0 24 24" title="Change category"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>`
          : `<span>${sEsc(m.subject)}</span>`}
        <span>· ${Math.round((m.chars||0)/1000)}k chars · ${new Date(m.uploaded_at).toLocaleDateString()}</span>
      </div>
      <div class="flex gap-2 mt-2 flex-wrap">
        <button class="gen-btn" onclick="quickGenSlides(${m.id})">Slides</button>
        <button class="gen-btn" onclick="quickGenFlashcards(${m.id})">Flashcards</button>
        <button class="gen-btn" onclick="quickGenQuiz(${m.id})">Quiz</button>
        ${ownerTag}
      </div>
    </div>
    <button onclick="deleteMaterial(${m.id})" class="text-slate-400 hover:text-red-400 transition-colors flex-shrink-0 p-1 mt-0.5" title="${m.is_owner ? 'Delete' : 'Remove from library'}" aria-label="${m.is_owner ? 'Delete material' : 'Remove material from library'}">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
    </button>
  </div>`;
}

function startInlineEdit(mid, field, spanEl) {
  const current = spanEl.textContent;
  const input = document.createElement('input');
  input.type = 'text';
  input.value = current;
  input.className = 'border border-emerald-500 rounded px-1.5 py-0.5 text-sm outline-none w-full max-w-xs';
  spanEl.replaceWith(input);
  input.focus(); input.select();

  let committed = false;  // guard against blur firing twice
  const commit = async () => {
    if (committed) return;
    committed = true;
    const val = input.value.trim() || current;
    // Nothing changed — just restore the span without a network round-trip
    if (val !== current) {
      try {
        await api('PATCH', `/api/materials/${mid}`, { [field]: val });
        const m = S.materials.find(x => x.id === mid);
        if (m) { if (field === 'name') m.original_name = val; else m.subject = val; }
        // If subject changed, re-render groups
        if (field === 'subject') { _matsLastFetched = 0; loadMaterials(true); return; }
      } catch(e) { toast(e.message, 'error'); }
    }
    // Restore span with the (possibly new) value
    const span = document.createElement('span');
    span.className = (field === 'name' ? 'mat-name' : 'mat-subject') + ' cursor-pointer hover:text-emerald-700';
    span.textContent = val;
    span.onclick = () => startInlineEdit(mid, field, span);
    span.title = field === 'name' ? 'Click to rename' : 'Click to change subject';
    input.replaceWith(span);
  };

  input.addEventListener('blur',    commit);
  input.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); input.blur(); } if (e.key === 'Escape') { input.value = current; input.blur(); } });
}

async function saveMaterialOrder() {
  // Read current DOM order and POST to backend
  const items = [];
  document.querySelectorAll('.mat-card[data-owned="true"]').forEach((card, idx) => {
    items.push({ id: parseInt(card.dataset.id), sort_order: idx });
  });
  if (!items.length) return;
  try {
    await api('POST', '/api/materials/reorder', items);
    // Update local state order
    const orderMap = Object.fromEntries(items.map(x => [x.id, x.sort_order]));
    S.materials.sort((a, b) => (orderMap[a.id] ?? 999) - (orderMap[b.id] ?? 999));
  } catch(e) { console.error('reorder failed', e); }
}

function populateMaterialSelects() {
  const selects = ['slides-material-select','fc-material-select','quiz-material-select','tutor-material-select','mm-material-select'];
  selects.forEach(id => {
    const el = document.getElementById(id);
    if (!el) return;
    const isOptional = id === 'quiz-material-select' || id === 'tutor-material-select' || id === 'fc-material-select';
    const placeholder = isOptional ? '<option value="">All materials</option>' : '<option value="">Select a material…</option>';
    // Keep existing placeholder if tutor
    if (id === 'tutor-material-select') {
      el.innerHTML = '<option value="">No context (general)</option>' +
        S.materials.map(m => `<option value="${m.id}">${m.original_name}</option>`).join('');
    } else {
      el.innerHTML = placeholder + S.materials.map(m => `<option value="${m.id}">${m.original_name}</option>`).join('');
    }
  });
}

async function deleteMaterial(id) {
  if (!confirm('Delete this material and all its generated content?')) return;
  try {
    await api('DELETE', `/api/materials/${id}`);
    toast('Material deleted', 'success');
    _matsLastFetched = 0;
    loadMaterials(true);
  } catch(e) { toast(e.message, 'error'); }
}

// Upload handling
const dropZone  = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('border-emerald-500','bg-emerald-50'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('border-emerald-500','bg-emerald-50'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('border-emerald-500','bg-emerald-50');
  handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', () => handleFiles(fileInput.files));

async function handleFiles(files) {
  const status = document.getElementById('upload-status');
  const subject = document.getElementById('upload-subject').value || 'Medicine';
  for (const file of files) {
    status.className = 'mt-3 text-sm upload-progress';
    status.classList.remove('hidden');
    status.innerHTML = `<div class="spinner" style="width:16px;height:16px;border-width:2px"></div> Uploading ${file.name}…`;
    try {
      const fd = new FormData();
      fd.append('file', file);
      fd.append('subject', subject);
      await api('POST', '/api/upload', fd);
      status.innerHTML = `✅ ${file.name} uploaded and processed!`;
      status.className = 'mt-3 text-sm text-green-600';
      toast(`${file.name} uploaded successfully`, 'success');
      _matsLastFetched = 0;
      loadMaterials(true);
    } catch(e) {
      status.innerHTML = `❌ Error: ${e.message}`;
      status.className = 'mt-3 text-sm text-red-600';
      toast(e.message, 'error');
    }
  }
  fileInput.value = '';
}

// Quick generate buttons on material cards
async function quickGenSlides(id) {
  loading(true, 'Generating revision slides…');
  try {
    const res = await api('POST', `/api/generate/slides/${id}`);
    toast(`${res.count} slides ready!`, 'success');
    showPage('slides');
    await loadMaterials();
    document.getElementById('slides-material-select').value = id;
    loadSlides(id);
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}
async function quickGenFlashcards(id) {
  loading(true, 'Generating flashcards…');
  try {
    const res = await api('POST', `/api/generate/flashcards/${id}`);
    const msg = res.existing ? `${res.count} flashcards already exist — opening now` : `${res.count} flashcards created!`;
    toast(msg, 'success');
    showPage('flashcards');
    await loadMaterials();
    document.getElementById('fc-material-select').value = id;
    loadFlashcards();
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}
async function quickGenQuiz(id) {
  loading(true, 'Generating quiz questions…');
  try { await api('POST', `/api/generate/quiz/${id}`); toast('Quiz ready!', 'success'); }
  catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

// ── Slides ────────────────────────────────────────────────────────────────
async function initSlidesPage() {
  await loadMaterials();
  const sel = document.getElementById('slides-material-select');
  if (sel.value) loadSlides(sel.value);
}

async function generateSlides(force = false) {
  const id = document.getElementById('slides-material-select').value;
  if (!id) { toast('Please select a material first', 'error'); return; }
  loading(true, force ? 'Regenerating slides with AI…' : 'Preparing slides…');
  try {
    const res = await api('POST', `/api/generate/slides/${id}${force ? '?force=true' : ''}`);
    toast(res.existing ? `${res.count} saved slides loaded (no AI used)` : `${res.count} slides generated!`,
          res.existing ? 'info' : 'success');
    loadSlides(id);
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

async function loadSlides(id) {
  if (!id) return;
  const emptyEl = document.getElementById('slides-empty');
  // Skeleton slide while fetching
  emptyEl.innerHTML = skelBlock(340, 'mt-6');
  emptyEl.classList.remove('hidden');
  try {
    S.slides = await api('GET', `/api/slides?material_id=${id}`);
    S.slideIdx = 0;
    if (S.slides.length) {
      document.getElementById('slide-viewer').classList.remove('hidden');
      emptyEl.classList.add('hidden');
      renderSlide();
    } else {
      emptyEl.innerHTML = emptyState('🖼️', 'No slides for this material yet',
        'Press “Generate Slides” above and MedVault builds a revision deck from it.');
      emptyEl.classList.remove('hidden');
      document.getElementById('slide-viewer').classList.add('hidden');
    }
  } catch(e) {
    console.error(e);   // api() has already toasted (#10)
    emptyEl.innerHTML = emptyState('🖼️', 'Couldn’t load slides', 'Check your connection and try again.');
  }
}

document.getElementById('slides-material-select')?.addEventListener('change', e => loadSlides(e.target.value));

// ── Slide renderer dispatch ───────────────────────────────────────────────
function renderSlide() {
  const s = S.slides[S.slideIdx];
  if (!s) return;
  const c = typeof s.content === 'object' ? s.content : (() => { try { return JSON.parse(s.content); } catch(e) { return {}; } })();
  const card = document.getElementById('slide-card');
  const type = c.type || 'concept';
  const renderers = { overview: slideOverview, concept: slideConcept, diagram: slideDiagram,
    comparison: slideComparison, process: slideProcess, mnemonic: slideMnemonic, clinical: slideClinical,
    stat: slideStat, keyterms: slideKeyterms, takeaway: slideTakeaway };
  card.innerHTML = (renderers[type] || slideConcept)(c);
  document.getElementById('slide-counter').textContent = `${S.slideIdx+1} / ${S.slides.length}`;
}

function prevSlide() { if (S.slideIdx > 0) { S.slideIdx--; renderSlide(); } }
function nextSlide() { if (S.slideIdx < S.slides.length-1) { S.slideIdx++; renderSlide(); } }

function sPearl(text) {
  if (!text) return '';
  return `<div class="s-pearl"><span class="s-pearl-label">Clinical Pearl</span>${sEsc(text)}</div>`;
}
function sTag(topic) {
  return topic ? `<div class="s-tag">${sEsc(topic)}</div>` : '';
}
function sEsc(t) {
  return (t||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ── Slide type renderers ──────────────────────────────────────────────────

function slideOverview(c) {
  const themes = (c.key_themes || []).map(t => `<span class="s-ov-pill">${sEsc(t)}</span>`).join('');
  return `<div class="s-overview">
    <div class="s-ov-bar"></div>
    <div class="s-ov-body">
      <div class="s-ov-eyebrow">Module Overview</div>
      <h1 class="s-ov-title">${sEsc(c.title)}</h1>
      ${c.subtitle ? `<p class="s-ov-sub">${sEsc(c.subtitle)}</p>` : ''}
      <div class="s-ov-themes">${themes}</div>
    </div>
  </div>`;
}

function slideConcept(c) {
  const points = (c.key_points || []).map(p =>
    `<li class="s-con-point"><span class="s-con-bullet">→</span><span>${sEsc(p)}</span></li>`
  ).join('');
  return `<div class="s-concept s-accent-${c.color || 'teal'}">
    <div class="s-con-header">
      <div>${sTag(c.topic)}<h2 class="s-con-title">${sEsc(c.title)}</h2></div>
      ${c.icon ? `<span class="s-con-icon">${c.icon}</span>` : ''}
    </div>
    <div class="s-con-body">
      <div class="s-con-def-col">
        <span class="s-con-def-label">Definition</span>
        <p class="s-con-def">${c.definition ? sEsc(c.definition) : 'See key points →'}</p>
      </div>
      <div class="s-con-points-col">
        <ul class="s-con-points">${points}</ul>
      </div>
    </div>
    ${c.clinical_pearl ? `<div class="s-con-pearl-wrap">${sPearl(c.clinical_pearl)}</div>` : ''}
  </div>`;
}

function slideDiagram(c) {
  let diagramContent;
  if (c.image_url) {
    // Use uploaded material image instead of generated diagram
    diagramContent = `<img src="${c.image_url}" alt="${sEsc(c.title)}"
      style="max-width:100%;max-height:230px;object-fit:contain;border-radius:10px;display:block">`;
  } else {
    diagramContent = buildHTMLDiagram(c.diagram_type, c.nodes || [], c.connections || []);
  }
  return `<div class="s-diagram">
    <div class="s-diag-header">${sTag(c.topic)}<h2 class="s-diag-title">${sEsc(c.title)}</h2></div>
    <div class="s-diag-wrap">${diagramContent}</div>
    ${c.caption ? `<p class="s-diag-caption">${sEsc(c.caption)}</p>` : ''}
    ${c.clinical_pearl ? `<div class="s-diag-pearl-wrap">${sPearl(c.clinical_pearl)}</div>` : ''}
  </div>`;
}

function slideComparison(c) {
  const L = c.left || {}, R = c.right || {};
  const lCol = L.color || 'blue', rCol = R.color || 'red';
  const lPoints = (L.points || []).map(p => `<li><span class="s-cmp-dot">•</span>${sEsc(p)}</li>`).join('');
  const rPoints = (R.points || []).map(p => `<li><span class="s-cmp-dot">•</span>${sEsc(p)}</li>`).join('');
  return `<div class="s-comparison">
    <div class="s-cmp-header">${sTag(c.topic)}<h2 class="s-cmp-title">${sEsc(c.title)}</h2></div>
    <div class="s-cmp-cols">
      <div class="s-cmp-col s-cmp-col-${lCol}">
        <div class="s-cmp-col-head"><span class="s-cmp-col-label">${sEsc(L.label || 'A')}</span></div>
        <div class="s-cmp-col-body"><ul class="s-cmp-list">${lPoints}</ul></div>
      </div>
      <div class="s-cmp-col s-cmp-col-${rCol}">
        <div class="s-cmp-col-head"><span class="s-cmp-col-label">${sEsc(R.label || 'B')}</span></div>
        <div class="s-cmp-col-body"><ul class="s-cmp-list">${rPoints}</ul></div>
      </div>
    </div>
    ${c.key_difference ? `<div class="s-cmp-diff">💡 ${sEsc(c.key_difference)}</div>` : ''}
  </div>`;
}

function slideProcess(c) {
  const steps = c.steps || [];
  const stepCards = steps.map((s, i) => `
    <div class="s-proc-step">
      <div class="s-proc-step-num">${s.number || i+1}</div>
      <div class="s-proc-step-body">
        <div class="s-proc-step-title">${sEsc(s.title || '')}</div>
        ${s.description ? `<div class="s-proc-step-desc">${sEsc(s.description)}</div>` : ''}
      </div>
    </div>`
  ).join('');
  return `<div class="s-process">
    <div class="s-proc-header">${sTag(c.topic)}<h2 class="s-proc-title">${sEsc(c.title)}</h2></div>
    <div class="s-proc-steps">${stepCards}</div>
    ${c.clinical_pearl ? `<div class="s-proc-pearl-wrap">${sPearl(c.clinical_pearl)}</div>` : ''}
  </div>`;
}

function slideMnemonic(c) {
  const letters = (c.expansion || []).map(e => {
    const letter = e.letter || (e.meaning||'')[0] || '?';
    return `<div class="s-mn-row">
      <span class="s-mn-letter">${sEsc(letter)}</span>
      <span class="s-mn-meaning">${sEsc(e.meaning || '')}</span>
    </div>`;
  }).join('');
  return `<div class="s-mnemonic">
    <div class="s-mn-top">
      <div class="s-mn-context-box">
        <span class="s-mn-context-label">${sEsc(c.topic || 'Mnemonic')}</span>
        <p class="s-mn-context-text">${c.context ? sEsc(c.context) : 'Use this mnemonic to remember the key terms below.'}</p>
      </div>
      <div class="s-mn-word-box"><div class="s-mn-word">${sEsc(c.mnemonic || '')}</div></div>
    </div>
    <div class="s-mn-grid">${letters}</div>
  </div>`;
}

function slideClinical(c) {
  return `<div class="s-clinical">
    <div class="s-clin-header">${sTag(c.topic)}<h2 class="s-clin-title">${sEsc(c.title)}</h2></div>
    ${c.scenario ? `<div class="s-clin-case"><span class="s-clin-case-label">Clinical Case</span>${sEsc(c.scenario)}</div>` : ''}
    <div class="s-clin-qa">
      <div class="s-clin-q-box">
        <span class="s-clin-qa-label">Question</span>
        <p>${c.question ? sEsc(c.question) : ''}</p>
      </div>
      <div class="s-clin-a-box">
        <span class="s-clin-qa-label">Answer</span>
        <p>${c.answer ? sEsc(c.answer) : ''}</p>
      </div>
    </div>
    ${c.teaching_point ? `<div class="s-clin-teaching">💡 ${sEsc(c.teaching_point)}</div>` : ''}
  </div>`;
}

function slideStat(c) {
  const list = (c.stats || []).slice(0, 4);
  const cells = list.map(s => `
    <div class="s-stat-cell">
      <div class="s-stat-value">${sEsc(s.value || '')}${s.unit ? `<span class="s-stat-unit">${sEsc(s.unit)}</span>` : ''}</div>
      <div class="s-stat-label">${sEsc(s.label || '')}</div>
      ${s.note ? `<div class="s-stat-note">${sEsc(s.note)}</div>` : ''}
    </div>`).join('');
  return `<div class="s-stat">
    <div class="s-stat-header">${sTag(c.topic)}<h2 class="s-stat-title">${sEsc(c.title)}</h2></div>
    <div class="s-stat-grid s-stat-n${list.length}">${cells}</div>
    ${c.clinical_pearl ? `<div class="s-stat-pearl-wrap">${sPearl(c.clinical_pearl)}</div>` : ''}
  </div>`;
}

function slideKeyterms(c) {
  const rows = (c.terms || []).slice(0, 6).map(t => `
    <div class="s-kt-row">
      <div class="s-kt-term">${sEsc(t.term || '')}</div>
      <div class="s-kt-def">${sEsc(t.definition || '')}</div>
    </div>`).join('');
  return `<div class="s-keyterms">
    <div class="s-kt-header">${sTag(c.topic)}<h2 class="s-kt-title">${sEsc(c.title)}</h2></div>
    <div class="s-kt-list">${rows}</div>
  </div>`;
}

function slideTakeaway(c) {
  const points = (c.points || []).map(p =>
    `<li class="s-ta-point"><span class="s-ta-check">✓</span><span>${sEsc(p)}</span></li>`).join('');
  return `<div class="s-takeaway">
    <div class="s-ta-eyebrow">${sEsc(c.topic || 'High-Yield')}</div>
    <h2 class="s-ta-title">${sEsc(c.title)}</h2>
    ${c.headline ? `<p class="s-ta-headline">${sEsc(c.headline)}</p>` : ''}
    <ul class="s-ta-points">${points}</ul>
  </div>`;
}

// ── HTML diagram builders (replaces SVG — no character limits, reflowable) ──
// Clean, vivid palette — every colour is dark enough for crisp white text
const DIAG_COLORS = ['#4f46e5','#0284c7','#0d9488','#059669','#d97706','#dc2626','#7c3aed','#db2777'];

function buildHTMLDiagram(type, nodes, connections) {
  if (!nodes.length) return '<p class="s-diag-empty">No diagram data</p>';
  if (type === 'cycle')     return htmlCycle(nodes);
  if (type === 'hierarchy') return htmlHierarchy(nodes, connections);
  return htmlFlow(nodes, connections); // flow, process, default
}

function htmlFlow(nodes, connections) {
  const items = nodes.slice(0, 8);
  // Build sequential connection map from explicit connections or default left→right
  const connSet = new Set();
  if (connections.length) {
    connections.forEach(c => connSet.add(c.from + '→' + c.to));
  } else {
    items.slice(0,-1).forEach((n,i) => connSet.add(n.id + '→' + items[i+1].id));
  }
  let html = '<div class="s-diag-flow">';
  items.forEach((nd, i) => {
    const col = DIAG_COLORS[i % DIAG_COLORS.length];
    html += `<div class="s-diag-flow-node">
      <div class="s-diag-node-pill" style="--nc:${col}">
        <div class="s-diag-node-label">${sEsc(nd.label || '')}</div>
        ${nd.description ? `<div class="s-diag-node-desc">${sEsc(nd.description)}</div>` : ''}
      </div>
      ${nd.sub ? `<div class="s-diag-node-sub">${sEsc(nd.sub)}</div>` : ''}
    </div>`;
    if (i < items.length - 1) {
      html += '<div class="s-diag-conn">→</div>';
    }
  });
  html += '</div>';
  return html;
}

function htmlCycle(nodes) {
  const items = nodes.slice(0, 7);
  let html = '<div class="s-diag-flow" style="flex-wrap:wrap">';
  items.forEach((nd, i) => {
    const col = DIAG_COLORS[i % DIAG_COLORS.length];
    html += `<div class="s-diag-flow-node">
      <div class="s-diag-node-pill" style="--nc:${col}">
        <div class="s-diag-node-label">${sEsc(nd.label || '')}</div>
        ${nd.description ? `<div class="s-diag-node-desc">${sEsc(nd.description)}</div>` : ''}
      </div>
    </div>`;
    if (i < items.length - 1) {
      html += '<div class="s-diag-conn">→</div>';
    } else {
      html += '<div class="s-diag-conn s-diag-conn-cycle" title="cycles back">↺</div>';
    }
  });
  html += '</div>';
  return html;
}

function htmlHierarchy(nodes, connections) {
  if (!connections.length) return htmlFlow(nodes, connections);
  // Build parent→children map
  const childMap = {};
  nodes.forEach(n => { childMap[n.id] = []; });
  const hasParent = new Set();
  connections.forEach(c => {
    if (childMap[c.from] !== undefined) childMap[c.from].push(c.to);
    hasParent.add(c.to);
  });
  const root = nodes.find(n => !hasParent.has(n.id)) || nodes[0];
  if (!root) return htmlFlow(nodes, connections);
  const nodeMap = {};
  nodes.forEach(n => { nodeMap[n.id] = n; });
  const rootCol = DIAG_COLORS[0];
  let html = `<div class="s-diag-hier">
    <div class="s-diag-hier-root">
      <div class="s-diag-node-pill" style="--nc:${rootCol}">
        <div class="s-diag-node-label">${sEsc(root.label || '')}</div>
        ${root.description ? `<div class="s-diag-node-desc">${sEsc(root.description)}</div>` : ''}
      </div>
    </div>
    <div class="s-diag-hier-children">`;
  (childMap[root.id] || []).forEach((cid, ci) => {
    const child = nodeMap[cid];
    if (!child) return;
    const col = DIAG_COLORS[(ci + 1) % DIAG_COLORS.length];
    html += `<div class="s-diag-hier-child">
      <div class="s-diag-node-pill" style="--nc:${col}">
        <div class="s-diag-node-label">${sEsc(child.label || '')}</div>
        ${child.description ? `<div class="s-diag-node-desc">${sEsc(child.description)}</div>` : ''}
      </div>`;
    // Grandchildren
    const grandchildren = childMap[cid] || [];
    if (grandchildren.length) {
      html += '<div style="display:flex;flex-direction:column;gap:5px;margin-top:6px;padding-left:10px;border-left:2px solid #e2e8f0;">';
      grandchildren.forEach((gcid, gi) => {
        const gc = nodeMap[gcid];
        if (!gc) return;
        const gcCol = DIAG_COLORS[(ci + gi + 2) % DIAG_COLORS.length];
        html += `<div class="s-diag-node-pill" style="--nc:${gcCol};font-size:.75rem;">
          <div class="s-diag-node-label">${sEsc(gc.label || '')}</div>
          ${gc.description ? `<div class="s-diag-node-desc">${sEsc(gc.description)}</div>` : ''}
        </div>`;
      });
      html += '</div>';
    }
    html += '</div>';
  });
  html += '</div></div>';
  return html;
}

// ── Flashcards ────────────────────────────────────────────────────────────
async function initFcPage() { await loadMaterials(); }

async function generateFlashcards(force = false) {
  const id = document.getElementById('fc-material-select').value;
  if (!id) { toast('Please select a material first', 'error'); return; }
  loading(true, force ? 'Regenerating flashcards with AI…' : 'Loading flashcards…');
  try {
    const res = await api('POST', `/api/generate/flashcards/${id}${force ? '?force=true' : ''}`);
    if (res.existing) {
      toast(`${res.count} flashcards loaded`, 'info');
    } else {
      toast(`${res.count} flashcards created!`, 'success');
    }
    loadFlashcards();
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

async function loadFlashcards() {
  const id       = document.getElementById('fc-material-select').value;
  const adap     = document.getElementById('fc-adaptive').checked;
  const dueOnly  = document.getElementById('fc-due-only').checked;
  if (!id && !dueOnly) { loadSRSStats(); return; }
  const viewer = document.getElementById('fc-viewer');
  const empty  = document.getElementById('fc-empty');
  // Skeleton card while fetching
  empty.innerHTML = skelBlock(300, 'mt-8');
  empty.classList.remove('hidden');
  viewer.classList.add('hidden');
  try {
    const params = (id ? `material_id=${id}&` : '') + `adaptive=${adap}&due_only=${dueOnly}`;
    S.flashcards = await api('GET', `/api/flashcards?${params}`);
    S.fcIdx = 0; S.fcCorrect = 0; S.fcFlipped = false;
    S.fcDueOnly = dueOnly;
    if (S.flashcards.length) {
      viewer.classList.remove('hidden'); empty.classList.add('hidden');
      document.getElementById('fc-done').classList.add('hidden');
      showFlashcard();
    } else {
      empty.innerHTML = dueOnly
        ? emptyState('✅', 'All caught up!', 'No cards are due right now — come back later, or untick “Due only” to review everything.')
        : emptyState('🃏', 'No flashcards yet', 'Press “Generate Cards” above to build a deck from this material.');
      empty.classList.remove('hidden'); viewer.classList.add('hidden');
    }
    loadSRSStats();
  } catch(e) {
    console.error(e);   // api() has already toasted (#10)
    empty.innerHTML = emptyState('🃏', 'Couldn’t load flashcards', 'Check your connection and try again.');
  }
}

document.getElementById('fc-material-select')?.addEventListener('change', loadFlashcards);
document.getElementById('fc-adaptive')?.addEventListener('change', loadFlashcards);
document.getElementById('fc-due-only')?.addEventListener('change', loadFlashcards);
document.getElementById('quiz-material-select')?.addEventListener('change', startQuiz);

function showFlashcard() {
  if (S.fcIdx >= S.flashcards.length) { showFcDone(); return; }
  // Ensure card wrap is visible and done screen is hidden
  document.getElementById('fc-done').classList.add('hidden');
  document.getElementById('card-3d').parentElement.classList.remove('hidden');
  const c = S.flashcards[S.fcIdx];
  document.getElementById('fc-topic').textContent    = c.topic || 'General';
  document.getElementById('fc-question').textContent = c.question;
  // Render chemical structure on question side if available
  renderSmilesInEl(c.smiles, document.getElementById('fc-question').parentElement, 'append');
  document.getElementById('fc-answer').textContent   = c.answer;
  // Show related topics if available
  let relEl = document.getElementById('fc-related');
  if (!relEl) {
    relEl = document.createElement('div');
    relEl.id = 'fc-related';
    relEl.className = 'text-xs mt-2 text-emerald-700';
    document.getElementById('fc-answer').parentElement.appendChild(relEl);
  }
  let related = [];
  try { related = typeof c.related_topics === 'string' ? JSON.parse(c.related_topics) : (c.related_topics || []); } catch(e) {}
  relEl.innerHTML = related.length ? '🔗 Related: ' + related.map(r => `<span class="inline-block bg-emerald-50 border border-emerald-200 rounded px-1.5 py-0.5 mr-1">${sEsc(r)}</span>`).join('') : '';
  document.getElementById('fc-result-btns').classList.add('hidden');
  document.getElementById('card-3d').classList.remove('flipped');
  S.fcFlipped = false;
  const done = S.fcIdx;
  const total = S.flashcards.length;
  document.getElementById('fc-progress-text').textContent  = `Card ${done+1} of ${total}`;
  document.getElementById('fc-accuracy-text').textContent  = done ? `${Math.round(S.fcCorrect/done*100)}% correct` : '';
  document.getElementById('fc-progress-bar').style.width   = `${(done/total)*100}%`;
}

function restartFlashcards() {
  S.fcIdx = 0; S.fcCorrect = 0; S.fcFlipped = false;
  showFlashcard();
}

function flipCard() {
  if (S.fcIdx >= S.flashcards.length) return;
  document.getElementById('card-3d').classList.toggle('flipped');
  S.fcFlipped = !S.fcFlipped;
  if (S.fcFlipped) document.getElementById('fc-result-btns').classList.remove('hidden');
}

async function fcResult(correct) {
  const card = S.flashcards[S.fcIdx];
  if (correct) S.fcCorrect++;
  try { await api('POST', `/api/flashcards/${card.id}/result`, { correct }, { quiet: true }); } catch(e) {}
  S.fcIdx++;
  showFlashcard();
}

function showFcDone() {
  document.getElementById('fc-done').classList.remove('hidden');
  document.getElementById('card-3d').parentElement.classList.add('hidden');
  document.getElementById('fc-result-btns').classList.add('hidden');
  const pct = S.flashcards.length ? Math.round(S.fcCorrect/S.flashcards.length*100) : 0;
  const scoreText = `You got ${S.fcCorrect} / ${S.flashcards.length} correct (${pct}%)`;
  const srsNote = S.fcDueOnly
    ? ' · Cards scheduled for spaced review — check back tomorrow for your next batch.'
    : ' · Answer cards to schedule them for spaced review.';
  document.getElementById('fc-final-score').textContent = scoreText + srsNote;
  loadSRSStats(); // refresh dashboard queue counts
}

// ── GAMSAT Writing coach ──────────────────────────────────────────────────
const WR = { task:'A', stimulus:null, timer:null, timerLeft:0, timerPhase:null,
             drills:[], drillIdx:0, progressLoaded:false };

function wrEsc(s) { const d = document.createElement('div'); d.textContent = s == null ? '' : String(s); return d.innerHTML; }

async function initWritingPage() {
  if (!WR.stimulus) await wrLoadStimulus(false);
  wrRefreshStats();
}

// Practice ↔ Tips ↔ Progress tabs (Tips is static; Progress lazy-loads on first open)
function wrShowTab(tab) {
  ['practice', 'tips', 'wordbank', 'progress'].forEach(t => {
    document.getElementById('wr-tab-' + t).classList.toggle('hidden', t !== tab);
    const btn = document.getElementById('wr-tab-btn-' + t);
    btn.classList.toggle('active', t === tab);
    btn.setAttribute('aria-selected', t === tab ? 'true' : 'false');
  });
  if (tab === 'progress' && !WR.progressLoaded) wrLoadProgress();
  if (tab === 'wordbank' && !WB.inited) wbInit();
  if (tab === 'tips') wrLoadPersonalTips();   // refresh each open — cheap, reads stats
}

/* ══════════════════════════════════════════════════════════════
   WORD BANK — personal vocabulary + browser speech (zero-API)
   ══════════════════════════════════════════════════════════════ */
const WB = { inited: false, active: 'all', voice: null, saved: [] };

const WB_CATS = {
  vocab:      { name: 'Vocabulary',         color: '#6366f1' },
  philosophy: { name: 'Philosophy',         color: '#0ea5a4' },
  grammar:    { name: 'Grammar & usage',    color: '#d97706' },
  synonyms:   { name: 'Synonym banks',      color: '#db2777' },
  idioms:     { name: 'Idioms & phrases',   color: '#7c3aed' },
  archaic:    { name: 'Archaic & literary', color: '#c2582a' },
};

// [category, word, part-of-speech, definition, example]
const WB_WORDS = [
  ['vocab','antithetical','adj.','Directly opposed; mutually incompatible','His actions were antithetical to everything he claimed to value.'],
  ['vocab','schadenfreude','noun','Pleasure derived from another’s misfortune','There’s a streak of schadenfreude in how the novel treats its villains.'],
  ['vocab','poignant','adj.','Evoking a keen sense of sadness or regret','The ending lands poignantly, without tipping into sentimentality.'],
  ['vocab','exasperated','adj.','Intensely irritated and frustrated','Nick grows exasperated with the Buchanans’ carelessness.'],
  ['vocab','primordial','adj.','Existing from the very beginning; primeval','The poem reaches for something primordial in human longing.'],
  ['vocab','paradigm','noun','A typical example or model; a framework of thought','Gatsby is the paradigm of the self-made American.'],
  ['vocab','discernment','noun','The ability to judge well; keen insight','Her essays show real discernment about tone.'],
  ['vocab','substantive','adj.','Having real importance or solid basis; not superficial','A substantive argument, not just stylistic flourish.'],
  ['vocab','eschew','verb','To deliberately avoid or abstain from','The writer eschews cliché in favour of fresh imagery.'],
  ['vocab','reciprocity','noun','Mutual exchange; giving and receiving in kind','Love, for Nozick, depends on reciprocity.'],
  ['vocab','deride','verb','To mock or ridicule','Critics derided the sequel as hollow.'],
  ['vocab','capitulate','verb','To surrender or give in','She refused to capitulate to the pressure.'],
  ['vocab','hegemonic','adj.','Relating to dominance of one group or idea over others','A hegemonic cultural narrative.'],
  ['vocab','martyr','noun','One who suffers for a cause; (fig.) one who plays the victim','He cast himself as a martyr to the family’s expectations.'],
  ['vocab','apotheosis','noun','The highest point; elevation to divine status','The final act is the apotheosis of Gatsby’s dream.'],
  ['vocab','pariah','noun','A social outcast','After the scandal he became a pariah.'],
  ['vocab','cynical','adj.','Distrustful of others’ motives; sceptical of sincerity','A cynical view of the “American Dream.”'],
  ['vocab','facade','noun','An outward appearance masking reality','Their marriage was a facade of respectability.'],
  ['vocab','edifice','noun','A large building; (fig.) a complex system of ideas','The whole edifice of his self-image collapses.'],
  ['vocab','mirage','noun','An illusion; something that appears real but isn’t','The green light is a mirage of the future.'],
  ['vocab','meandering','adj.','Wandering aimlessly; indirect','A meandering plot that never quite commits.'],
  ['vocab','immolate','verb','To sacrifice or destroy, especially by fire','He all but immolates himself for an unworthy ideal.'],
  ['vocab','unrequited','adj.','(Of love) not returned','Unrequited longing drives the whole narrative.'],
  ['vocab','debilitated','adj.','Weakened; drained of strength','A debilitated sense of purpose.'],
  ['vocab','obsolete','adj.','No longer in use; outdated','Values the modern world has rendered obsolete.'],
  ['vocab','patently','adv.','Clearly, obviously','A patently false claim.'],
  ['vocab','tangible','adj.','Perceptible by touch; real and concrete','No tangible evidence, only atmosphere.'],
  ['vocab','rebuttal','noun','A refutation; a counter-argument','Her rebuttal dismantled the opposing case.'],
  ['vocab','contention','noun','An assertion in an argument; or a dispute','My central contention is that…'],
  ['vocab','contingent','adj.','Dependent on; subject to chance','Happiness contingent on wealth is fragile.'],
  ['vocab','commensurate','adj.','Proportionate to; matching in size or degree','A reward commensurate with the effort.'],
  ['vocab','incomparable','adj.','Beyond comparison; unequalled','An incomparable prose stylist.'],
  ['vocab','analogous','adj.','Comparable in some respect','The two images are analogous in function.'],
  ['vocab','construe','verb','To interpret or understand in a particular way','His silence can be construed as guilt.'],
  ['vocab','confer','verb','To grant or bestow','Wealth confers status but not virtue.'],
  ['vocab','pertain','verb','To relate or be relevant to','Evidence pertaining to the theme of decay.'],
  ['vocab','elicit','verb','To draw out (a response or reaction)','The scene elicits genuine pity.'],
  ['vocab','aggregation','noun','A collection or clustering into a whole','An aggregation of small betrayals.'],
  ['vocab','litigation','noun','The process of taking legal action','The dispute ended in litigation.'],
  ['vocab','survivorship','noun','The state of surviving; (bias) judging only survivors','Survivorship bias skews the sample.'],
  ['vocab','compassion fatigue','noun','Emotional exhaustion from prolonged caring','Nurses often describe compassion fatigue.'],
  ['vocab','gentrification','noun','Renovation of a district that displaces poorer residents','The suburb’s gentrification erased its character.'],
  ['vocab','bittersweet','adj.','Both pleasant and painful at once','A bittersweet farewell.'],
  ['vocab','actuated','verb','Set in motion; motivated','Actuated by envy rather than principle.'],
  ['vocab','collated','verb','Collected and arranged in order','She collated the sources into one document.'],
  ['vocab','covert','adj.','Hidden; secret (opposite of overt)','A covert threat beneath an overt politeness.'],
  ['vocab','overt','adj.','Open and observable; not hidden','His overt hostility surprised no one.'],
  ['philosophy','eros','noun','Passionate, desiring love (Greek). Classical loves: eros (desire), agape (selfless), philia (friendship), storge (familial).',''],
  ['philosophy','fungible','adj.','Replaceable by an identical unit (money is fungible). Nozick: love treats the beloved as non-fungible.',''],
  ['philosophy','non-fungible','adj.','Unique, not interchangeable — the opposite of fungible.',''],
  ['philosophy','teleological','adj.','Explained by purpose or end-goal (telos = end).',''],
  ['philosophy','ontological','adj.','Concerning the nature of being and existence.',''],
  ['philosophy','epistemic','adj.','Relating to knowledge and justified belief.',''],
  ['philosophy','phenomenology','noun','The study of experience as it appears to consciousness.',''],
  ['philosophy','conative','adj.','Relating to will, striving, or desire (vs cognitive/affective).',''],
  ['philosophy','desiderative','adj.','Expressing desire or wanting.',''],
  ['philosophy','volitional','adj.','Relating to the will; done by conscious choice.',''],
  ['philosophy','dispositional','adj.','A tendency to behave a certain way (vs occurrent = happening now).',''],
  ['philosophy','occurrent','adj.','Actively occurring in the moment (contrast dispositional).',''],
  ['philosophy','instantiated','verb','Made concrete; represented by an actual instance.',''],
  ['philosophy','pro tanto','phrase','“To that extent” — a reason with some weight, not decisive.',''],
  ['philosophy','arational','adj.','Outside the scope of reason (neither rational nor irrational).',''],
  ['philosophy','genetic fallacy','noun','Judging a claim by its origin rather than its merit.',''],
  ['philosophy','ressentiment','noun','(Nietzsche) reassigning blame for one’s frustration; moralised envy.',''],
  ['philosophy','mitleid','noun','German: “pity/compassion” — a concept Nietzsche critiques.',''],
  ['philosophy','socratic','adj.','By questioning and dialogue (the Socratic method).',''],
  ['philosophy','techne','noun','Greek: craft, skill, art (tekhne).',''],
  ['philosophy','panspermia','noun','Theory that life spread through the universe via space debris.',''],
  ['grammar','compound sentence','','Two independent clauses joined by a coordinating conjunction.','Gatsby believed in the green light, but the dream was already behind him.'],
  ['grammar','FANBOYS','','The coordinating conjunctions.','For, And, Nor, But, Or, Yet, So.'],
  ['grammar','gerund','','An -ing verb used as a noun.','Reading is fun.'],
  ['grammar','participle','','Verb form used as an adjective; past participle = broken, written, gone.','the running water / a broken promise'],
  ['grammar','infinitive phrase','','to + verb functioning as noun/adjective/adverb.','To succeed was her only goal.'],
  ['grammar','linking vs helping verbs','','Linking connects subject to description (is, seem); helping supports the main verb (have, will).',''],
  ['grammar','syntax','','The arrangement of words into sentences.',''],
  ['grammar','syntactic vs semantic','','Structure/grammar vs meaning.',''],
  ['grammar','morphological','','Relating to word forms and their parts (morphemes).',''],
  ['grammar','diction','','Word choice; a particular vocabulary or way of speaking (parlance).',''],
  ['grammar','oxford comma','','The comma before “and” in a list.','a, b, and c'],
  ['grammar','methodology vs method','','The study/rationale of methods vs the method itself.',''],
  ['grammar','whom vs who','','whom = object (to whom); who = subject.','To whom did you speak? / Who called?'],
  ['grammar','although vs though','','Interchangeable as conjunctions; though can also end a sentence.','It was hard. I finished, though.'],
  ['grammar','brought vs bought','','brought = carried (bring); bought = purchased (buy).',''],
  ['idioms','peas in a pod','','Extremely alike, inseparable.','Tom and Daisy are peas in a pod — careless people who retreat into their money.'],
  ['idioms','in concert','','Acting together, in coordination.','The images work in concert to build a mood of decay.'],
  ['idioms','inclement weather','','Harsh, stormy weather (formal).','The reunion opens in inclement weather — rain mirroring Gatsby’s nerves.'],
  ['idioms','followed suit','','Did the same thing as someone else.','One critic praised it; the rest followed suit.'],
  ['idioms','cold shoulder','','Deliberate coldness or snubbing.','She gave him the cold shoulder all evening.'],
  ['idioms','catch a stray','','(slang) Get hit by an insult not aimed at you.',''],
  ['idioms','u-turn','','A complete reversal of position or policy.','The government did a u-turn on the policy.'],
  ['archaic','thy','','Your (archaic, singular); thine = yours.','thy kingdom come'],
  ['archaic','thou','','You (archaic, singular subject); thee = object form.',''],
  ['archaic','lest','','For fear that; in case.','lest we forget'],
  ['archaic','indited','','Composed or wrote (a poem/letter) — NOT indicted (charged with a crime).','He indited a sonnet to his beloved.'],
  ['archaic','kindred','','Similar in nature; one’s relatives.','a kindred spirit'],
  ['archaic','alchemist','','Medieval chemist seeking to turn metal to gold; (fig.) a transformer.',''],
  ['archaic','verbatim','','Word for word, exactly as spoken or written.',''],
  ['archaic','lexicon','','The vocabulary of a language, person, or field.',''],
];

const WB_SYNS = [
  ['restricted / restrained / controlled','constrained, curtailed, circumscribed, confined, checked, reined in'],
  ['strength / hardness','fortitude, robustness, resilience, tenacity, potency'],
  ['busy','occupied, engaged, swamped, preoccupied, industrious'],
  ['enthusiastic','ardent, fervent, keen, zealous, eager'],
  ['although','though, even if, notwithstanding, albeit, granted that'],
  ['fundamentally','essentially, intrinsically, at its core, in essence'],
  ['initiate / establish','institute, inaugurate, set in motion, found, instigate'],
  ['created','forged, fashioned, generated, produced, conceived'],
  ['promoting','fostering, advancing, championing, cultivating, bolstering'],
  ['providing','furnishing, supplying, affording, yielding, granting'],
  ['reducing','diminishing, curtailing, attenuating, mitigating, tempering'],
  ['consolidated','unified, merged, cemented, fortified, integrated'],
  ['thankfully','mercifully, fortunately, gratifyingly'],
  ['routine','habitual, customary, methodical, workaday'],
  ['endeavour','strive, undertake, aspire, venture'],
  ['confused','bewildered, disoriented, perplexed, flummoxed, muddled'],
  ['meaningless','hollow, vacuous, futile, empty, inconsequential'],
  ['interest','fascination, curiosity, engagement, preoccupation'],
  ['comparable','analogous, equivalent, akin, commensurate, parallel'],
  ['monopoly / powerhouse','stronghold, juggernaut, dominion, hegemony'],
  ['underdog','outsider, long shot, dark horse'],
  ['hagiography','idealised biography, uncritical praise, whitewash'],
  ['obsolete','outmoded, antiquated, defunct, superseded'],
  ['recoils','flinches, shrinks back, winces, retreats'],
];

// Built-in seed, in the uniform [cat, word, pos, def, example] shape.
// A 6th element (id) marks a user-saved word so it gets a delete button.
const WB_SEED = WB_WORDS.concat(WB_SYNS.map(([k, v]) => ['synonyms', k, '', v, '']));
let WB_ALL = WB_SEED.slice();

// Rebuild WB_ALL from the seed plus the user's saved words (fetched from the DB).
function wbMergeSaved() {
  const savedRows = WB.saved.map(r => [
    r.category || 'vocab', r.word, r.pos || '', r.definition || '', r.example || '', r.id,
  ]);
  WB_ALL = savedRows.concat(WB_SEED);   // user words first within each category
}

async function wbLoadSaved() {
  try {
    const res = await api('GET', '/api/wordbank', null, { quiet: true });
    WB.saved = Array.isArray(res.words) ? res.words : [];
  } catch (e) { WB.saved = []; }   // offline / not-logged-in → seed only
  wbMergeSaved();
}

function wbInit() {
  WB.inited = true;
  // filter chips
  const fx = document.getElementById('wb-filters');
  const mk = (id, label) => {
    const c = document.createElement('button');
    c.className = 'wb-chip' + (id === 'all' ? ' on' : '');
    c.textContent = label;
    c.dataset.cat = id;
    c.onclick = () => {
      WB.active = id;
      document.querySelectorAll('.wb-chip').forEach(x => x.classList.toggle('on', x.dataset.cat === id));
      wbRender();
    };
    fx.appendChild(c);
  };
  mk('all', 'All');
  Object.entries(WB_CATS).forEach(([id, c]) => mk(id, c.name));
  // voices load asynchronously in most browsers
  wbPickVoice();
  if (window.speechSynthesis) speechSynthesis.onvoiceschanged = wbPickVoice;
  wbRender();                       // render the seed immediately
  wbLoadSaved().then(wbRender);     // then merge in the user's saved words
}

function wbPickVoice() {
  if (!window.speechSynthesis) return;
  const voices = speechSynthesis.getVoices();
  const wantAU = document.getElementById('wb-uk-voice')?.checked;   // toggle → AU/UK
  WB.voice =
    (wantAU && (voices.find(v => v.name === 'Karen') ||
                voices.find(v => v.name === 'Daniel') ||
                voices.find(v => /en-AU|en-GB/i.test(v.lang)))) ||
    voices.find(v => v.name === 'Samantha') ||   // default: clear US voice
    voices.find(v => /^en[-_]US/i.test(v.lang)) ||
    voices.find(v => /^en/i.test(v.lang)) || null;
}

function wbSpeak(word, btn) {
  if (!window.speechSynthesis) { toast('Speech not supported in this browser', 'error'); return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(word);
  if (WB.voice) u.voice = WB.voice;
  u.rate = 0.9;
  if (btn) { btn.classList.add('speaking'); u.onend = u.onerror = () => btn.classList.remove('speaking'); }
  speechSynthesis.speak(u);
}

async function wbDelete(id) {
  try {
    await api('DELETE', '/api/wordbank/' + id);
    WB.saved = WB.saved.filter(r => r.id !== id);
    wbMergeSaved();
    wbRender();
    toast('Word removed', 'success');
  } catch (e) { /* api() already surfaces the error */ }
}

function wbHl(s, q) {
  const e = wrEsc(s);
  if (!q) return e;
  const i = s.toLowerCase().indexOf(q);
  if (i < 0) return e;
  return wrEsc(s.slice(0, i)) + '<mark>' + wrEsc(s.slice(i, i + q.length)) + '</mark>' + wrEsc(s.slice(i + q.length));
}

function wbRender() {
  const q = (document.getElementById('wb-search').value || '').trim().toLowerCase();
  const content = document.getElementById('wb-content');
  content.innerHTML = '';
  let shown = 0;
  Object.entries(WB_CATS).forEach(([cat, meta]) => {
    if (WB.active !== 'all' && WB.active !== cat) return;
    const items = WB_ALL.filter(w => w[0] === cat &&
      (!q || (w[1] + ' ' + w[3] + ' ' + w[4]).toLowerCase().includes(q)));
    if (!items.length) return;
    shown += items.length;
    const sec = document.createElement('section');
    sec.innerHTML = `<h3 class="wb-sec"><span class="wb-dot" style="background:${meta.color}"></span>${meta.name} <span class="wb-sec-n">${items.length}</span></h3>`;
    if (cat === 'synonyms') {
      items.forEach(([, k, , v, , id]) => {
        const d = document.createElement('div');
        d.className = 'wb-syn';
        d.innerHTML =
          `<button class="wb-speaker" title="Hear it" aria-label="Pronounce ${wrEsc(k)}" onclick="wbSpeak('${k.replace(/'/g, "\\'")}', this)">🔊</button>` +
          `<span class="wb-syn-key">${wbHl(k, q)}</span><span class="wb-arrow">→</span><span class="wb-syn-val">${wbHl(v, q)}</span>` +
          (id ? `<button class="wb-del" title="Remove" aria-label="Remove ${wrEsc(k)}" onclick="wbDelete(${id})">✕</button>` : '');
        sec.appendChild(d);
      });
    } else {
      const grid = document.createElement('div');
      grid.className = 'wb-grid';
      items.forEach(([, word, pos, def, eg, id]) => {
        const card = document.createElement('div');
        card.className = 'wb-card';
        card.style.borderLeftColor = meta.color;
        card.innerHTML =
          `<div class="wb-word-row">` +
            `<button class="wb-speaker" title="Hear it" aria-label="Pronounce ${wrEsc(word)}" onclick="wbSpeak('${word.replace(/'/g, "\\'")}', this)">🔊</button>` +
            `<span class="wb-word">${wbHl(word, q)}</span>` +
            (pos ? `<span class="wb-pos">${wrEsc(pos)}</span>` : '') +
            (id ? `<button class="wb-del" title="Remove" aria-label="Remove ${wrEsc(word)}" onclick="wbDelete(${id})">✕</button>` : '') +
          `</div>` +
          `<div class="wb-def">${wbHl(def, q)}</div>` +
          (eg ? `<div class="wb-eg">${wbHl(eg, q)}</div>` : '');
        grid.appendChild(card);
      });
      sec.appendChild(grid);
    }
    content.appendChild(sec);
  });
  document.getElementById('wb-empty').classList.toggle('hidden', shown > 0);
  document.getElementById('wb-count').textContent = shown + ' shown · ' + WB_ALL.length + ' total';
}

async function wrRefreshStats() {
  try {
    const s = await api('GET', '/api/writing/stats', null, { quiet: true }); // background badge refresh
    const btn = document.getElementById('wr-drills-btn');
    if (s.due_drills > 0) {
      btn.classList.remove('hidden');
      document.getElementById('wr-due-badge').textContent = `${s.due_drills} due`;
    } else btn.classList.add('hidden');
    const trend = (s.band_trend || []).slice(-8);
    document.getElementById('wr-band-trend').textContent =
      trend.length ? 'Recent bands: ' + trend.map(t => t.overall_band).join(' → ') : '';
  } catch(e) {}
}

function wrSetTask(t) {
  WR.task = t;
  document.getElementById('wr-task-A').classList.toggle('active', t === 'A');
  document.getElementById('wr-task-B').classList.toggle('active', t === 'B');
  wrLoadStimulus(false);
}

async function wrLoadStimulus(generate) {
  const box = document.getElementById('wr-stimulus');
  box.innerHTML = `<p class="text-slate-400 text-sm">${generate ? 'Generating a fresh stimulus with AI…' : 'Loading stimulus…'}</p>`;
  try {
    const s = await api('GET', `/api/writing/stimulus?task=${WR.task}&generate=${!!generate}`, null, { quiet: true }); // error shown inline in the stimulus card
    WR.stimulus = s;
    wrRenderStimulus(s);
  } catch(e) { box.innerHTML = `<p class="text-red-500 text-sm">${wrEsc(e.message)}</p>`; }
}

function wrRenderStimulus(s) {
  document.getElementById('wr-stimulus').innerHTML = `
    <div class="text-xs font-semibold uppercase tracking-widest mb-1" style="color:var(--wr-accent-deep,#52644f)">Task ${wrEsc(s.task)} · ${s.task === 'A' ? 'Argumentative / analytical' : 'Reflective / personal'}</div>
    <h3 class="text-xl font-bold text-slate-800 mb-4">${wrEsc(s.theme)}</h3>
    <div class="space-y-2 mb-4">
      ${(s.quotes || []).map(q => `<blockquote class="wr-quote">${wrEsc(q)}</blockquote>`).join('')}
    </div>
    <p class="text-sm text-slate-500 italic">${wrEsc(s.instruction || '')}</p>`;
}

// ── Timer: GAMSAT-authentic 5 min reading + 30 min writing ──
function wrToggleTimer() {
  if (WR.timer) { wrStopTimer(); return; }
  WR.timerPhase = 'reading'; WR.timerLeft = 5 * 60;
  document.getElementById('wr-timer-btn').textContent = '⏹ Stop timer';
  document.getElementById('wr-timer').classList.remove('hidden');
  WR.timer = setInterval(() => {
    WR.timerLeft--;
    if (WR.timerLeft <= 0) {
      if (WR.timerPhase === 'reading') {
        WR.timerPhase = 'writing'; WR.timerLeft = 30 * 60;
        toast('Reading time over — start writing!', 'info');
      } else {
        wrStopTimer(); toast('Time is up — submit your essay!', 'info'); return;
      }
    }
    wrRenderTimer();
  }, 1000);
  wrRenderTimer();
}
function wrRenderTimer() {
  const m = Math.floor(WR.timerLeft / 60), s = WR.timerLeft % 60;
  document.getElementById('wr-timer').textContent =
    `${WR.timerPhase === 'reading' ? '📖 Reading' : '✍️ Writing'} ${m}:${String(s).padStart(2, '0')}`;
}
function wrStopTimer() {
  clearInterval(WR.timer); WR.timer = null;
  document.getElementById('wr-timer').classList.add('hidden');
  document.getElementById('wr-timer-btn').textContent = '⏱ Start 5+30';
}

function wrUpdateWordCount() {
  const n = document.getElementById('wr-essay').value.trim().split(/\s+/).filter(Boolean).length;
  const el = document.getElementById('wr-wordcount');
  let note = '';                                  // GAMSAT essays run ~500 words
  if (n === 0)        note = '';
  else if (n < 150)   note = ' · keep going';
  else if (n < 400)   note = ' · aim ~500';
  else if (n <= 650)  note = ' · good length';
  else                note = ' · consider tightening';
  el.textContent = `${n} words${note}`;
}

async function wrSubmitEssay() {
  const essay = document.getElementById('wr-essay').value.trim();
  if (essay.split(/\s+/).filter(Boolean).length < 30) { toast('Write at least ~30 words first', 'error'); return; }
  if (!WR.stimulus) { toast('Load a stimulus first', 'error'); return; }
  const btn = document.getElementById('wr-submit');
  btn.disabled = true; btn.textContent = 'Assessing…';
  loading(true, 'Marking your essay against the rubric…');
  try {
    const r = await api('POST', '/api/writing/assess', {
      task: WR.stimulus.task, theme: WR.stimulus.theme,
      quotes: WR.stimulus.quotes, instruction: WR.stimulus.instruction, essay });
    r.essay = essay;
    wrRenderAssessment(r);
    wrRefreshStats();
    WR.progressLoaded = false; // new essay → Progress tab reloads on next open
  } catch(e) { toast(e.message, 'error'); }
  finally { loading(false); btn.disabled = false; btn.textContent = 'Submit for Assessment'; }
}

// Render the essay with each grammar error's `original` span highlighted; hover/focus shows the fix.
// Error taxonomy → colour families. Each of the 10 audit categories maps to one
// of 5 visual groups so the marked essay is legible at a glance. `key` becomes a
// CSS class suffix (.wr-fam-grammar etc.); `label` heads the legend.
const WR_ERR_GROUPS = {
  grammar:     { key: 'grammar',     label: 'Grammar',     cats: ['article', 'preposition', 'verb-tense', 'agreement', 'word-order'] },
  'word-choice': { key: 'word',      label: 'Word choice', cats: ['word-choice'] },
  spelling:    { key: 'spelling',    label: 'Spelling',    cats: ['spelling', 'plurals'] },
  punctuation: { key: 'punctuation', label: 'Punctuation', cats: ['punctuation'] },
  register:    { key: 'register',    label: 'Register',    cats: ['register'] },
};
// category string → family key ('grammar' | 'word' | 'spelling' | 'punctuation' | 'register')
function wrErrFamily(cat) {
  cat = (cat || '').toLowerCase();
  for (const g of Object.values(WR_ERR_GROUPS)) if (g.cats.includes(cat)) return g.key;
  return 'grammar';
}

// Locate each error's span in the essay and attach a stable 1-based number, so the
// coloured marks and the reasoning list below share the same index. Returns the
// spans (with .num) so the caller can render a matching list.
function wrLocateErrors(text, errors) {
  const spans = [], used = [];
  (errors || []).forEach((e, i) => {
    const orig = ((e && e.original) || '').trim();
    if (!orig) { return; }
    let from = 0, idx;
    while ((idx = text.indexOf(orig, from)) !== -1) {
      const end = idx + orig.length;
      if (!used.some(u => idx < u[1] && end > u[0])) { used.push([idx, end]); spans.push({ start: idx, end, e, srcIdx: i }); break; }
      from = idx + 1;
    }
  });
  spans.sort((a, b) => a.start - b.start);
  spans.forEach((s, i) => { s.num = i + 1; });   // number in reading order
  return spans;
}

function wrHighlightEssay(text, errors) {
  const spans = wrLocateErrors(text, errors);
  let html = '', cur = 0;
  spans.forEach(s => {
    html += wrEsc(text.slice(cur, s.start));
    const fam = wrErrFamily(s.e.category);
    const tip = [s.e.corrected ? '→ ' + s.e.corrected : '', s.e.explanation || '', s.e.category ? '(' + s.e.category + ')' : '']
      .filter(Boolean).join('  ·  ');
    html += `<mark class="wr-err-mark wr-fam-${fam}" tabindex="0" title="${wrEsc(tip)}">` +
            `${wrEsc(text.slice(s.start, s.end))}<sup class="wr-err-num">${s.num}</sup></mark>`;
    cur = s.end;
  });
  return html + wrEsc(text.slice(cur));
}

// The numbered legend shown above the marked essay — only the families actually present.
function wrErrLegend(errors) {
  const present = new Set((errors || []).map(e => wrErrFamily(e.category)));
  const items = Object.values(WR_ERR_GROUPS).filter(g => present.has(g.key))
    .map(g => `<span class="wr-legend-item"><span class="wr-legend-swatch wr-fam-${g.key}"></span>${g.label}</span>`)
    .join('');
  return items ? `<div class="wr-legend">${items}</div>` : '';
}

// Numbered reasoning list — one row per error, index-matched to the marks above.
function wrErrReasonList(text, errors) {
  const spans = wrLocateErrors(text, errors);
  // errors whose original couldn't be located still deserve a row (appended, unnumbered marks)
  const located = new Set(spans.map(s => s.srcIdx));
  const rows = spans.map(s => wrErrReasonRow(s.num, s.e));
  (errors || []).forEach((e, i) => { if (!located.has(i)) rows.push(wrErrReasonRow(null, e)); });
  return rows.join('');
}
function wrErrReasonRow(num, e) {
  const fam = wrErrFamily(e.category);
  return `<li class="wr-reason">
    <span class="wr-reason-num wr-fam-${fam}">${num ?? '•'}</span>
    <div class="wr-reason-body">
      <div class="wr-reason-head">
        <span class="wr-cat-chip wr-fam-${fam}">${wrEsc(e.category || '')}</span>
        ${e.original ? `<span class="wr-reason-fix"><span class="wr-reason-orig">${wrEsc(e.original)}</span> <span class="wr-reason-arrow">→</span> <span class="wr-reason-corr">${wrEsc(e.corrected || '')}</span></span>` : ''}
      </div>
      ${e.explanation ? `<p class="wr-reason-why">${wrEsc(e.explanation)}</p>` : ''}
    </div>
  </li>`;
}

function wrRenderAssessment(r, targetEl) {
  const a = r.assessment || {};
  const chip = b => `<span class="wr-band-chip ${b >= 5 ? 'wr-band-high' : b >= 4 ? 'wr-band-mid' : 'wr-band-low'}">Band ${b}</span>`;
  // evidence may be a single string (old shape) or an array of up to 3 quotes (new)
  const evidenceHtml = c => {
    const ev = Array.isArray(c.evidence) ? c.evidence : (c.evidence ? [c.evidence] : []);
    return ev.filter(Boolean).map(q => `<div class="wr-evidence">“${wrEsc(q)}”</div>`).join('');
  };
  const crits = (a.criteria || []).map(c => `
    <div class="bg-slate-50 rounded-xl border border-slate-200 p-4">
      <div class="flex items-center justify-between gap-2 mb-2">
        <span class="font-semibold text-slate-700 text-sm">${wrEsc(c.name)}</span>
        <span class="flex items-center gap-1">${chip(c.band)}${c.capped_by_error_density ? '<span class="text-[10px] font-semibold text-amber-600" title="Capped by objective grammar error density">capped</span>' : ''}</span>
      </div>
      ${evidenceHtml(c)}
      <p class="text-sm text-slate-600 mt-2">${wrEsc(c.justification || '')}</p>
    </div>`).join('');
  const st = r.error_stats || {};
  const essayText = r.essay || r.essay_text || '';
  const marked = essayText ? `
    <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <h4 class="text-sm font-bold text-slate-700 mb-1">Your essay — marked</h4>
      ${(r.errors || []).length ? `<p class="text-xs text-slate-400 mb-2">Each highlight is numbered — the matching explanation is in the list below.</p>${wrErrLegend(r.errors)}` : ''}
      <div class="wr-marked-essay">${(r.errors || []).length ? wrHighlightEssay(essayText, r.errors) : wrEsc(essayText)}</div>
    </div>` : '';
  const panel = targetEl || document.getElementById('wr-assessment');
  panel.innerHTML = `
    <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
      <div class="flex items-center gap-4 mb-5">
        <div class="wr-overall">${a.overall_band ?? '–'}</div>
        <div>
          <div class="font-bold text-slate-800 text-lg">Overall Band ${a.overall_band ?? '–'} / 6</div>
          <div class="text-xs text-slate-500">${st.error_count ?? 0} language errors · ${st.per_100_words ?? 0} per 100 words · Language cap: band ${st.language_band_cap ?? 6}</div>
        </div>
        <button onclick="wrPrintReport()" class="btn-secondary text-sm ml-auto" title="Print or save this report as a PDF">🖨 Report</button>
      </div>
      <div class="grid md:grid-cols-2 gap-3">${crits}</div>
    </div>
    ${marked}
    <div class="grid md:grid-cols-2 gap-4">
      <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
        <h4 class="text-sm font-bold text-green-700 mb-2">Strengths</h4>
        <ul class="list-disc pl-5 text-sm text-slate-600 space-y-1">${(a.strengths || []).map(s => `<li>${wrEsc(s)}</li>`).join('')}</ul>
      </div>
      <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
        <h4 class="text-sm font-bold text-amber-700 mb-2">Priority fixes</h4>
        <ul class="list-disc pl-5 text-sm text-slate-600 space-y-1">${(a.priority_improvements || []).map(s => `<li>${wrEsc(s)}</li>`).join('')}</ul>
      </div>
    </div>
    ${(r.errors || []).length ? `
    <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
      <h4 class="text-sm font-bold text-slate-700 mb-1">Error breakdown (${r.errors.length}) — numbered to match your essay above</h4>
      <p class="text-xs text-slate-400 mb-3">Every mistake, with the rule behind it. These feed your grammar drills.</p>
      <ol class="wr-reason-list">${wrErrReasonList(essayText, r.errors)}</ol>
    </div>` : ''}`;
  panel.classList.remove('hidden');
  if (!targetEl) panel.scrollIntoView({ behavior: 'smooth' });
}

// Print / Save-as-PDF a clean standalone report of the currently rendered assessment.
function wrPrintReport() {
  const panel = document.getElementById('wr-assessment');
  if (!panel || panel.classList.contains('hidden') || !panel.innerHTML.trim()) {
    toast('Assess an essay first', 'error'); return;
  }
  const w = window.open('', '_blank');
  if (!w) { toast('Allow pop-ups to print the report', 'error'); return; }
  w.document.write(`<!doctype html><html><head><meta charset="utf-8"><title>Writing assessment report</title>
    <style>
      body { font-family: Georgia,'Iowan Old Style',serif; max-width: 820px; margin: 28px auto; padding: 0 18px; color: #2b2b2b; line-height: 1.6; }
      h2 { margin: 0 0 4px; } .sub { color:#777; font-size:13px; margin-bottom:18px; }
      .wr-marked-essay { white-space: pre-wrap; }
      .wr-err-mark { background: var(--fam-bg, rgba(176,84,56,.14)); border-bottom: 2px solid var(--fam-line, rgba(176,84,56,.55)); }
      .wr-err-num { font-size: .62em; font-weight: 700; vertical-align: super; margin-left: 1px; color: var(--fam-line,#b05438); }
      .wr-fam-grammar{--fam-bg:rgba(37,99,235,.13);--fam-line:#2563eb;--fam-ink:#1d4ed8}
      .wr-fam-word{--fam-bg:rgba(139,92,246,.14);--fam-line:#8b5cf6;--fam-ink:#6d28d9}
      .wr-fam-spelling{--fam-bg:rgba(220,38,38,.13);--fam-line:#dc2626;--fam-ink:#b91c1c}
      .wr-fam-punctuation{--fam-bg:rgba(217,119,6,.15);--fam-line:#d97706;--fam-ink:#b45309}
      .wr-fam-register{--fam-bg:rgba(13,148,136,.14);--fam-line:#0d9488;--fam-ink:#0f766e}
      .wr-legend{display:flex;flex-wrap:wrap;gap:12px;margin-bottom:12px} .wr-legend-item{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#6b6355} .wr-legend-swatch{width:12px;height:12px;border-radius:3px;background:var(--fam-bg);border-bottom:2px solid var(--fam-line)}
      .wr-reason-list{list-style:none;margin:0;padding:0} .wr-reason{display:flex;gap:12px;padding:9px 0;border-top:1px solid #eee} .wr-reason-num{flex-shrink:0;width:22px;height:22px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:var(--fam-bg);color:var(--fam-ink);border:1.5px solid var(--fam-line)} .wr-cat-chip{font-size:11px;font-weight:700;text-transform:uppercase;padding:2px 8px;border-radius:9999px;background:var(--fam-bg);color:var(--fam-ink)} .wr-reason-head{display:flex;gap:10px;align-items:center;flex-wrap:wrap} .wr-reason-orig{color:#b91c1c;text-decoration:line-through} .wr-reason-corr{color:#15803d;font-weight:600} .wr-reason-why{margin:4px 0 0;font-size:13px;color:#6b6355}
      table { width:100%; border-collapse: collapse; font-size: 13px; margin-top: 6px; }
      th,td { text-align:left; padding: 4px 8px; border-bottom: 1px solid #eee; vertical-align: top; }
      h4 { margin: 18px 0 6px; } ul { margin: 4px 0; padding-left: 20px; }
      .wr-band-chip { border:1px solid #ccc; border-radius: 9999px; padding: 1px 8px; font-size: 12px; }
      .line-through { text-decoration: line-through; }
      @media print { button { display:none; } }
    </style></head>
    <body><h2>Writing assessment report</h2><div class="sub">${new Date().toLocaleString()}</div>${panel.innerHTML}</body></html>`);
  w.document.close(); w.focus();
  setTimeout(() => { try { w.print(); } catch (e) {} }, 300);
}

// ── Progress tab — read-only analytics over stored essays (no AI) ─────────
const WR_CRIT_SHORT = {
  'Quality of Thought & Argument': 'Thought & Argument',
  'Structure & Development':       'Structure',
  'Language & Expression':         'Language',
  'Engagement with the Stimulus':  'Engagement',
};
const WR_CRIT_ADVICE = {
  'Quality of Thought & Argument': 'Sharpen your contention — take a position someone could disagree with, and develop it in depth rather than breadth.',
  'Structure & Development':       'Two developed body paragraphs plus a counter-argument beat four thin ones. Plan the skeleton before you write.',
  'Language & Expression':         'Error density caps this band — slow down and re-read. Your grammar drills target your exact recurring mistakes.',
  'Engagement with the Stimulus':  'Engage the quotes’ claims directly — argue with at least one of them rather than writing around the theme.',
};
// Per-error-category coaching — what it is · why it costs you · how to fix it.
// Drives the zero-AI "Personalised for you" tips from your real error counts.
const WR_CAT_ADVICE = {
  'article':     { what: 'Missing or wrong a/an/the.', fix: 'Before each noun ask: is this one specific thing (the) or one of many (a/an)? Uncountable nouns often take no article.' },
  'preposition': { what: 'Wrong little linking word (in/on/at/of/for).', fix: 'These go by fixed pairings, not logic — learn them per phrase (“depend on”, “consist of”). Note each one you miss.' },
  'verb-tense':  { what: 'Tense slips or inconsistency.', fix: 'Pick one narrative tense and hold it. Scan each paragraph for a verb that jumps time without reason.' },
  'agreement':   { what: 'Subject and verb don’t match in number.', fix: 'Find the true subject and check singular/plural — beware phrases between subject and verb (“the list of items IS…”).' },
  'word-choice': { what: 'A word that’s close but not right.', fix: 'When a word feels approximate, name the exact idea and pick the precise term. Watch commonly-confused pairs (affect/effect, then/than).' },
  'word-order':  { what: 'Words in an unnatural sequence.', fix: 'Read the sentence aloud — English is Subject–Verb–Object; keep modifiers next to what they modify.' },
  'plurals':     { what: 'Singular/plural form errors.', fix: 'Check irregular plurals (criterion→criteria, phenomenon→phenomena) and don’t add ’s for a plural.' },
  'spelling':    { what: 'Misspelled words.', fix: 'Keep a personal list of the ones you miss and drill them — most spelling errors are a small set of repeat offenders.' },
  'punctuation': { what: 'Comma splices, missing/extra marks.', fix: 'Two full sentences can’t be joined by a comma — use a full stop, semicolon, or a conjunction. Read for where you pause.' },
  'register':    { what: 'Too informal for an essay.', fix: 'Cut contractions, slang and filler; state ideas plainly and formally. If it sounds like a text, rewrite it.' },
};

// "Personalised for you" — recurring flaws from your real error/criterion data (zero AI),
// plus a clearly-labelled opt-in AI deep-dive button.
async function wrLoadPersonalTips() {
  const wrap = document.getElementById('wr-personal');
  if (!wrap) return;
  let s;
  try { s = await api('GET', '/api/writing/stats', null, { quiet: true }); }
  catch (e) { wrap.innerHTML = ''; return; }   // silently fall back to the static guide
  if (!s || !s.essay_count) {
    wrap.innerHTML = `<div class="wr-personal">
      <div class="wr-personal-head"><h3>Personalised for you</h3></div>
      <p class="wr-personal-empty">Write and submit an essay in the Practice tab — then this fills with tips built from your own recurring mistakes.</p>
    </div>`;
    return;
  }
  const errs = Object.entries(s.errors_by_category || {}).sort((a, b) => b[1] - a[1]).slice(0, 3);
  const crits = (s.criteria_averages || []).filter(c => c.count > 0).sort((a, b) => a.avg - b.avg);
  const weakest = crits[0];

  const flawRows = errs.map(([cat, n]) => {
    const fam = wrErrFamily(cat);
    const a = WR_CAT_ADVICE[cat] || { what: '', fix: '' };
    return `<li class="wr-flaw">
      <div class="wr-flaw-head">
        <span class="wr-cat-chip wr-fam-${fam}">${wrEsc(cat)}</span>
        <span class="wr-flaw-count">${n}×</span>
        <span class="wr-flaw-what">${wrEsc(a.what)}</span>
      </div>
      <p class="wr-flaw-fix">${wrEsc(a.fix)}</p>
    </li>`;
  }).join('');

  const weakestHtml = weakest ? `
    <div class="wr-weakest">
      <div class="wr-weakest-label">Weakest criterion · avg band ${weakest.avg} over ${weakest.count} essay${weakest.count === 1 ? '' : 's'}</div>
      <div class="wr-weakest-name">${wrEsc(WR_CRIT_SHORT[weakest.name] || weakest.name)}</div>
      <p class="wr-weakest-advice">${wrEsc(WR_CRIT_ADVICE[weakest.name] || '')}</p>
    </div>` : '';

  wrap.innerHTML = `<div class="wr-personal">
    <div class="wr-personal-head">
      <h3>Personalised for you</h3>
      <span class="wr-personal-sub">from your ${s.essay_count} essay${s.essay_count === 1 ? '' : 's'}</span>
    </div>
    ${weakestHtml}
    ${flawRows ? `<div class="wr-flaws-title">Your recurring language slips</div><ol class="wr-flaws">${flawRows}</ol>` : ''}
    <div class="wr-personal-actions">
      ${errs.length ? `<button class="btn-secondary text-sm" onclick="wrShowTab('practice'); wrLoadDrills();">Drill these →</button>` : ''}
      <button id="wr-coach-btn" class="btn-secondary text-sm" onclick="wrAiDeepDive()" title="Uses AI credit">✨ AI deep-dive <span class="wr-credit-note">(uses credit)</span></button>
    </div>
    <div id="wr-coach-out" class="wr-coach-out hidden"></div>
  </div>`;
}

// Opt-in AI coaching — the only credit-spending path here, behind an explicit button.
async function wrAiDeepDive() {
  const btn = document.getElementById('wr-coach-btn');
  const out = document.getElementById('wr-coach-out');
  if (!out) return;
  if (btn) { btn.disabled = true; btn.textContent = 'Analysing your essays…'; }
  out.classList.remove('hidden');
  out.innerHTML = '<div class="skeleton rounded-xl" style="height:120px"></div>';
  try {
    const r = await api('POST', '/api/writing/coach', {});
    const tips = (r.tips || []).map(t => `<li>${wrEsc(t)}</li>`).join('');
    out.innerHTML = `<div class="wr-coach-card">
      <div class="wr-coach-head">✨ AI coach — tailored to your essays</div>
      ${r.summary ? `<p class="wr-coach-summary">${wrEsc(r.summary)}</p>` : ''}
      ${tips ? `<ul class="wr-coach-tips">${tips}</ul>` : ''}
    </div>`;
  } catch (e) {
    out.innerHTML = `<p class="text-sm text-red-500">${wrEsc(e.message || 'Deep-dive failed')}</p>`;
  } finally {
    if (btn) { btn.disabled = false; btn.innerHTML = '✨ AI deep-dive <span class="wr-credit-note">(uses credit)</span>'; }
  }
}
const wrDate = s => { try { return new Date(String(s).replace(' ', 'T') + 'Z')
  .toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }); } catch(e) { return s; } };

async function wrLoadProgress() {
  const loadEl = document.getElementById('wr-prog-loading');
  // Skeleton mirroring the Progress layout: chart card + 4 criterion cards
  loadEl.innerHTML = `
    <div class="skeleton rounded-2xl" style="height:260px" aria-hidden="true"></div>
    <div class="grid sm:grid-cols-2 xl:grid-cols-4 gap-3 mt-4" aria-hidden="true">
      ${Array.from({ length: 4 }, () => '<div class="skeleton rounded-2xl" style="height:96px"></div>').join('')}
    </div>`;
  loadEl.classList.remove('hidden');
  try {
    const s = await api('GET', '/api/writing/stats', null, { quiet: true }); // error shown inline below
    WR.progressLoaded = true;
    loadEl.classList.add('hidden');
    const trend = s.band_trend || [];
    document.getElementById('wr-prog-empty').classList.toggle('hidden', trend.length > 0);
    document.getElementById('wr-prog-content').classList.toggle('hidden', !trend.length);
    document.getElementById('wr-essay-detail').classList.add('hidden');
    if (!trend.length) return;
    wrRenderTrendChart(trend, s.improvement);
    wrRenderCriteria(s.criteria_averages || [], trend);
    wrRenderFocusNext(s);
    wrRenderErrorBreakdown(s.errors_by_category || {});
    wrRenderArchive(trend, s.essay_count);
  } catch(e) {
    loadEl.innerHTML = `<p class="text-sm text-center py-8" style="color:#8a5347">Could not load progress — ${wrEsc(e.message)}</p>`;
  }
}

// Chart.js line of overall band + per-criterion lines. Calm writing palette —
// muted sage/clay/stone, deliberately NOT the dashboard cyan.
function wrRenderTrendChart(trend, improvement) {
  const el = document.getElementById('wr-trend-chart');
  if (S.charts.wrTrend) S.charts.wrTrend.destroy();

  const labels = trend.map(t => wrDate(t.created_at).replace(/ \d{4}$/, ''));
  // Criterion names in order of first appearance across the trend
  const critNames = [];
  trend.forEach(t => Object.keys(t.criteria || {}).forEach(n => { if (!critNames.includes(n)) critNames.push(n); }));

  const ctx = el.getContext('2d');
  const areaFill = () => {
    const gr = ctx.createLinearGradient(0, 0, 0, el.height || 240);
    gr.addColorStop(0, 'rgba(107,127,106,0.18)'); // sage, soft
    gr.addColorStop(1, 'rgba(107,127,106,0)');
    return gr;
  };
  const line = (label, data, color, opts = {}) => ({
    label, data,
    borderColor: color,
    backgroundColor: opts.fill ? areaFill() : 'transparent',
    borderWidth: opts.width || 1.3,
    tension: 0.3,
    fill: !!opts.fill,
    spanGaps: true,
    pointRadius: opts.points ? 3 : 0,
    pointHoverRadius: 4,
    pointBackgroundColor: '#fffdf8',
    pointBorderColor: color,
    pointBorderWidth: 2,
    borderDash: opts.dashed ? [4, 4] : [],
  });
  const critColors = ['#a8927b', '#8a95a5', '#b0776d', '#9a8fa5']; // tan, stone-blue, clay, mauve — all muted
  const datasets = [
    line('Overall band', trend.map(t => t.overall_band ?? null), '#52644f', { fill: true, width: 2.2, points: true }),
    ...critNames.map((n, i) =>
      line(WR_CRIT_SHORT[n] || n, trend.map(t => (t.criteria || {})[n] ?? null),
           critColors[i % critColors.length], { dashed: true })),
  ];

  S.charts.wrTrend = new Chart(el, {
    type: 'line',
    data: { labels, datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { font: { size: 11 }, boxWidth: 18, padding: 14, color: '#857d70' } },
        tooltip: { mode: 'index', intersect: false, padding: 10, cornerRadius: 6,
          backgroundColor: 'rgba(63,58,51,0.92)', titleFont: { size: 11 }, bodyFont: { size: 12 },
          displayColors: false }
      },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 10 }, color: '#a89f90' }, border: { color: 'rgba(231,224,210,0.9)' } },
        y: { min: 1, max: 6, ticks: { stepSize: 1, font: { size: 10 }, color: '#a89f90', callback: v => 'Band ' + v },
             grid: { color: 'rgba(240,235,224,0.9)' }, border: { display: false } }
      }
    }
  });

  // Honest one-line summary under the heading — soften below 3 essays
  const n = (improvement || {}).sample_size || trend.length;
  const d = (improvement || {}).delta;
  let note = `${n} graded essay${n === 1 ? '' : 's'}`;
  if (n < 3) note += ' — too few to read a trend yet; keep writing.';
  else if (d != null) {
    note += d > 0 ? ` — overall band up ${d.toFixed(1)} comparing your earliest and latest essays.`
          : d < 0 ? ` — overall band down ${Math.abs(d).toFixed(1)} comparing your earliest and latest essays.`
          : ' — overall band holding steady so far.';
  }
  document.getElementById('wr-trend-note').textContent = note;
}

// Per-criterion average cards with an honest, sample-size-aware delta
function wrRenderCriteria(averages, trend) {
  const el = document.getElementById('wr-criteria-cards');
  if (!averages.length) {
    el.innerHTML = '<p class="text-sm col-span-full" style="color:var(--wr-ink-soft,#857d70)">No per-criterion data stored for these essays yet.</p>';
    return;
  }
  el.innerHTML = averages.map(c => {
    const series = trend.map(t => (t.criteria || {})[c.name]).filter(b => b != null);
    let deltaHtml = '';
    if (series.length >= 3) {
      const d = series[series.length - 1] - series[0];
      deltaHtml = d > 0 ? `<span class="wr-crit-delta-up">▲ +${d} since first essay</span>`
                : d < 0 ? `<span class="wr-crit-delta-down">▼ ${d} since first essay</span>`
                :         `<span class="wr-crit-delta-flat">— steady</span>`;
    } else {
      deltaHtml = `<span class="wr-crit-delta-flat">early days — trend needs 3+ essays</span>`;
    }
    return `<div class="wr-crit-card">
      <div class="wr-crit-name">${wrEsc(WR_CRIT_SHORT[c.name] || c.name)}</div>
      <div class="wr-crit-avg">${c.avg}<span class="text-sm font-medium" style="color:var(--wr-ink-soft,#857d70)"> / 6 avg</span></div>
      <div class="wr-crit-meta">across ${c.count} essay${c.count === 1 ? '' : 's'} · ${deltaHtml}</div>
    </div>`;
  }).join('');
}

// Pure logic: lowest-average criterion + most frequent error category
function wrRenderFocusNext(s) {
  const el = document.getElementById('wr-focus-next');
  const avgs = s.criteria_averages || [];
  const weakest = avgs.length ? avgs.reduce((a, b) => (b.avg < a.avg ? b : a)) : null;
  const errs = Object.entries(s.errors_by_category || {}).sort((a, b) => b[1] - a[1]);
  const topErr = errs[0];
  let html = `<h4 class="text-sm font-bold mb-3" style="color:var(--wr-ink,#3f3a33)">Focus next</h4>`;
  if (!weakest && !topErr) {
    html += `<p class="text-sm" style="color:var(--wr-ink-soft,#857d70)">Once a few essays are graded, your weakest criterion and most frequent language slips will show up here.</p>`;
  } else {
    if (weakest) {
      html += `<div class="mb-3">
        <div class="text-xs font-semibold uppercase tracking-widest mb-1" style="color:var(--wr-accent-deep,#52644f)">Weakest criterion</div>
        <p class="text-sm font-semibold" style="color:var(--wr-ink,#3f3a33)">${wrEsc(weakest.name)} <span class="font-normal" style="color:var(--wr-ink-soft,#857d70)">· avg band ${weakest.avg} over ${weakest.count} essay${weakest.count === 1 ? '' : 's'}</span></p>
        <p class="text-sm mt-1" style="color:var(--wr-ink-soft,#857d70)">${wrEsc(WR_CRIT_ADVICE[weakest.name] || 'Give this dimension extra attention in your next essay.')}</p>
      </div>`;
    }
    if (topErr) {
      html += `<div class="mb-3">
        <div class="text-xs font-semibold uppercase tracking-widest mb-1" style="color:var(--wr-accent-deep,#52644f)">Most frequent language slip</div>
        <p class="text-sm" style="color:var(--wr-ink,#3f3a33)"><span class="wr-err-cat">${wrEsc(topErr[0])}</span> <span style="color:var(--wr-ink-soft,#857d70)">· ${topErr[1]} time${topErr[1] === 1 ? '' : 's'} across your essays</span></p>
      </div>`;
    }
    html += `<button class="btn-secondary text-sm" onclick="wrShowTab('practice'); wrLoadDrills();">Practice grammar drills →</button>`;
  }
  el.innerHTML = html;
}

// Compact bar list from errors_by_category
function wrRenderErrorBreakdown(errors) {
  const el = document.getElementById('wr-error-breakdown');
  const entries = Object.entries(errors).sort((a, b) => b[1] - a[1]);
  let html = `<h4 class="text-sm font-bold mb-3" style="color:var(--wr-ink,#3f3a33)">Language errors by category</h4>`;
  if (!entries.length) {
    html += `<p class="text-sm" style="color:var(--wr-ink-soft,#857d70)">No recorded language errors — either spotless prose or no essays yet.</p>`;
  } else {
    const max = entries[0][1];
    html += entries.slice(0, 8).map(([cat, n]) => `
      <div class="flex items-center gap-3 py-1.5">
        <span class="text-sm flex-1 truncate" style="color:var(--wr-ink,#3f3a33)">${wrEsc(cat)}</span>
        <div class="w-28 flex-shrink-0"><div class="wr-err-bar" style="width:${Math.max(8, Math.round(n / max * 100))}%"></div></div>
        <span class="text-xs w-6 text-right flex-shrink-0" style="color:var(--wr-ink-soft,#857d70)">${n}</span>
      </div>`).join('');
  }
  el.innerHTML = html;
}

// Archive list — date · task · theme · band; click to re-open the full essay
function wrRenderArchive(trend, essayCount) {
  const el = document.getElementById('wr-archive-list');
  const chip = b => b == null ? '' :
    `<span class="wr-band-chip ${b >= 5 ? 'wr-band-high' : b >= 4 ? 'wr-band-mid' : 'wr-band-low'}">Band ${b}</span>`;
  el.innerHTML = trend.slice().reverse().map(t => `
    <div class="wr-archive-row" role="button" tabindex="0" onclick="wrOpenEssay(${t.id})" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();wrOpenEssay(${t.id});}" aria-label="Open essay: ${wrEsc(t.theme || 'Untitled theme')}">
      <span class="text-xs flex-shrink-0 w-24" style="color:var(--wr-ink-soft,#857d70)">${wrEsc(wrDate(t.created_at))}</span>
      <span class="text-xs font-semibold flex-shrink-0" style="color:var(--wr-accent-deep,#52644f)">Task ${wrEsc(t.task || '?')}</span>
      <span class="text-sm flex-1 truncate" style="color:var(--wr-ink,#3f3a33)">${wrEsc(t.theme || 'Untitled theme')}</span>
      ${chip(t.overall_band)}
    </div>`).join('') +
    (essayCount > trend.length
      ? `<p class="text-xs mt-2" style="color:var(--wr-ink-soft,#857d70)">Showing your ${trend.length} most recent of ${essayCount} essays.</p>` : '');
}

async function wrOpenEssay(id) {
  const det = document.getElementById('wr-essay-detail');
  det.classList.remove('hidden');
  det.innerHTML = skelBlock(220);   // skeleton while the archived essay loads (#6)
  det.scrollIntoView({ behavior: 'smooth' });
  try {
    const r = await api('GET', `/api/writing/essays/${id}`, null, { quiet: true }); // error shown inline below
    det.innerHTML = `
      <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
        <div class="flex items-start justify-between gap-3 mb-4">
          <div>
            <div class="text-xs font-semibold uppercase tracking-widest mb-1" style="color:var(--wr-accent-deep,#52644f)">Task ${wrEsc(r.task || '?')} · ${wrEsc(wrDate(r.created_at))}</div>
            <h3 class="text-lg font-bold" style="color:var(--wr-ink,#3f3a33)">${wrEsc(r.theme || 'Untitled theme')}</h3>
          </div>
          <button class="text-slate-400 hover:text-red-500 text-sm flex-shrink-0" onclick="wrCloseEssay()">Close ✕</button>
        </div>
        <div class="wr-archive-essay">${wrEsc(r.essay_text)}</div>
      </div>
      <div id="wr-essay-detail-assess" class="space-y-4"></div>`;
    // Re-render the stored assessment with the existing renderer
    wrRenderAssessment(r, document.getElementById('wr-essay-detail-assess'));
  } catch(e) {
    det.innerHTML = `<p class="text-sm text-red-500">${wrEsc(e.message)}</p>`;
  }
}
function wrCloseEssay() { document.getElementById('wr-essay-detail').classList.add('hidden'); }

// ── Grammar drills (SM-2 on your own error patterns) ──
async function wrLoadDrills() {
  loading(true, 'Building drills from your error patterns…');
  try {
    const r = await api('GET', '/api/writing/drills');
    WR.drills = r.drills || [];
    if (!WR.drills.length) { toast('No drills due right now', 'info'); return; }
    WR.drillIdx = 0;
    document.getElementById('wr-drill-panel').classList.remove('hidden');
    document.getElementById('wr-drill-done').classList.add('hidden');
    document.getElementById('wr-drill-card').classList.remove('hidden');
    wrShowDrill();
    document.getElementById('wr-drill-panel').scrollIntoView({ behavior: 'smooth' });
  } catch(e) { toast(e.message, 'error'); }
  finally { loading(false); }
}
// Show the attempt stage: the concept question + an empty response box.
function wrShowDrill() {
  if (WR.drillIdx >= WR.drills.length) { wrDrillsDone(); return; }
  const d = WR.drills[WR.drillIdx];
  document.getElementById('wr-drill-cat').textContent = d.category;
  document.getElementById('wr-drill-question').textContent = d.question || '';
  const resp = document.getElementById('wr-drill-response');
  resp.value = ''; resp.disabled = false;
  document.getElementById('wr-drill-attempt').classList.remove('hidden');
  document.getElementById('wr-drill-reveal').classList.add('hidden');
  document.getElementById('wr-drill-progress').textContent = `Drill ${WR.drillIdx + 1} of ${WR.drills.length}`;
  resp.focus();
}
// Reveal stage: freeze their answer and show it beside the ideal answer + rule.
function wrRevealDrill() {
  if (WR.drillIdx >= WR.drills.length) return;
  const d = WR.drills[WR.drillIdx];
  const yours = (document.getElementById('wr-drill-response').value || '').trim();
  const y = document.getElementById('wr-drill-yours');
  if (yours) { y.textContent = yours; y.classList.remove('wr-drill-empty'); }
  else { y.textContent = '(you left this blank — have a go next time)'; y.classList.add('wr-drill-empty'); }
  document.getElementById('wr-drill-ideal').textContent = d.ideal_answer || '';
  document.getElementById('wr-drill-explanation').textContent = d.explanation || '';
  document.getElementById('wr-drill-attempt').classList.add('hidden');
  document.getElementById('wr-drill-reveal').classList.remove('hidden');
}
async function wrDrillResult(correct) {
  const d = WR.drills[WR.drillIdx];
  try { await api('POST', `/api/writing/drills/${d.card_id}/result`, { correct }, { quiet: true }); } catch(e) {}
  WR.drillIdx++;
  wrShowDrill();
}
function wrDrillsDone() {
  document.getElementById('wr-drill-card').classList.add('hidden');
  document.getElementById('wr-drill-done').classList.remove('hidden');
  wrRefreshStats();
}
function wrCloseDrills() { document.getElementById('wr-drill-panel').classList.add('hidden'); }


// ── Quiz ──────────────────────────────────────────────────────────────────
async function initQuizPage() { await loadMaterials(); }

function setQuizDifficulty(level) {
  S.quizDifficulty = level;
  document.querySelectorAll('.diff-btn').forEach(b => {
    // Strip any active-* class
    b.className = b.className.replace(/\bactive-\w+/g, '').trim();
  });
  const btn = document.getElementById(`diff-${level}`);
  if (btn) btn.classList.add(`active-${level}`);
}

async function generateQuiz(force = false) {
  const id = document.getElementById('quiz-material-select').value;
  if (!S.materials.length) { toast('Upload a material first', 'error'); return; }
  loading(true, force ? `Regenerating ${S.quizDifficulty} quiz…` : `Preparing ${S.quizDifficulty} quiz…`);
  try {
    const mid = id || S.materials[0]?.id;
    const res = await api('POST', `/api/generate/quiz/${mid}?difficulty=${S.quizDifficulty}${force ? '&force=true' : ''}`);
    const msg = res.ai_unavailable ? `AI unavailable — loaded your ${res.count} saved questions`
              : res.existing        ? `${res.count} saved questions loaded (no AI used)`
              :                       `${res.count} questions generated!`;
    toast(msg, res.existing ? 'info' : 'success');
    startQuiz();
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

async function startQuiz() {
  const id = document.getElementById('quiz-material-select').value;
  const emptyEl = document.getElementById('quiz-empty');
  // Skeleton question card while fetching
  emptyEl.innerHTML = skelBlock(260, 'mt-6');
  emptyEl.classList.remove('hidden');
  document.getElementById('quiz-viewer').classList.add('hidden');
  try {
    const qp = new URLSearchParams();
    if (id) qp.set('material_id', id);
    if (S.quizDifficulty) qp.set('difficulty', S.quizDifficulty);
    S.quiz = await api('GET', `/api/quiz?${qp.toString()}`);
    S.qIdx = 0; S.qCorrect = 0; S.qAnswered = false; S.quizResults = [];
    document.getElementById('quiz-done').classList.add('hidden');
    document.getElementById('quiz-review').classList.add('hidden');
    document.getElementById('quiz-explanation').classList.add('hidden');
    if (S.quiz.length) {
      document.getElementById('quiz-viewer').classList.remove('hidden');
      emptyEl.classList.add('hidden');
      showQuestion();
    } else {
      emptyEl.innerHTML = emptyState('🧠', 'No questions yet',
        'Press “Generate Quiz” above to build a question bank from this material.');
      emptyEl.classList.remove('hidden');
      document.getElementById('quiz-viewer').classList.add('hidden');
    }
  } catch(e) {
    console.error(e);   // api() has already toasted (#10)
    emptyEl.innerHTML = emptyState('🧠', 'Couldn’t load the quiz', 'Check your connection and try again.');
  }
}

function showQuestion() {
  if (S.qIdx >= S.quiz.length) { showQuizDone(); return; }
  const q = S.quiz[S.qIdx];
  S.qAnswered = false;
  document.getElementById('quiz-progress-text').textContent = `Question ${S.qIdx+1} of ${S.quiz.length}`;
  document.getElementById('quiz-topic-badge').textContent   = q.topic || '';
  document.getElementById('quiz-progress-bar').style.width  = `${(S.qIdx/S.quiz.length)*100}%`;
  document.getElementById('quiz-question').textContent = q.question;
  // Render chemical structure if SMILES provided
  renderSmilesInEl(q.smiles, document.getElementById('quiz-question').parentElement, 'append');
  document.getElementById('quiz-explanation').classList.add('hidden');
  // Difficulty badge
  const diffEl = document.getElementById('quiz-diff-badge');
  const diffMap = { easy:'bg-green-100 text-green-700', medium:'bg-amber-100 text-amber-700', hard:'bg-red-100 text-red-700', daredevil:'bg-purple-900 text-white' };
  if (diffEl && q.difficulty) {
    diffEl.textContent = q.difficulty === 'daredevil' ? '😈 dare devil' : q.difficulty;
    diffEl.className = `text-xs font-semibold px-2 py-0.5 rounded-full ${diffMap[q.difficulty] || diffMap.medium}`;
    diffEl.classList.remove('hidden');
  } else if (diffEl) { diffEl.classList.add('hidden'); }

  // Spaced-repetition badge — flags a question that's resurfacing on schedule
  let revEl = document.getElementById('quiz-review-badge');
  if (!revEl && diffEl) {
    revEl = document.createElement('span');
    revEl.id = 'quiz-review-badge';
    revEl.className = 'text-xs font-semibold px-2 py-0.5 rounded-full bg-sky-100 text-sky-700';
    diffEl.parentElement.insertBefore(revEl, diffEl);
  }
  if (revEl) {
    if (q.is_review) { revEl.textContent = '🔁 Review'; revEl.classList.remove('hidden'); }
    else revEl.classList.add('hidden');
  }

  const opts = document.getElementById('quiz-options');
  opts.innerHTML = (q.options || []).map((opt, i) => {
    const letter = ['A','B','C','D'][i];
    return `<button class="quiz-option" onclick="selectAnswer('${letter}', this)">${sEsc(opt)}</button>`;
  }).join('');

  const badge = document.getElementById('quiz-score-badge');
  badge.textContent = `${S.qCorrect} / ${S.qIdx} correct`;
  badge.classList.toggle('hidden', S.qIdx === 0);

  // Reorient: scroll the question card to the top so the full question +
  // all options are visible without manual scrolling (cards vary in height).
  const viewer = document.getElementById('quiz-viewer');
  if (viewer) {
    requestAnimationFrame(() => {
      viewer.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // also reset window in case the viewer is near the top already
      if (window.scrollY < viewer.offsetTop) window.scrollTo({ top: viewer.offsetTop - 12, behavior: 'smooth' });
    });
  }
}

async function selectAnswer(letter, btn) {
  if (S.qAnswered) return;
  S.qAnswered = true;
  const q = S.quiz[S.qIdx];

  try {
    const res = await api('POST', `/api/quiz/${q.id}/answer`, { answer: letter });
    // Highlight all buttons
    document.querySelectorAll('.quiz-option').forEach((b, i) => {
      const l = ['A','B','C','D'][i];
      b.disabled = true;
      if (l === res.correct_answer[0]) b.classList.add('correct');
      else if (b === btn && !res.correct) b.classList.add('wrong');
    });

    if (res.correct) S.qCorrect++;

    // Save for post-quiz review
    S.quizResults.push({
      question:       q.question,
      options:        q.options,
      topic:          q.topic,
      difficulty:     q.difficulty || 'medium',
      user_answer:    letter,
      correct_answer: res.correct_answer[0],
      correct:        res.correct,
      explanation:    res.explanation
    });

    // Update the score pill NOW (showQuestion only fires on the next question,
    // so without this the last answer never gets counted in the pill).
    const sb = document.getElementById('quiz-score-badge');
    if (sb) {
      sb.textContent = `${S.qCorrect} / ${S.quizResults.length} correct`;
      sb.classList.remove('hidden');
    }

    const expEl = document.getElementById('quiz-explanation');
    const label = document.getElementById('quiz-result-label');
    label.innerHTML = res.correct
      ? '<span class="text-green-600">✓ Correct!</span>'
      : `<span class="text-red-600">✗ Incorrect</span> — Correct answer: <strong>${res.correct_answer}</strong>`;
    label.className = 'font-semibold mb-2';
    document.getElementById('quiz-explanation-text').textContent = res.explanation || '';
    // Show related topics on quiz
    let qRelEl = document.getElementById('quiz-related');
    if (!qRelEl) {
      qRelEl = document.createElement('div');
      qRelEl.id = 'quiz-related';
      qRelEl.className = 'text-xs mt-2 text-emerald-700';
      expEl.appendChild(qRelEl);
    }
    let qRelated = [];
    try { qRelated = typeof q.related_topics === 'string' ? JSON.parse(q.related_topics) : (q.related_topics || []); } catch(e) {}
    qRelEl.innerHTML = qRelated.length ? '🔗 Related: ' + qRelated.map(r => `<span class="inline-block bg-emerald-50 border border-emerald-200 rounded px-1.5 py-0.5 mr-1">${sEsc(r)}</span>`).join('') : '';
    expEl.classList.remove('hidden');
  } catch(e) { toast(e.message, 'error'); }
}

function nextQuestion() {
  S.qIdx++;
  document.getElementById('quiz-explanation').classList.add('hidden');
  showQuestion();
}

function showQuizDone() {
  document.getElementById('quiz-viewer').classList.add('hidden');
  document.getElementById('quiz-done').classList.remove('hidden');
  const pct = S.quiz.length ? Math.round(S.qCorrect/S.quiz.length*100) : 0;
  document.getElementById('quiz-final-score').textContent =
    `You scored ${S.qCorrect} out of ${S.quiz.length} (${pct}%). ${pct >= 75 ? 'Great work!' : pct >= 50 ? 'Keep practising!' : 'Focus on your weak topics!'}`;
  loadDashboard(); // refresh charts
}

function showQuizReview() {
  document.getElementById('quiz-done').classList.add('hidden');
  document.getElementById('quiz-review').classList.remove('hidden');

  const wrong = S.quizResults.filter(r => !r.correct).length;
  document.getElementById('quiz-review-subtitle').textContent =
    `— ${wrong} wrong, ${S.quizResults.length - wrong} correct`;

  const diffBg = { easy:'bg-green-100 text-green-700', medium:'bg-amber-100 text-amber-700', hard:'bg-red-100 text-red-700' };

  // Wrong answers first, then correct
  const sorted = [...S.quizResults].sort((a, b) => (a.correct ? 1 : 0) - (b.correct ? 1 : 0));

  document.getElementById('quiz-review-list').innerHTML = sorted.map(r => {
    const opts = (r.options || []).map((opt, i) => {
      const letter = ['A','B','C','D'][i];
      let cls = 'border-slate-200 bg-white text-slate-600';
      if (letter === r.correct_answer)             cls = 'border-green-500 bg-green-50 text-green-800 font-medium';
      else if (letter === r.user_answer && !r.correct) cls = 'border-red-400 bg-red-50 text-red-700';
      return `<div class="px-4 py-2.5 rounded-xl border-2 text-sm ${cls}">${sEsc(opt)}</div>`;
    }).join('');

    const borderCol   = r.correct ? 'border-green-400' : 'border-red-400';
    const resultBadge = r.correct
      ? '<span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-green-100 text-green-700">✓ Correct</span>'
      : '<span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-red-100 text-red-700">✗ Wrong</span>';
    const diffBadge = `<span class="text-xs font-semibold px-2 py-0.5 rounded-full ${diffBg[r.difficulty] || diffBg.medium}">${r.difficulty}</span>`;

    return `<div class="card border-l-4 ${borderCol}">
      <div class="flex items-start justify-between gap-3 mb-3">
        <p class="font-medium text-slate-800 leading-relaxed text-sm flex-1">${sEsc(r.question)}</p>
        <div class="flex gap-1.5 flex-shrink-0">${diffBadge}${resultBadge}</div>
      </div>
      <div class="space-y-1.5 mb-3">${opts}</div>
      ${r.explanation ? `<div class="bg-blue-50 border border-blue-200 rounded-xl px-4 py-3 text-sm text-blue-800 leading-relaxed"><span class="font-semibold">Explanation: </span>${sEsc(r.explanation)}</div>` : ''}
    </div>`;
  }).join('');
}

function hideQuizReview() {
  document.getElementById('quiz-review').classList.add('hidden');
  document.getElementById('quiz-done').classList.remove('hidden');
}

// ── Tutor ─────────────────────────────────────────────────────────────────
function initTutorPage() { loadMaterials(); }

function setTutorMode(mode) {
  S.tutorMode = mode;
  document.getElementById('mode-explain').classList.toggle('active', mode === 'explain');
  document.getElementById('mode-socratic').classList.toggle('active', mode === 'socratic');
}

function chatKeydown(e) {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
}

async function sendMessage() {
  const input = document.getElementById('chat-input');
  const msg = input.value.trim();
  if (!msg) return;
  input.value = '';

  appendMessage('user', msg);

  // Typing indicator
  const typing = document.createElement('div');
  typing.className = 'flex gap-2';
  typing.id = 'typing-indicator';
  typing.innerHTML = `<div class="chat-bubble assistant"><div class="typing-dots"><span></span><span></span><span></span></div></div>`;
  document.getElementById('chat-messages').appendChild(typing);
  scrollChat();

  const mid = document.getElementById('tutor-material-select').value;
  let assistantEl = null;

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(S.userId ? { 'X-User-Id': S.userId } : {}) },
      body: JSON.stringify({ message: msg, mode: S.tutorMode, session_id: S.sessionId, material_id: mid || null })
    });

    const reader = res.body.getReader();
    const dec    = new TextDecoder();
    let buf = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const lines = buf.split('\n');
      buf = lines.pop();

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue;
        try {
          const data = JSON.parse(line.slice(6));
          if (data.error) { toast(data.error, 'error'); break; }
          if (data.text) {
            if (!assistantEl) {
              document.getElementById('typing-indicator')?.remove();
              assistantEl = appendMessage('assistant', '');
            }
            assistantEl.innerHTML = formatMd(assistantEl.textContent + data.text);
            assistantEl.dataset.raw = (assistantEl.dataset.raw || '') + data.text;
            scrollChat();
          }
        } catch(e) {}
      }
    }
  } catch(e) {
    document.getElementById('typing-indicator')?.remove();
    appendMessage('assistant', 'Sorry, something went wrong. Check your API key and try again.');
    toast(e.message, 'error');
  }
}

function appendMessage(role, text) {
  document.getElementById('chat-empty')?.remove(); // clear the empty state (#7) on first message
  const wrap = document.createElement('div');
  wrap.className = `flex ${role === 'user' ? 'justify-end' : 'justify-start'}`;
  const bubble = document.createElement('div');
  bubble.className = `chat-bubble ${role}`;
  bubble.innerHTML = role === 'assistant' ? formatMd(text) : escHtml(text);
  wrap.appendChild(bubble);
  document.getElementById('chat-messages').appendChild(wrap);
  scrollChat();
  return bubble;
}

function scrollChat() {
  const el = document.getElementById('chat-messages');
  el.scrollTop = el.scrollHeight;
}

async function clearChat() {
  try { await api('DELETE', `/api/chat/${S.sessionId}`, null, { quiet: true }); } catch(e) {}
  S.sessionId = Math.random().toString(36).slice(2);
  // Back to the friendly empty state (#7) — consistent with a fresh page load
  document.getElementById('chat-messages').innerHTML = `<div id="chat-empty">${emptyState('💬', 'Ask me anything about your materials', 'Pick a material above for context, or switch to Socratic mode to be guided with questions.')}</div>`;
}

function formatMd(text) {
  return text
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/^### (.+)$/gm,'<h4 class="font-semibold mt-3 mb-1">$1</h4>')
    .replace(/^## (.+)$/gm,'<h3 class="font-bold mt-3 mb-1">$1</h3>')
    .replace(/^# (.+)$/gm,'<h2 class="text-lg font-bold mt-3 mb-1">$1</h2>')
    .replace(/^- (.+)$/gm,'<li>$1</li>')
    .replace(/(<li>.*<\/li>)/gs, '<ul class="list-disc pl-4 my-1">$1</ul>')
    .replace(/\n\n/g,'</p><p class="mt-2">')
    .replace(/\n/g,'<br/>')
    .replace(/^(.)/,'<p>$1').concat('</p>');
}
function escHtml(t) {
  return t.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}



// ── Knowledge Graph (force-directed) ─────────────────────────────────────
let _graphAnim = null;

// Cleanup tracker for graph event listeners (prevents leaks on re-init)
let _graphCleanup = null;

async function initGraphPage() {
  if (_graphAnim) { cancelAnimationFrame(_graphAnim); _graphAnim = null; }
  if (_graphCleanup) { _graphCleanup(); _graphCleanup = null; }
  try {
    const data = await api('GET', '/api/knowledge-graph');
    if (!data.nodes.length) {
      const c = document.getElementById('graph-canvas');
      const ctx = c.getContext('2d');
      c.width = c.clientWidth * 2; c.height = c.clientHeight * 2;
      ctx.scale(2, 2);
      ctx.fillStyle = '#94a3b8'; ctx.font = '16px system-ui'; ctx.textAlign = 'center';
      ctx.fillText('Upload materials and take quizzes to build your knowledge graph', c.clientWidth / 2, c.clientHeight / 2);
      return;
    }
    runForceGraph(data);
  } catch(e) { toast(e.message, 'error'); }
}

async function graphResetCustomizations() {
  if (!confirm('Reset all graph customizations? This restores hidden nodes and edges.')) return;
  try {
    await api('POST', '/api/knowledge-graph/reset');
    toast('Graph reset — reloading…', 'success');
    initGraphPage();
  } catch(e) { toast(e.message, 'error'); }
}

function runForceGraph(data) {
  const canvas = document.getElementById('graph-canvas');
  const ctx = canvas.getContext('2d');
  const tooltip = document.getElementById('graph-tooltip');
  const ctxMenu = document.getElementById('graph-context-menu');
  const connectBanner = document.getElementById('graph-connect-banner');
  const dpr = window.devicePixelRatio || 1;

  function resize() {
    const rect = canvas.parentElement.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    canvas.style.width = rect.width + 'px';
    canvas.style.height = rect.height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize();

  let W = canvas.clientWidth, H = canvas.clientHeight;

  // Initialize node positions randomly
  const nodes = data.nodes.map(n => ({
    ...n,
    x: W/2 + (Math.random() - 0.5) * W * 0.6,
    y: H/2 + (Math.random() - 0.5) * H * 0.6,
    vx: 0, vy: 0,
  }));
  const nodeMap = {};
  nodes.forEach(n => nodeMap[n.id] = n);
  let edges = data.edges.filter(e => nodeMap[e.source] && nodeMap[e.target]);

  // State
  let _hoverNode = null, _dragNode = null, _selectedNode = null;
  let _connectMode = false, _connectSource = null;
  // Camera: screen = world * s + offset. Identity by default.
  let _cam = { s: 1, ox: 0, oy: 0 };
  let _panning = false, _panStartX = 0, _panStartY = 0, _panOX = 0, _panOY = 0, _fitted = false;

  // ── Pre-compute word sets for topic similarity ──
  function getWords(label) {
    return new Set(label.toLowerCase().replace(/[^a-z0-9\s]/g, '').split(/\s+/).filter(w => w.length > 2));
  }
  // Cache similarity scores between all topic pairs (computed once)
  const simCache = new Map();
  const topicNodes = nodes.filter(n => n.type === 'topic');
  for (let i = 0; i < topicNodes.length; i++) {
    const wi = getWords(topicNodes[i].label);
    for (let j = i + 1; j < topicNodes.length; j++) {
      const wj = getWords(topicNodes[j].label);
      // Jaccard similarity on word sets
      let inter = 0;
      for (const w of wi) if (wj.has(w)) inter++;
      const union = new Set([...wi, ...wj]).size;
      const sim = union > 0 ? inter / union : 0;
      if (sim > 0.15) { // only store meaningful similarity
        const key = topicNodes[i].id + '|' + topicNodes[j].id;
        simCache.set(key, sim);
      }
    }
  }

  // ── Performance score (0-1) for physics ──
  function perfScore(n) {
    if (n.type === 'topic' && n.attempts > 0) return (n.accuracy || 0) / 100;
    if (n.type === 'subject') return 0.8;
    if (n.type === 'material') return 0.5;
    return 0.3; // no data
  }

  // ── Pre-compute colors (avoid recalc per frame) ──
  function calcColor(n) {
    if (n.type === 'subject') return '#6366f1';
    if (n.type === 'material') return '#0ea5e9';
    const acc = n.accuracy || 0;
    if (n.attempts === 0) return '#94a3b8';
    if (acc <= 50) {
      const t = acc / 50;
      return `rgb(${Math.round(239+(245-239)*t)},${Math.round(68+(158-68)*t)},${Math.round(68+(11-68)*t)})`;
    } else {
      const t = (acc - 50) / 50;
      return `rgb(${Math.round(245-(245-34)*t)},${Math.round(158+(197-158)*t)},${Math.round(11+(94-11)*t)})`;
    }
  }
  nodes.forEach(n => { n._color = calcColor(n); n._perf = perfScore(n); });

  // ── Performance-based physics ──
  const BASE_REPULSION = 5200;
  const SPRING = 0.006;
  const SPRING_LEN = 150;
  const DAMPING = 0.88;        // higher damping → settles instead of jittering
  const CENTER_PULL = 0.0004;
  const SIM_ATTRACTION = 1.0;  // strength of similarity-based attraction
  const MIN_GAP = 70;          // soft minimum spacing (smooth, decays to 0 at the gap)
  const MAX_V = 18;            // velocity cap — prevents the overshoot "glitching"
  const WORLD_MARGIN = Math.max(W, H) * 0.7;  // let nodes spread well past the canvas

  function tick() {
    const N = nodes.length;

    // Repulsion between all nodes — PERFORMANCE BASED
    for (let i = 0; i < N; i++) {
      const ni = nodes[i];
      for (let j = i + 1; j < N; j++) {
        const nj = nodes[j];
        let dx = nj.x - ni.x;
        let dy = nj.y - ni.y;
        let dist2 = dx * dx + dy * dy;
        if (dist2 < 1) dist2 = 1;
        let dist = Math.sqrt(dist2);

        // Performance-based repulsion — green spreads out well, red only SLIGHTLY more
        const avgPerf = (ni._perf + nj._perf) / 2;
        const repMult = 1.7 + 0.5 * (1 - avgPerf);
        let force = (BASE_REPULSION * repMult) / dist2;

        // Soft minimum-spacing push: quadratic, zero at MIN_GAP, so it eases
        // off as nodes separate instead of shoving forever (no jitter).
        if (dist < MIN_GAP) { const g = (MIN_GAP - dist) / MIN_GAP; force += g * g * 22; }

        // Topic similarity attraction — topics sharing words pull together
        if (ni.type === 'topic' && nj.type === 'topic') {
          const simKey = ni.id + '|' + nj.id;
          const sim = simCache.get(simKey) || simCache.get(nj.id + '|' + ni.id) || 0;
          if (sim > 0 && dist > 40) {
            // Similar topics attract proportional to their word overlap (real relationships only)
            force -= SIM_ATTRACTION * sim;
          }
        }

        let fx = dx / dist * force;
        let fy = dy / dist * force;
        ni.vx -= fx; ni.vy -= fy;
        nj.vx += fx; nj.vy += fy;
      }
    }

    // Spring forces along edges
    for (const e of edges) {
      const a = nodeMap[e.source], b = nodeMap[e.target];
      if (!a || !b) continue;
      let dx = b.x - a.x, dy = b.y - a.y;
      let dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const avgP = (a._perf + b._perf) / 2;
      const springK = SPRING * (0.5 + avgP);
      const targetLen = SPRING_LEN * (1.2 - 0.4 * avgP);
      let force = (dist - targetLen) * springK;
      let fx = dx / dist * force;
      let fy = dy / dist * force;
      a.vx += fx; a.vy += fy;
      b.vx -= fx; b.vy -= fy;
    }

    // Center pull + damping + velocity cap + (generous) boundary
    for (const n of nodes) {
      n.vx += (W / 2 - n.x) * CENTER_PULL;
      n.vy += (H / 2 - n.y) * CENTER_PULL;
      n.vx *= DAMPING; n.vy *= DAMPING;
      // Cap speed so a big summed force can't fling a node across the canvas.
      if (n.vx >  MAX_V) n.vx =  MAX_V; else if (n.vx < -MAX_V) n.vx = -MAX_V;
      if (n.vy >  MAX_V) n.vy =  MAX_V; else if (n.vy < -MAX_V) n.vy = -MAX_V;
      if (n !== _dragNode) {
        n.x += n.vx; n.y += n.vy;
      }
      // Wide world bounds — nodes spread out; the camera auto-fits to show them.
      n.x = Math.max(-WORLD_MARGIN, Math.min(W + WORLD_MARGIN, n.x));
      n.y = Math.max(-WORLD_MARGIN, Math.min(H + WORLD_MARGIN, n.y));
    }
  }

  // Fit all nodes into view with padding (called once the layout settles, and on Reset).
  function fitView() {
    if (!nodes.length) return;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    for (const n of nodes) {
      if (n.x < minX) minX = n.x; if (n.x > maxX) maxX = n.x;
      if (n.y < minY) minY = n.y; if (n.y > maxY) maxY = n.y;
    }
    const pad = 70;
    const bw = (maxX - minX) || 1, bh = (maxY - minY) || 1;
    const s = Math.min((W - pad * 2) / bw, (H - pad * 2) / bh, 1.4);
    _cam.s  = Math.max(0.2, s);
    _cam.ox = (W - (minX + maxX) * _cam.s) / 2;
    _cam.oy = (H - (minY + maxY) * _cam.s) / 2;
  }

  // ── Drawing (optimized — no per-node gradients) ──
  function draw() {
    // Clear in screen space, then draw everything through the camera transform.
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.setTransform(dpr * _cam.s, 0, 0, dpr * _cam.s, dpr * _cam.ox, dpr * _cam.oy);

    // Edges
    for (const e of edges) {
      const a = nodeMap[e.source], b = nodeMap[e.target];
      if (!a || !b) continue;
      ctx.beginPath();
      ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
      if (e.concept) {
        // Real concept link (from the AI's related_topics) — the strongest topic-topic
        // signal, so draw it solid teal and thicker the more questions assert it.
        ctx.strokeStyle = 'rgba(13,148,136,0.55)';
        ctx.lineWidth = 1.5 + Math.min(2.5, ((e.weight || 1) - 1) * 0.6);
        ctx.setLineDash([]);
      } else if (e.custom) {
        ctx.strokeStyle = 'rgba(99,102,241,0.5)';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
      } else if (e.similarity) {
        ctx.strokeStyle = 'rgba(168,85,247,0.3)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 6]);
      } else {
        const avgP = (a._perf + b._perf) / 2;
        ctx.strokeStyle = `rgba(100,116,139,${(0.15 + avgP * 0.3).toFixed(2)})`;
        ctx.lineWidth = 1 + avgP;
        ctx.setLineDash([]);
      }
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Connection preview line
    if (_connectMode && _connectSource && _hoverNode && _hoverNode !== _connectSource) {
      ctx.beginPath();
      ctx.moveTo(_connectSource.x, _connectSource.y);
      ctx.lineTo(_hoverNode.x, _hoverNode.y);
      ctx.strokeStyle = 'rgba(99,102,241,0.6)';
      ctx.lineWidth = 2;
      ctx.setLineDash([6, 4]);
      ctx.stroke();
      ctx.setLineDash([]);
    }

    // Nodes
    for (const n of nodes) {
      const r = n.size || 10;
      const isHovered = n === _hoverNode;
      const isConnectSrc = _connectMode && n === _connectSource;

      // Glow ring for hover / connect source
      if (isHovered || isConnectSrc) {
        ctx.beginPath();
        ctx.arc(n.x, n.y, r + 5, 0, Math.PI * 2);
        ctx.fillStyle = n._color.startsWith('rgb') ?
          n._color.replace('rgb', 'rgba').replace(')', ',0.3)') :
          'rgba(99,102,241,0.3)';
        ctx.fill();
      }

      // Main circle
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = n._color;
      ctx.fill();

      // Subtle highlight (cheap 3D)
      ctx.beginPath();
      ctx.arc(n.x - r * 0.2, n.y - r * 0.25, r * 0.45, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.18)';
      ctx.fill();

      // Border
      if (isConnectSrc) {
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#6366f1';
        ctx.beginPath(); ctx.arc(n.x, n.y, r + 1.5, 0, Math.PI * 2); ctx.stroke();
      } else if (isHovered) {
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#fff';
        ctx.beginPath(); ctx.arc(n.x, n.y, r + 1, 0, Math.PI * 2); ctx.stroke();
      }

      // Label
      ctx.fillStyle = '#1e293b';
      ctx.font = n.type === 'subject' ? 'bold 12px system-ui' : '10px system-ui';
      ctx.textAlign = 'center';
      ctx.fillText(n.label, n.x, n.y + r + 14);

      // Accuracy badge
      if (n.type === 'topic' && n.attempts > 0) {
        const badge = `${Math.round(n.accuracy)}%`;
        ctx.font = 'bold 8px system-ui';
        const bw = ctx.measureText(badge).width + 6;
        ctx.fillStyle = n.accuracy >= 70 ? 'rgba(34,197,94,0.9)' : n.accuracy >= 40 ? 'rgba(245,158,11,0.9)' : 'rgba(239,68,68,0.9)';
        const bx = n.x - bw/2, by = n.y - r - 12;
        ctx.beginPath();
        if (ctx.roundRect) { ctx.roundRect(bx, by, bw, 13, 4); }
        else { ctx.rect(bx, by, bw, 13); }
        ctx.fill();
        ctx.fillStyle = '#fff';
        ctx.textAlign = 'center';
        ctx.fillText(badge, n.x, by + 10);
      }
    }
  }

  // Animation loop
  let frame = 0;
  function loop() {
    tick();
    // Auto-fit on the INITIAL settle only (guarded by _fitted so later drags,
    // which reset `frame`, never rescale the view): an early rough fit so it's
    // never the raw crammed view, then a precise fit once fully settled.
    if (!_fitted) {
      if (frame === 60) fitView();
      if (frame >= 349) { fitView(); _fitted = true; }
    }
    draw();
    frame++;
    if (frame < 350 || _dragNode) {
      _graphAnim = requestAnimationFrame(loop);
    } else {
      _graphAnim = null;
    }
  }
  _graphAnim = requestAnimationFrame(loop);

  function restartSim() {
    frame = 0;
    if (!_graphAnim) _graphAnim = requestAnimationFrame(loop);
  }

  // ── Hit testing ──
  function getNodeAt(mx, my) {
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const dx = mx - n.x, dy = my - n.y;
      if (dx * dx + dy * dy < (n.size + 6) * (n.size + 6)) return n;
    }
    return null;
  }
  function getEdgeAt(mx, my) {
    for (const e of edges) {
      const a = nodeMap[e.source], b = nodeMap[e.target];
      if (!a || !b) continue;
      const dx = b.x - a.x, dy = b.y - a.y;
      const len2 = dx*dx + dy*dy;
      if (len2 === 0) continue;
      let t = ((mx - a.x)*dx + (my - a.y)*dy) / len2;
      t = Math.max(0, Math.min(1, t));
      const px = a.x + t*dx, py = a.y + t*dy;
      const d = Math.sqrt((mx-px)*(mx-px) + (my-py)*(my-py));
      if (d < 8) return e;
    }
    return null;
  }
  function getMousePos(e) {
    // Return WORLD coordinates (inverse of the camera transform) so hit-testing
    // and node dragging keep working at any zoom/pan.
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    return { x: (sx - _cam.ox) / _cam.s, y: (sy - _cam.oy) / _cam.s };
  }

  // ── Context menu helpers ──
  function hideCtxMenu() { ctxMenu.style.display = 'none'; }
  function showCtxMenu(x, y, items) {
    ctxMenu.innerHTML = items.map(item => {
      if (item.divider) return '<div style="height:1px;background:rgba(0,0,0,0.08);margin:4px 0"></div>';
      const color = item.danger ? '#ef4444' : '#334155';
      return `<div class="graph-ctx-item" data-action="${item.action}" style="padding:8px 14px;border-radius:8px;cursor:pointer;display:flex;align-items:center;gap:8px;color:${color};transition:background 0.15s" onmouseenter="this.style.background='rgba(0,0,0,0.04)'" onmouseleave="this.style.background='transparent'">${item.icon || ''}${item.label}</div>`;
    }).join('');
    ctxMenu.style.display = 'block';
    const pr = canvas.parentElement.getBoundingClientRect();
    ctxMenu.style.left = Math.min(x, pr.width - 200) + 'px';
    ctxMenu.style.top = Math.min(y, pr.height - 200) + 'px';
    ctxMenu.querySelectorAll('.graph-ctx-item').forEach(el => {
      el.onclick = () => {
        const act = el.dataset.action;
        hideCtxMenu();
        items.find(i => i.action === act)?.handler?.();
      };
    });
  }

  // ── Node context menu actions ──
  async function deleteNode(node) {
    try {
      await api('POST', '/api/knowledge-graph/hide-node', { node_id: node.id });
    } catch(e) { toast(e.message, 'error'); return; }
    const idx = nodes.indexOf(node);
    if (idx !== -1) nodes.splice(idx, 1);
    delete nodeMap[node.id];
    edges = edges.filter(e => e.source !== node.id && e.target !== node.id);
    _hoverNode = null; _selectedNode = null;
    toast(`Removed "${node.label}"`, 'info');
    restartSim();
  }

  async function severEdge(edge) {
    try {
      await api('POST', '/api/knowledge-graph/hide-edge', { source: edge.source, target: edge.target });
    } catch(e) { toast(e.message, 'error'); return; }
    edges = edges.filter(e => e !== edge);
    toast('Connection severed', 'info');
    restartSim();
  }

  function startConnect(node) {
    _connectMode = true;
    _connectSource = node;
    connectBanner.style.display = 'block';
    if (!_graphAnim) draw();
  }

  async function finishConnect(targetNode) {
    if (!_connectSource || _connectSource === targetNode) return;
    const exists = edges.some(e =>
      (e.source === _connectSource.id && e.target === targetNode.id) ||
      (e.source === targetNode.id && e.target === _connectSource.id)
    );
    if (exists) {
      toast('Already connected', 'info');
    } else {
      try {
        await api('POST', '/api/knowledge-graph/add-edge', { source: _connectSource.id, target: targetNode.id });
        edges.push({ source: _connectSource.id, target: targetNode.id, custom: true });
        toast(`Connected "${_connectSource.label}" ↔ "${targetNode.label}"`, 'success');
      } catch(e) { toast(e.message, 'error'); }
    }
    _connectMode = false;
    _connectSource = null;
    connectBanner.style.display = 'none';
    restartSim();
  }

  // ── Event handlers (all assigned as properties — no addEventListener leaks) ──
  canvas.onmousemove = function(e) {
    // Panning the canvas (dragging empty space).
    if (_panning) {
      const rect = canvas.getBoundingClientRect();
      _cam.ox = _panOX + (e.clientX - rect.left - _panStartX);
      _cam.oy = _panOY + (e.clientY - rect.top  - _panStartY);
      tooltip.style.display = 'none';
      if (!_graphAnim) draw();
      return;
    }
    const { x, y } = getMousePos(e);
    if (_dragNode) {
      _dragNode.x = x; _dragNode.y = y;
      _dragNode.vx = 0; _dragNode.vy = 0;
      if (!_graphAnim) draw();
      return;
    }
    const n = getNodeAt(x, y);
    _hoverNode = n;
    canvas.style.cursor = _connectMode ? 'crosshair' : (n ? 'pointer' : 'grab');
    if (n) {
      let info = `<strong>${sEsc(n.label)}</strong><br>`;
      if (n.type === 'subject') info += '<span style="color:#a5b4fc">Subject</span>';
      else if (n.type === 'material') info += `<span style="color:#7dd3fc">Material</span> · ${sEsc(n.file_type || '')}`;
      else {
        if (n.attempts > 0) {
          const pct = n.accuracy;
          const bar = `<div style="background:rgba(255,255,255,0.15);border-radius:3px;height:4px;margin-top:4px;overflow:hidden"><div style="background:${pct>=70?'#22c55e':pct>=40?'#f59e0b':'#ef4444'};width:${pct}%;height:100%;border-radius:3px"></div></div>`;
          info += `Accuracy: <strong>${pct}%</strong><br>Attempts: ${n.attempts}${bar}`;
        } else {
          info += '<span style="color:#94a3b8">No quiz data yet</span>';
        }
      }
      tooltip.innerHTML = info;
      tooltip.style.display = 'block';
      const pr = canvas.parentElement.getBoundingClientRect();
      tooltip.style.left = (e.clientX - pr.left + 14) + 'px';
      tooltip.style.top = (e.clientY - pr.top - 12) + 'px';
    } else {
      tooltip.style.display = 'none';
    }
    if (!_graphAnim) draw();
  };

  canvas.onmousedown = function(e) {
    if (e.button === 2) return;
    hideCtxMenu();
    const { x, y } = getMousePos(e);
    const n = getNodeAt(x, y);
    if (_connectMode && n && n !== _connectSource) {
      finishConnect(n);
      return;
    }
    _dragNode = n;
    if (n) {
      canvas.style.cursor = 'grabbing';
      restartSim();
    } else {
      // Empty space → pan the camera.
      const rect = canvas.getBoundingClientRect();
      _panning = true;
      _panStartX = e.clientX - rect.left; _panStartY = e.clientY - rect.top;
      _panOX = _cam.ox; _panOY = _cam.oy;
      canvas.style.cursor = 'grabbing';
    }
  };

  canvas.onmouseup = function() {
    _dragNode = null; _panning = false;
    canvas.style.cursor = _connectMode ? 'crosshair' : (_hoverNode ? 'pointer' : 'grab');
  };
  canvas.onmouseleave = function() {
    _dragNode = null; _panning = false;
    tooltip.style.display = 'none';
    canvas.style.cursor = 'grab';
  };

  // Scroll to zoom, centred on the cursor.
  canvas.onwheel = function(e) {
    e.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left, sy = e.clientY - rect.top;
    const factor = Math.exp(-e.deltaY * 0.0015);
    const ns = Math.max(0.2, Math.min(2.5, _cam.s * factor));
    // Keep the world point under the cursor fixed while zooming.
    _cam.ox = sx - (sx - _cam.ox) * (ns / _cam.s);
    _cam.oy = sy - (sy - _cam.oy) * (ns / _cam.s);
    _cam.s = ns;
    if (!_graphAnim) draw();
  };

  // Double-click empty space → recenter / fit everything back into view.
  canvas.ondblclick = function(e) {
    const p = getMousePos(e);
    if (getNodeAt(p.x, p.y)) return; // ignore double-click on a node
    fitView();
    if (!_graphAnim) draw();
  };

  // ── RIGHT-CLICK: use oncontextmenu (replaces any previous handler) ──
  canvas.oncontextmenu = function(e) {
    e.preventDefault();
    e.stopPropagation();
    hideCtxMenu();
    const { x, y } = getMousePos(e);
    const node = getNodeAt(x, y);
    const edge = !node ? getEdgeAt(x, y) : null;
    const pr = canvas.parentElement.getBoundingClientRect();
    const menuX = e.clientX - pr.left;
    const menuY = e.clientY - pr.top;

    if (node) {
      const connEdges = edges.filter(ed => ed.source === node.id || ed.target === node.id);
      const items = [
        { label: `<strong>${sEsc(node.label)}</strong>`, action: 'noop', handler: () => {} },
        { divider: true },
        {
          icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>',
          label: 'Connect to…', action: 'connect',
          handler: () => startConnect(node)
        },
      ];
      if (connEdges.length > 0) {
        items.push({
          icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
          label: `Sever all (${connEdges.length})`, action: 'sever-all',
          handler: async () => {
            for (const ed of connEdges) {
              await api('POST', '/api/knowledge-graph/hide-edge', { source: ed.source, target: ed.target });
            }
            edges = edges.filter(ed => ed.source !== node.id && ed.target !== node.id);
            toast(`Severed ${connEdges.length} connections`, 'info');
            restartSim();
          }
        });
      }
      items.push({ divider: true });
      items.push({
        icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
        label: 'Remove node', action: 'delete', danger: true,
        handler: () => deleteNode(node)
      });
      showCtxMenu(menuX, menuY, items);
    } else if (edge) {
      const a = nodeMap[edge.source], b = nodeMap[edge.target];
      showCtxMenu(menuX, menuY, [
        { label: `<strong>${sEsc(a?.label||'?')} ↔ ${sEsc(b?.label||'?')}</strong>`, action: 'noop', handler: () => {} },
        { divider: true },
        {
          icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
          label: 'Sever connection', action: 'sever', danger: true,
          handler: () => severEdge(edge)
        }
      ]);
    }
    return false; // extra safety for preventing default
  };

  // ── Document-level listeners (with cleanup) ──
  function onDocClick(e) {
    if (!ctxMenu.contains(e.target)) hideCtxMenu();
  }
  function onDocKeydown(e) {
    if (e.key === 'Escape') {
      if (_connectMode) {
        _connectMode = false;
        _connectSource = null;
        connectBanner.style.display = 'none';
        if (!_graphAnim) draw();
      }
      hideCtxMenu();
    }
  }
  function onResize() {
    if (S.page === 'graph') {
      resize();
      W = canvas.clientWidth; H = canvas.clientHeight;
      if (!_graphAnim) draw();
    }
  }
  document.addEventListener('click', onDocClick);
  document.addEventListener('keydown', onDocKeydown);
  window.addEventListener('resize', onResize);

  // Cleanup function — called on next initGraphPage() to prevent listener leaks
  _graphCleanup = () => {
    document.removeEventListener('click', onDocClick);
    document.removeEventListener('keydown', onDocKeydown);
    window.removeEventListener('resize', onResize);
    canvas.onmousemove = null;
    canvas.onmousedown = null;
    canvas.onmouseup = null;
    canvas.onmouseleave = null;
    canvas.oncontextmenu = null;
    canvas.onwheel = null;
    canvas.ondblclick = null;
    tooltip.style.display = 'none';
    ctxMenu.style.display = 'none';
    connectBanner.style.display = 'none';
  };
}

// ── Compete: Leaderboard & Quiz Battles ──────────────────────────────────
let _competeTab = 'leaderboard';
let _activeBattleId = null;
let _battleAnswers = {};

async function initCompetePage() {
  showCompeteTab(_competeTab);
}

function showCompeteTab(tab) {
  _competeTab = tab;
  // Hide all sections
  document.getElementById('compete-leaderboard').classList.add('hidden');
  document.getElementById('compete-battles').classList.add('hidden');
  document.getElementById('battle-active').classList.add('hidden');
  document.getElementById('battle-results').classList.add('hidden');
  // Style tabs
  const lbBtn = document.getElementById('compete-tab-leaderboard');
  const btBtn = document.getElementById('compete-tab-battles');
  lbBtn.className = 'px-4 py-2 rounded-lg text-sm font-medium ' + (tab === 'leaderboard' ? 'text-white' : 'bg-slate-100 text-slate-600');
  lbBtn.style.background = tab === 'leaderboard' ? '#0f172a' : '';
  btBtn.className = 'px-4 py-2 rounded-lg text-sm font-medium ' + (tab === 'battles' ? 'text-white' : 'bg-slate-100 text-slate-600');
  btBtn.style.background = tab === 'battles' ? '#0f172a' : '';

  if (tab === 'leaderboard') {
    document.getElementById('compete-leaderboard').classList.remove('hidden');
    loadLeaderboard();
  } else {
    document.getElementById('compete-battles').classList.remove('hidden');
    loadBattles();
  }
}

async function loadLeaderboard() {
  const body = document.getElementById('leaderboard-body');
  const podium = document.getElementById('leaderboard-podium');
  // Skeleton while the leaderboard loads (#6)
  podium.innerHTML = '';
  body.innerHTML = `<tr><td colspan="5" class="p-3">${skelRows(4)}</td></tr>`;
  try {
    const data = await api('GET', '/api/leaderboard');

    // Empty state (#7) — nobody has answered anything yet
    if (!data.length) {
      body.innerHTML = `<tr><td colspan="5">${emptyState('🏆', 'No rankings yet', 'Answer quiz questions to claim your spot on the board.')}</td></tr>`;
      return;
    }

    // Podium for top 3
    const medals = ['🥇', '🥈', '🥉'];
    const podiumColors = ['bg-yellow-50 border-yellow-300', 'bg-slate-50 border-slate-300', 'bg-amber-50 border-amber-300'];
    const top3 = data.slice(0, 3);
    podium.innerHTML = top3.map((p, i) => `
      <div class="text-center p-4 rounded-xl border-2 ${podiumColors[i]} ${p.is_me ? 'ring-2 ring-emerald-500' : ''}">
        <div class="text-3xl mb-1">${medals[i]}</div>
        <div class="font-bold text-slate-800 ${p.is_me ? 'text-emerald-700' : ''}">${sEsc(p.username)}</div>
        <div class="text-2xl font-bold text-slate-700 mt-1">${p.total_correct}</div>
        <div class="text-xs text-slate-400">correct answers</div>
        <div class="text-xs text-slate-500 mt-1">${p.accuracy}% accuracy</div>
        ${p.streak > 0 ? `<div class="text-xs text-orange-500 mt-1">🔥 ${p.streak} day streak</div>` : ''}
      </div>
    `).join('');

    // Full table
    body.innerHTML = data.map(p => `
      <tr class="${p.is_me ? 'bg-emerald-50 font-semibold' : 'hover:bg-slate-50'}">
        <td class="p-3 text-slate-500">${p.rank}</td>
        <td class="p-3">
          <span class="${p.is_me ? 'text-emerald-800' : 'text-slate-700'}">${sEsc(p.username)}</span>
          ${p.is_me ? '<span class="text-xs text-emerald-600 ml-1">(you)</span>' : ''}
        </td>
        <td class="p-3 text-right font-medium">${p.total_correct}</td>
        <td class="p-3 text-right">${p.accuracy}%</td>
        <td class="p-3 text-right">${p.streak > 0 ? '🔥 ' + p.streak + 'd' : '-'}</td>
      </tr>
    `).join('');
  } catch(e) { body.innerHTML = ''; toast(e.message, 'error'); }
}

async function createBattle() {
  const topic = document.getElementById('battle-topic').value.trim();
  const count = document.getElementById('battle-count').value;
  if (!topic) { toast('Enter a topic for the battle', 'error'); return; }
  try {
    const b = await api('POST', '/api/battles', { topic, num_questions: parseInt(count) });
    toast(`Battle created! ${b.num_questions} questions on "${b.topic}"`, 'success');
    document.getElementById('battle-topic').value = '';
    loadBattles();
  } catch(e) { toast(e.message, 'error'); }
}

async function loadBattles() {
  const list = document.getElementById('battles-list');
  const empty = document.getElementById('battles-empty');
  // Skeleton while battles load (#6)
  empty.classList.add('hidden');
  list.innerHTML = skelRows(3);
  try {
    const battles = await api('GET', '/api/battles');

    // Empty state (#7) — no battles created yet
    if (!battles.length) {
      list.innerHTML = '';
      empty.innerHTML = emptyState('⚔️', 'No battles yet', 'Create one above and challenge your friends.');
      empty.classList.remove('hidden');
      return;
    }

    list.innerHTML = battles.map(b => {
      const pList = b.participants.map(p =>
        `<span class="${p.is_me ? 'text-emerald-700 font-medium' : 'text-slate-600'}">${sEsc(p.username)}${p.completed ? ' ✅ ' + p.score + '/' + p.total : ' ⏳'}</span>`
      ).join(', ');

      let actionBtn = '';
      if (b.i_completed) {
        actionBtn = `<button onclick="viewBattleResults(${b.id})" class="btn-secondary text-xs">View Results</button>`;
      } else if (b.i_joined) {
        actionBtn = `<button onclick="startBattle(${b.id})" class="btn-primary text-xs">Play Now</button>`;
      } else {
        actionBtn = `<button onclick="joinBattle(${b.id})" class="btn-primary text-xs">Join Battle</button>`;
      }

      return `<div class="card">
        <div class="flex items-start justify-between gap-3">
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <span class="text-lg">⚔️</span>
              <h3 class="font-semibold text-slate-700">${sEsc(b.topic)}</h3>
              <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">${b.num_questions} Qs</span>
            </div>
            <div class="text-xs text-slate-400 mt-1">by ${sEsc(b.creator)} · ${b.participants.length} player${b.participants.length !== 1 ? 's' : ''}</div>
            <div class="text-xs mt-2">${pList}</div>
          </div>
          ${actionBtn}
        </div>
      </div>`;
    }).join('');
  } catch(e) { list.innerHTML = ''; toast(e.message, 'error'); }
}

async function joinBattle(bid) {
  try {
    await api('POST', `/api/battles/${bid}/join`);
    toast('Joined!', 'success');
    loadBattles();
  } catch(e) { toast(e.message, 'error'); }
}

async function startBattle(bid) {
  try {
    const questions = await api('GET', `/api/battles/${bid}/questions`);
    _activeBattleId = bid;
    _battleAnswers = {};

    document.getElementById('compete-battles').classList.add('hidden');
    document.getElementById('battle-active').classList.remove('hidden');
    document.getElementById('battle-active-title').textContent = `Battle: ${questions.length} questions`;

    const container = document.getElementById('battle-questions');
    container.innerHTML = questions.map((q, i) => {
      const opts = q.options;
      return `<div class="card">
        <div class="flex gap-2 mb-2">
          <span class="text-xs font-bold text-slate-400">${i + 1}/${questions.length}</span>
          <span class="text-xs px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">${sEsc(q.topic)}</span>
        </div>
        <p class="font-medium text-slate-800 mb-3">${sEsc(q.question)}</p>
        <div class="space-y-2">
          ${opts.map(o => `
            <label class="flex items-center gap-3 p-3 rounded-lg border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50 cursor-pointer transition-all battle-option" data-qid="${q.id}" data-answer="${sEsc(o)}">
              <input type="radio" name="bq_${q.id}" value="${sEsc(o)}" onchange="setBattleAnswer(${q.id}, this.value)" class="accent-emerald-600" />
              <span class="text-sm text-slate-700">${sEsc(o)}</span>
            </label>
          `).join('')}
        </div>
      </div>`;
    }).join('');
  } catch(e) { toast(e.message, 'error'); }
}

function setBattleAnswer(qid, answer) {
  _battleAnswers[qid] = answer;
  // Highlight selected
  document.querySelectorAll(`[data-qid="${qid}"]`).forEach(el => {
    el.classList.toggle('border-emerald-500', el.dataset.answer === answer);
    el.classList.toggle('bg-emerald-50', el.dataset.answer === answer);
  });
}

function cancelBattle() {
  document.getElementById('battle-active').classList.add('hidden');
  document.getElementById('compete-battles').classList.remove('hidden');
  _activeBattleId = null;
  _battleAnswers = {};
}

async function submitBattleAnswers() {
  if (!_activeBattleId) return;
  const answered = Object.keys(_battleAnswers).length;
  const qCount = document.querySelectorAll('#battle-questions .card').length;
  if (answered < qCount && !confirm(`You've answered ${answered}/${qCount} questions. Submit anyway?`)) return;

  loading(true, 'Submitting battle answers...');
  try {
    const result = await api('POST', `/api/battles/${_activeBattleId}/submit`, { answers: _battleAnswers });
    showBattleResults(result);
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

function showBattleResults(result) {
  document.getElementById('battle-active').classList.add('hidden');
  document.getElementById('compete-battles').classList.add('hidden');
  document.getElementById('battle-results').classList.remove('hidden');

  const pct = Math.round(result.score / result.total * 100);
  document.getElementById('battle-score-display').textContent = `${result.score}/${result.total}`;
  document.getElementById('battle-score-subtitle').textContent = `${pct}% correct`;

  // Standings
  const standings = document.getElementById('battle-standings');
  standings.innerHTML = '<h3 class="font-semibold text-slate-700 mb-2">Standings</h3>' +
    result.standings.map((s, i) => `
      <div class="flex items-center justify-between py-2 ${i > 0 ? 'border-t border-slate-100' : ''}">
        <div class="flex items-center gap-2">
          <span class="text-lg">${i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i+1) + '.'}</span>
          <span class="font-medium text-slate-700">${sEsc(s.username)}</span>
          ${!s.completed ? '<span class="text-xs text-slate-400">(playing...)</span>' : ''}
        </div>
        <span class="font-bold ${i === 0 ? 'text-emerald-700' : 'text-slate-600'}">${s.completed ? s.score + '/' + s.total : '—'}</span>
      </div>
    `).join('');

  // Question review
  const review = document.getElementById('battle-review');
  review.innerHTML = '<h3 class="font-semibold text-slate-700 mb-2">Review</h3>' +
    result.results.map((r, i) => `
      <div class="card border-l-4 ${r.correct ? 'border-l-green-400' : 'border-l-red-400'}">
        <div class="flex items-center gap-2 mb-1">
          <span>${r.correct ? '✅' : '❌'}</span>
          <span class="text-xs text-slate-400">Q${i+1}</span>
        </div>
        ${!r.correct ? `<p class="text-sm text-slate-600"><strong>Your answer:</strong> ${sEsc(r.your_answer || '(skipped)')}</p>
        <p class="text-sm text-green-700"><strong>Correct:</strong> ${sEsc(r.correct_answer)}</p>` : ''}
        <p class="text-xs text-slate-500 mt-1">${sEsc(r.explanation)}</p>
      </div>
    `).join('');

  _activeBattleId = null;
  _battleAnswers = {};
}

async function viewBattleResults(bid) {
  // Re-fetch battle to show standings
  try {
    const battles = await api('GET', '/api/battles');
    const b = battles.find(x => x.id === bid);
    if (!b) return;

    document.getElementById('compete-battles').classList.add('hidden');
    document.getElementById('battle-results').classList.remove('hidden');

    const myP = b.participants.find(p => p.is_me);
    const pct = myP ? Math.round(myP.score / myP.total * 100) : 0;
    document.getElementById('battle-score-display').textContent = myP ? `${myP.score}/${myP.total}` : '-';
    document.getElementById('battle-score-subtitle').textContent = `${pct}% correct · ${sEsc(b.topic)}`;

    const standings = document.getElementById('battle-standings');
    standings.innerHTML = '<h3 class="font-semibold text-slate-700 mb-2">Standings</h3>' +
      b.participants.map((s, i) => `
        <div class="flex items-center justify-between py-2 ${i > 0 ? 'border-t border-slate-100' : ''}">
          <div class="flex items-center gap-2">
            <span class="text-lg">${i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : (i+1) + '.'}</span>
            <span class="font-medium ${s.is_me ? 'text-emerald-700' : 'text-slate-700'}">${sEsc(s.username)}${s.is_me ? ' (you)' : ''}</span>
          </div>
          <span class="font-bold ${i === 0 ? 'text-emerald-700' : 'text-slate-600'}">${s.completed ? s.score + '/' + s.total : '⏳'}</span>
        </div>
      `).join('');

    document.getElementById('battle-review').innerHTML = '';
  } catch(e) { toast(e.message, 'error'); }
}

// ── Sidebar collapse ──────────────────────────────────────────────────────
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  sb.classList.toggle('sb-collapsed');
  const prefs = getSettingsPrefs();
  prefs.sidebarCollapsed = sb.classList.contains('sb-collapsed');
  saveSettingsPrefs(prefs);
}

// ── Mobile sidebar drawer (#9) — off-canvas on small screens ─────────────
function toggleMobileSidebar(force) {
  const sb = document.getElementById('sidebar');
  const bd = document.getElementById('sidebar-backdrop');
  const btn = document.getElementById('mobile-menu-btn');
  const open = typeof force === 'boolean' ? force : !sb.classList.contains('mobile-open');
  sb.classList.toggle('mobile-open', open);
  if (bd) bd.classList.toggle('hidden', !open);
  if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
}
function closeMobileSidebar() { toggleMobileSidebar(false); }

// ── Settings — per-profile so each person keeps their own theme/font/subject ──
function prefsKey() {
  // Scoped to the active user; falls back to a shared key before login
  return S.userId ? `ua_prefs_${S.userId}` : 'ua_prefs';
}
function getSettingsPrefs() {
  try { return JSON.parse(localStorage.getItem(prefsKey()) || '{}'); } catch(e) { return {}; }
}
function saveSettingsPrefs(prefs) {
  localStorage.setItem(prefsKey(), JSON.stringify(prefs));
}

function applyTheme(name) {
  const t = THEMES[name] || THEMES.deepfocus;
  const r = document.documentElement;
  // Accent ramp — everything else (shell / canvas / ink) is fixed by the tokens.
  r.style.setProperty('--brand',        t.brand);
  r.style.setProperty('--brand-strong', t.brandStrong);
  r.style.setProperty('--brand-deep',   t.brandDeep);
  r.style.setProperty('--brand-soft',   t.brandSoft);
  // Legacy aliases still referenced by inline styles / older markup
  r.style.setProperty('--teal',            t.brandDeep);
  r.style.setProperty('--teal-d',          t.brandStrong);
  r.style.setProperty('--nav-active-bg',   t.brandSoft);
  r.style.setProperty('--nav-active-text', t.brand);

  // Light canvas everywhere (the writing room overrides its own background)
  document.body.style.background = THEME_CANVAS;

  // Hero banner gradient
  const hero = document.querySelector('#page-dashboard > .rounded-2xl');
  if (hero) hero.style.background = t.heroBg;

  // Retire the old floating-bubble layer if it's still in the DOM
  const layer = document.getElementById('bubble-layer');
  if (layer) layer.remove();

  // Update brand logo gradient
  const logo = document.querySelector('#sidebar .rounded-xl[style*="background"]');
  if (logo) logo.style.background = `linear-gradient(135deg,${t.brand},${t.brandDeep})`;
}

function setTheme(name) {
  applyTheme(name);
  document.querySelectorAll('.theme-card').forEach(s =>
    s.classList.toggle('active', s.dataset.theme === name));
  const prefs = getSettingsPrefs();
  prefs.theme = name;
  saveSettingsPrefs(prefs);
}

function renderThemePicker() {
  const prefs = getSettingsPrefs();
  const current = THEMES[prefs.theme] ? prefs.theme : 'deepfocus';
  const el = document.getElementById('theme-picker');
  if (!el) return;
  el.innerHTML = Object.entries(THEMES).map(([key, t]) => `
    <button class="theme-card ${key === current ? 'active' : ''}" data-theme="${key}" onclick="setTheme('${key}')">
      <div class="theme-card-preview" style="background:${THEME_CANVAS}">
        <div class="theme-card-mockup" style="background:${THEME_CANVAS}">
          <div class="theme-mock-sidebar" style="background:${THEME_SHELL}">
            <div style="width:14px;height:14px;border-radius:5px;background:linear-gradient(135deg,${t.brand},${t.brandDeep});margin-bottom:8px"></div>
            <div style="width:100%;height:3px;border-radius:2px;background:${t.brand};margin-bottom:4px"></div>
            <div style="width:70%;height:3px;border-radius:2px;background:rgba(255,255,255,0.2)"></div>
          </div>
          <div class="theme-mock-content">
            <div class="theme-mock-hero" style="background:${t.heroBg}"></div>
            <div style="display:flex;gap:3px;margin-top:4px">
              <div style="flex:1;height:14px;border-radius:4px;background:#ffffff;border:1px solid #e2e8f0"></div>
              <div style="flex:1;height:14px;border-radius:4px;background:#ffffff;border:1px solid #e2e8f0"></div>
            </div>
            <div style="height:18px;border-radius:5px;background:#ffffff;border:1px solid #e2e8f0;margin-top:3px"></div>
          </div>
        </div>
      </div>
      <div class="theme-card-footer">
        <span class="theme-card-name">${t.name}</span>
        <span class="theme-card-dot" style="background:${t.brand}"></span>
      </div>
    </button>`).join('');
}

function initSettingsPage() {
  renderThemePicker();
  const prefs = getSettingsPrefs();
  if (prefs.fontSize) {
    const sel = document.getElementById('settings-font-size');
    if (sel) sel.value = prefs.fontSize;
  }
  if (prefs.defaultSubject) {
    const el = document.getElementById('settings-default-subject');
    if (el) el.value = prefs.defaultSubject;
  }
  loadNetworkInfo();
}

async function loadNetworkInfo() {
  const el = document.getElementById('network-info-list');
  if (!el) return;
  try {
    const data = await fetch('/api/network-info').then(r => r.json());
    let html = '';

    // Cloudflare tunnel URL (internet — shown first and prominently)
    if (data.tunnel_url) {
      html += `
        <div class="p-3 bg-emerald-50 rounded-xl border border-emerald-200 mb-3">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold uppercase tracking-widest text-emerald-700">🌐 Internet (Cloudflare Tunnel)</span>
            <span class="text-xs text-emerald-400">— live now</span>
          </div>
          <div class="flex items-center gap-2">
            <code class="flex-1 text-sm font-mono text-emerald-800 break-all">${data.tunnel_url}</code>
            <button onclick="navigator.clipboard.writeText('${data.tunnel_url}').then(()=>toast('Tunnel URL copied!','success'))"
              class="text-xs bg-emerald-500 hover:bg-emerald-700 text-white font-semibold px-3 py-1.5 rounded-lg flex-shrink-0">Copy</button>
          </div>
          <p class="text-emerald-700 text-xs mt-1.5">Send this to anyone — works from anywhere in the world. Runs automatically on startup.</p>
        </div>`;
    } else {
      html += `<div class="p-3 bg-amber-50 rounded-xl border border-amber-200 mb-3 text-sm text-amber-700">
        ⏳ Tunnel is starting up… refresh in a few seconds.
      </div>`;
    }

    // LAN addresses (same Wi-Fi only)
    if (data.ips && data.ips.length) {
      html += data.ips.map(ip => `
        <div class="flex items-center gap-3 p-3 bg-slate-50 rounded-xl border border-slate-200">
          <div class="flex-1 min-w-0">
            <div class="text-xs text-slate-400 mb-0.5">Same Wi-Fi only</div>
            <code class="text-sm font-mono text-slate-700">http://${ip}:${data.port}</code>
          </div>
          <button onclick="navigator.clipboard.writeText('http://${ip}:${data.port}').then(()=>toast('URL copied!','success'))"
            class="text-xs text-emerald-700 hover:text-emerald-800 font-medium flex-shrink-0">Copy</button>
        </div>`).join('');
    }
    el.innerHTML = html || `<p class="text-slate-400 text-sm">No network addresses found.</p>`;
  } catch(e) {
    el.innerHTML = `<p class="text-slate-400 text-sm">Could not detect network address.</p>`;
  }
}

function saveSettingsFontSize() {
  const size = document.getElementById('settings-font-size').value;
  document.documentElement.style.setProperty('--base-font', size);
  const prefs = getSettingsPrefs();
  prefs.fontSize = size;
  saveSettingsPrefs(prefs);
  toast('Text size updated!', 'success');
}

function saveSettingsSubject() {
  const subject = document.getElementById('settings-default-subject').value.trim();
  const prefs = getSettingsPrefs();
  prefs.defaultSubject = subject;
  saveSettingsPrefs(prefs);
  const uploadEl = document.getElementById('upload-subject');
  if (uploadEl && subject) uploadEl.value = subject;
  toast('Default subject saved!', 'success');
}

function loadSettingsPrefs() {
  const prefs = getSettingsPrefs();
  applyTheme(prefs.theme || 'deepfocus');
  if (prefs.fontSize) document.documentElement.style.setProperty('--base-font', prefs.fontSize);
  if (prefs.defaultSubject) {
    const uploadEl = document.getElementById('upload-subject');
    if (uploadEl) uploadEl.value = prefs.defaultSubject;
  }
  if (prefs.sidebarCollapsed) {
    document.getElementById('sidebar')?.classList.add('sb-collapsed');
  }
}

// ── Copy-for-Claude (one-click: snapshot current page context, copy, confirm) ──
async function quickCopyContext() {
  const fab = document.getElementById('claude-fab');
  if (fab) { fab.disabled = true; }

  try {
    // Auto-detect which material the user is currently looking at
    const mid = currentPageMaterialId() || '';
    const url = mid ? `/api/context/export?material_id=${mid}` : '/api/context/export';
    const b = await api('GET', url, null, { quiet: true }); // catch below shows a richer toast

    // Build the context — always include everything (user asked for one-click, no checkboxes)
    const text = formatClaudeContext(b, { wantWeak: true, wantMissed: true, wantStats: true });

    // Copy to clipboard
    try {
      await navigator.clipboard.writeText(text);
    } catch(e) {
      // Fallback for Safari / older browsers
      const ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.focus(); ta.select();
      document.execCommand('copy');
      document.body.removeChild(ta);
    }

    showClaudeSnack(b, text.length);
  } catch(e) {
    toast('Could not build context: ' + e.message, 'error');
  } finally {
    if (fab) { fab.disabled = false; }
  }
}

function showClaudeSnack(bundle, chars) {
  // Build a one-line summary of what was included
  const parts = [];
  if (bundle.material) parts.push(bundle.material.name);
  if (bundle.weak_topics && bundle.weak_topics.length) parts.push(`${bundle.weak_topics.length} weak topics`);
  if (bundle.missed && bundle.missed.length) parts.push(`${bundle.missed.length} missed Qs`);
  if (bundle.due_today) parts.push(`${bundle.due_today} cards due`);

  const snack = document.getElementById('claude-snack');
  const meta  = document.getElementById('claude-snack-meta');
  if (!snack) return;

  meta.textContent = (parts.length ? parts.join(' · ') + ' — ' : '')
    + `${chars.toLocaleString()} chars · free on Claude.ai`;

  // Show the snack
  snack.classList.remove('hidden');

  // Auto-dismiss after 9 s
  clearTimeout(window._snackTimer);
  window._snackTimer = setTimeout(hideClaudeSnack, 9000);
}

function hideClaudeSnack() {
  const snack = document.getElementById('claude-snack');
  if (snack) snack.classList.add('hidden');
  clearTimeout(window._snackTimer);
}

function currentPageMaterialId() {
  const ids = ['fc-material-select','quiz-material-select','slides-material-select','mm-material-select','tutor-material-select'];
  for (const id of ids) {
    const el = document.getElementById(id);
    if (el && el.value) return el.value;
  }
  return '';
}

function formatClaudeContext(b, opts) {
  const subject = (b.material && b.material.subject) || 'my course';
  let out = `I'm a student studying ${subject}. Below is my study context exported from my study app (MedVault). `
          + `Please use it to help me — answer questions, quiz me, and explain my weak areas.\n`;

  if (b.material) {
    out += `\n## Study material: ${b.material.name}\n${b.material.content}\n`;
  }
  if (opts.wantStats) {
    out += `\n## My overall performance\n`;
    out += `- Quiz accuracy: ${b.accuracy}% across ${b.total_questions} questions\n`;
    out += `- Flashcards due today: ${b.due_today}\n`;
  }
  if (opts.wantWeak && b.weak_topics && b.weak_topics.length) {
    out += `\n## My weakest topics (lowest quiz accuracy)\n`;
    b.weak_topics.forEach(t => { out += `- ${t.topic}: ${t.pct}% (${t.correct}/${t.attempts})\n`; });
  }
  if (opts.wantMissed && b.missed && b.missed.length) {
    out += `\n## Questions I recently got wrong\n`;
    b.missed.forEach((m, i) => {
      out += `${i+1}. ${m.question}\n   Correct answer: ${m.correct_answer}\n`;
      if (m.explanation) out += `   Explanation: ${m.explanation}\n`;
    });
  }
  out += `\n---\nMy question / what I need help with:\n`;
  return out;
}

function openClaudeWeb() {
  window.open('https://claude.ai/new', '_blank');
}

// ── Access code gate (internet-facing protection) ───────────────────────────
function showAccessGate() {
  document.getElementById('access-gate').classList.remove('hidden');
  const input = document.getElementById('access-code-input');
  if (input) { input.value = ''; setTimeout(() => input.focus(), 50); }
  document.getElementById('access-code-error').classList.add('hidden');
}

async function submitAccessCode() {
  const input = document.getElementById('access-code-input');
  const code  = (input?.value || '').trim();
  if (!code) return;
  // Test the code against the server
  try {
    const res = await fetch('/api/access-check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Access-Code': code },
      body: JSON.stringify({ code }),
    });
    if (res.ok) {
      sessionStorage.setItem('ua_access_code', code);
      localStorage.setItem('ua_access_code', code);
      document.getElementById('access-gate').classList.add('hidden');
      // Continue boot
      boot();
    } else {
      document.getElementById('access-code-error').classList.remove('hidden');
      input.select();
    }
  } catch(e) {
    document.getElementById('access-code-error').classList.remove('hidden');
  }
}

// ── Auth (login / register with passwords) ──────────────────────────────────
let _profiles = [];
let _authMode = 'login'; // 'login' or 'register'

async function showProfileGate() {
  document.getElementById('profile-gate').classList.remove('hidden');
  try {
    _profiles = await fetch('/api/profiles').then(r => r.json());
  } catch(e) { _profiles = []; }
  _authMode = _profiles.length ? 'login' : 'register';
  renderAuthUI();
}

function renderAuthUI() {
  const el = document.getElementById('profile-list');
  const isLogin = _authMode === 'login';
  el.innerHTML = `
    <div class="w-full max-w-xs mx-auto text-left">
      <div class="flex mb-4 rounded-lg overflow-hidden border border-white/20">
        <button id="tab-login" onclick="_authMode='login';renderAuthUI()"
          class="flex-1 py-2 text-sm font-semibold transition-colors ${isLogin ? 'text-white' : 'bg-white/5 text-slate-400 hover:text-white'}"
          style="${isLogin ? 'background:#0891b2' : ''}">
          Log in
        </button>
        <button id="tab-register" onclick="_authMode='register';renderAuthUI()"
          class="flex-1 py-2 text-sm font-semibold transition-colors ${!isLogin ? 'text-white' : 'bg-white/5 text-slate-400 hover:text-white'}"
          style="${!isLogin ? 'background:#0891b2' : ''}">
          Sign up
        </button>
      </div>
      ${_profiles.length && isLogin ? `
        <div class="flex flex-wrap gap-2 mb-4 justify-center">
          ${_profiles.map(p => `
            <button data-uname="${sEsc(p.username)}" class="profile-card px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm transition-colors">
              <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-emerald-600 text-white text-xs font-bold mr-1.5">${(p.username[0]||'?').toUpperCase()}</span>
              ${sEsc(p.username)}
            </button>`).join('')}
        </div>` : ''}
      <input id="auth-username" class="w-full px-4 py-3 rounded-xl bg-white/10 text-white placeholder-slate-400 border border-white/20 text-sm outline-none focus:border-emerald-500 mb-3"
        placeholder="Username" maxlength="40" autocomplete="username" />
      <input id="auth-password" type="password" class="w-full px-4 py-3 rounded-xl bg-white/10 text-white placeholder-slate-400 border border-white/20 text-sm outline-none focus:border-emerald-500 mb-3"
        placeholder="Password" autocomplete="${isLogin ? 'current-password' : 'new-password'}" />
      <p id="auth-error" class="text-red-400 text-sm mb-3 hidden"></p>
      <button onclick="submitAuth()" class="w-full py-3 rounded-xl font-semibold text-white text-sm"
        style="background:var(--teal)">${isLogin ? 'Log in' : 'Create account'} →</button>
      <p class="text-slate-500 text-xs text-center mt-4">
        ${isLogin ? "Don't have an account?" : 'Already have an account?'}
        <a href="#" onclick="_authMode='${isLogin ? 'register' : 'login'}';renderAuthUI();return false" class="text-emerald-400 hover:underline">
          ${isLogin ? 'Sign up' : 'Log in'}
        </a>
      </p>
    </div>`;

  // Quick-fill username when clicking a profile card
  el.querySelectorAll('[data-uname]').forEach(b => {
    b.addEventListener('click', () => {
      document.getElementById('auth-username').value = b.dataset.uname;
      document.getElementById('auth-password').focus();
    });
  });

  // Enter key submits
  ['auth-username','auth-password'].forEach(id => {
    const inp = document.getElementById(id);
    if (inp) inp.onkeydown = e => { if (e.key === 'Enter') submitAuth(); };
  });

  // Auto-focus
  setTimeout(() => {
    const u = document.getElementById('auth-username');
    if (u) u.focus();
  }, 50);
}

async function submitAuth() {
  const username = (document.getElementById('auth-username').value || '').trim();
  const password = document.getElementById('auth-password').value;
  const errEl = document.getElementById('auth-error');
  errEl.classList.add('hidden');

  if (!username) { errEl.textContent = 'Enter a username'; errEl.classList.remove('hidden'); return; }
  if (password.length < 4) { errEl.textContent = 'Password must be at least 4 characters'; errEl.classList.remove('hidden'); return; }

  const endpoint = _authMode === 'register' ? '/api/register' : '/api/login';
  try {
    const ac = sessionStorage.getItem('ua_access_code');
    const headers = { 'Content-Type': 'application/json' };
    if (ac) headers['X-Access-Code'] = ac;
    const res = await fetch(endpoint, {
      method: 'POST', headers,
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      if (err.detail === 'access_code_required') {
        showAccessGate();
        return;
      }
      throw new Error(err.detail || 'Request failed');
    }
    const data = await res.json();
    loginAs(data.id, data.username, data.token);
    if (data.password_set) toast('Password set for existing profile!', 'success');
  } catch(e) {
    errEl.textContent = e.message;
    errEl.classList.remove('hidden');
  }
}

function loginAs(id, username, token) {
  S.userId = String(id);
  S.username = username;
  localStorage.setItem('ua_user', JSON.stringify({ id, username }));
  if (token) localStorage.setItem('ua_token', token);
  document.getElementById('profile-gate').classList.add('hidden');
  updateProfileDisplay();
  loadSettingsPrefs();
  bootApp();
}

function switchProfile() {
  // Logout: clear token on server + local
  const token = localStorage.getItem('ua_token');
  if (token) {
    const ac = sessionStorage.getItem('ua_access_code');
    const headers = { 'Authorization': 'Bearer ' + token };
    if (ac) headers['X-Access-Code'] = ac;
    fetch('/api/logout', { method: 'POST', headers }).catch(() => {});
  }
  localStorage.removeItem('ua_user');
  localStorage.removeItem('ua_token');
  S.userId = null; S.username = null;
  S.materials = [];
  showProfileGate();
}

function updateProfileDisplay() {
  const nameEl = document.getElementById('current-profile-name');
  const avEl   = document.getElementById('current-profile-avatar');
  if (nameEl) nameEl.textContent = S.username || '';
  if (avEl)   avEl.textContent   = (S.username || '?')[0].toUpperCase();
}

// ── Discover (shared public materials) ──────────────────────────────────────
async function initDiscoverPage() {
  const el = document.getElementById('discover-list');
  el.innerHTML = skelRows(3);
  try {
    const mats = await api('GET', '/api/discover', null, { quiet: true }); // error shown inline below
    renderDiscover(mats);
  } catch(e) { el.innerHTML = `<p class="text-red-400 text-sm">${e.message}</p>`; }
}

function renderDiscover(mats) {
  const el = document.getElementById('discover-list');
  if (!mats.length) {
    el.innerHTML = emptyState('🌐', 'Nothing shared yet',
      'When someone marks a material public (Materials → 🔒/🌐 toggle), it appears here.');
    return;
  }
  const icons = { pdf: '📄', pptx: '📊', image: '🖼️', web: '🌐' };
  el.innerHTML = mats.map(m => `
    <div class="flex items-start gap-3 p-3 rounded-xl border border-slate-100 bg-slate-50 hover:bg-white transition-colors">
      <div class="text-2xl flex-shrink-0 mt-0.5">${icons[m.file_type] || '📁'}</div>
      <div class="flex-1 min-w-0">
        <div class="font-medium text-slate-700 truncate text-sm">${sEsc(m.original_name)}</div>
        <div class="text-xs text-slate-400 mt-0.5">${sEsc(m.subject)} · shared by ${sEsc(m.owner_name || 'someone')} · ${Math.round(m.chars/1000)}k chars</div>
      </div>
      <button onclick="addDiscovered(${m.id})" class="gen-btn flex-shrink-0 self-center">+ Add to my library</button>
    </div>`).join('');
}

async function addDiscovered(mid) {
  try {
    const res = await api('POST', `/api/materials/${mid}/add`);
    toast(res.already ? 'Already in your library' : "Added — copied the owner's cards, quiz & slides", 'success');
    await loadMaterials();
    initDiscoverPage();
  } catch(e) { toast(e.message, 'error'); }
}

async function toggleVisibility(mid, current) {
  const next = current === 'public' ? 'private' : 'public';
  try {
    await api('POST', `/api/materials/${mid}/visibility`, { visibility: next });
    toast(next === 'public'
      ? 'Now public — others can find it in Discover'
      : 'Now private — only you can see it', 'success');
    loadMaterials();
  } catch(e) { toast(e.message, 'error'); }
}

// ── Boot ────────────────────────────────────────────────────────────────────
async function bootApp() {
  try { S.materials = await api('GET', '/api/materials', null, { quiet: true }); } catch(e) {}
  showPage('dashboard');
}

// Named so the access gate can call it after the code is validated
async function boot() {
  const stored = (() => { try { return JSON.parse(localStorage.getItem('ua_user') || 'null'); } catch(e) { return null; } })();
  const token = localStorage.getItem('ua_token');

  // If we have a token, verify it's still valid by hitting any authed endpoint
  if (stored && stored.id && token) {
    try {
      const ac = sessionStorage.getItem('ua_access_code');
      const headers = { 'Authorization': 'Bearer ' + token };
      if (ac) headers['X-Access-Code'] = ac;
      const res = await fetch('/api/materials', { headers });
      if (res.ok) {
        S.userId = String(stored.id);
        S.username = stored.username;
        S.materials = await res.json();
        loadSettingsPrefs();
        updateProfileDisplay();
        showPage('dashboard');
        return;
      }
      // Token expired — clear it
      localStorage.removeItem('ua_token');
    } catch(e) {}
  }

  loadSettingsPrefs();
  showProfileGate();
}

(async () => {
  // 1. Check if an access code is required before anything else
  try {
    const info = await fetch('/api/access-check').then(r => r.json());
    if (info.required) {
      const stored = sessionStorage.getItem('ua_access_code');
      if (!stored) { showAccessGate(); return; }
      // Verify the stored code is still valid
      const check = await fetch('/api/access-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Access-Code': stored },
        body: JSON.stringify({ code: stored }),
      });
      if (!check.ok) { sessionStorage.removeItem('ua_access_code'); showAccessGate(); return; }
    }
  } catch(e) { /* server unreachable — proceed anyway */ }

  // 2. Access OK — restore profile and boot
  boot();
})();


/* ══════════════════════════════════════════════════════════════
   RUSSIAN — phased curriculum + SM-2 vocab drilling + browser TTS
   Zero-API: curriculum text is static, audio is the browser's ru-RU
   voice, and scheduling reuses the backend's shared sm2_schedule().
   ══════════════════════════════════════════════════════════════ */
const RU = {
  inited: false, tab: '0', voice: null, words: [], byPhase: {},
  stats: null, activeCat: 'all',
  drill: { cards: [], idx: 0, correct: 0, flipped: false, scope: -1 },
  pron: { stageIdx: 0, itemIdx: 0, listening: false, last: null }, pronPassed: {},
};

const RU_CATS = {
  letters: 'Alphabet', greetings: 'Greetings', intro: 'Introductions',
  politeness: 'Politeness', pronouns: 'Pronouns', numbers: 'Numbers',
  family: 'Family', colors: 'Colours', time: 'Days, months & time',
  verbs: 'Verbs', adjectives: 'Adjectives',
  food: 'Food & drink', shopping: 'Shopping', directions: 'Directions & transport',
  places: 'Places', lodging: 'Lodging',
  questions: 'Question words', conversation: 'Conversation',
  weather: 'Weather', body: 'Body & health', home: 'Home & objects',
  grammar: 'Grammar', vocab: 'Vocabulary',
};

// The 5-phase roadmap — content straight from the study spec (static, zero-API).
const RU_CURRICULUM = [
  {
    n: 0, icon: '①', short: 'Alphabet', title: 'The Alphabet (Cyrillic)', time: '~1–2 weeks',
    objective: 'Read and sound out any Russian word, even one you don’t know. This comes first and is non-negotiable — every later phase assumes you can read Cyrillic.',
    success: 'You can read мама, кофе, ресторан, метро, спасибо aloud without decoding letter by letter. Slow is fine — accuracy beats speed.',
    learn: [
      '<b>Look-alikes</b> first (А Е К М О Т) — same shape and sound as English.',
      '<b>False friends</b> that trip up everyone: В=v, Н=n, Р=rolled r, С=s, У=oo, Х=kh.',
      '<b>Brand-new letters</b> — learn the sound each makes; watch Ж=“zh”, Щ vs Ш, Я=“ya”, Ю=“yu”, Е=“ye”, Ё=“yo”.',
      '<b>Signs &amp; Ы</b>: Ъ (hard, silent), Ь (soft, silent — softens the letter before it), Ы (hard “i”, no English equivalent — lean on the audio).',
    ],
    resources: [
      { name: 'LearnRussianFree — Alphabet (audio, quiz, colour-coded)', url: 'https://learnrussianfree.com/alphabet/', note: 'All 33 letters with clickable audio and a quiz.' },
      { name: 'Learn Russian Alphabet — interactive game', url: 'https://learn-russian-alphabet.com/', note: 'Learn, then test each letter.' },
      { name: 'RussianForFree — How to read Russian', url: 'https://www.russianforfree.com/lessons-how-to-read-in-russian-01.php', note: 'Reading lessons that build up from the letters.' },
      { name: 'Refold — free Anki alphabet deck (native audio)', url: 'https://refold.la/blog/unlock-the-secrets-of-the-russian-alphabet-with-refolds-free-flashcards', note: 'Or just use the tappable grid + mic practice below.' },
    ],
  },
  {
    n: 1, icon: '②', short: 'Survival', title: 'Survival Basics', time: '~1–2 weeks',
    objective: 'Introduce yourself, be polite, count, and produce recognizable Russian sounds.',
    success: 'You can walk up to someone, greet them, say your name and where you’re from, and thank them — entirely in Russian, out loud.',
    learn: [
      '<b>Greetings:</b> Привет (informal), Здравствуйте (formal), Пока, До свидания — Russian takes the formal/informal split seriously.',
      '<b>Introduce yourself:</b> Меня зовут… , Я из… , Очень приятно.',
      '<b>Politeness:</b> Спасибо, Пожалуйста, Извините, Да / Нет.',
      '<b>Numbers</b> 0–20, then tens to 100 — constant for prices, time, quantities.',
      '<b>Pronunciation — vowel reduction:</b> unstressed О sounds like “a” (молоко ≈ “ma-la-KO”). Start noticing the stressed syllable.',
    ],
    resources: [
      { name: 'LearnRussianFree — Beginner start', url: 'https://learnrussianfree.com/beginner/', note: 'Cyrillic, first phrases and quizzes with audio.' },
      { name: 'RuSource — A1 (Beginner / Survival), curated', url: 'https://rusource.org/levels/A1', note: 'Hand-picked free A1 grammar & vocab.' },
      { name: 'RussianPod101 — Survival phrases', url: 'https://www.russianpod101.com/lesson-library/before-you-travel-to-russia-survival-russian-phrases', note: 'Greetings, politeness, essentials (freemium).' },
      { name: 'Duolingo Russian (free)', url: 'https://www.duolingo.com/course/ru/en/Learn-Russian', note: 'Say everything aloud — don’t just tap.' },
    ],
  },
  {
    n: 2, icon: '③', short: 'Travel', title: 'Travel & Everyday', time: 'longest phase · 1–2 hrs/day',
    objective: 'Handle the real traveler situations — food, shopping, directions, transport, lodging. The practical heart of the plan.',
    success: 'You can role-play ordering a meal, asking a price, and asking for directions, and mostly be understood.',
    learn: [
      '<b>Food:</b> Я хочу… , reading a menu, Счёт, пожалуйста.',
      '<b>Shopping:</b> Сколько стоит? , У вас есть…? , understanding numbers said back to you.',
      '<b>Directions &amp; transport:</b> Где…? , налево / направо / прямо, metro &amp; taxi words.',
      '<b>Lodging:</b> У меня бронь, asking about the room.',
      '<b>Grammar (go slow):</b> noun gender by ending, present tense, and your first two cases — accusative (the object) and prepositional (location). Don’t chase all six yet.',
    ],
    resources: [
      { name: 'MasterRussian — Phrasebook (hotel, food, shopping, doctor)', url: 'http://masterrussian.com/blphrasebook.shtml', note: 'Situational travel phrases by topic.' },
      { name: 'Wikivoyage — Russian phrasebook', url: 'https://en.wikivoyage.org/wiki/Russian_phrasebook', note: 'Traveller phrases organised by situation.' },
      { name: 'FSI Russian on Live Lingua — full textbook + audio', url: 'https://www.livelingua.com/project/fsi/russian', note: 'Free, no sign-up; work through units steadily.' },
    ],
  },
  {
    n: 3, icon: '④', short: 'Conversation', title: 'Conversation', time: 'open-ended · 1–2 hrs/day',
    objective: 'Hold a simple back-and-forth and understand slow, clear speech.',
    success: 'You can have a slow but real exchange with a patient native speaker — introduce yourself, ask and answer questions, talk about your day.',
    learn: [
      '<b>Past &amp; future tense</b> — past is easier than present (it agrees with gender/number, not person).',
      '<b>The remaining cases:</b> genitive (of / negation), dative (to/for), instrumental (with). The big hurdle — one case at a time over weeks.',
      '<b>Question words, fluidly:</b> Что, Где, Когда, Почему, Как.',
      '<b>Active practice:</b> one real conversation a week (start by text, move to voice). Mistakes are the point.',
      '<b>Daily listening</b> to slow-Russian podcasts / YouTube to train your ear.',
    ],
    resources: [
      { name: 'RussianPod101 — Absolute Beginner library', url: 'https://www.russianpod101.com/lesson-library/absolute-beginner', note: 'Short dialogues to train your ear (freemium).' },
      { name: 'Tandem — language exchange with native speakers', url: 'https://www.tandem.net/', note: 'Pair with daily slow-Russian listening.' },
    ],
  },
  {
    n: 4, icon: '⑤', short: 'Maintain', title: 'Maintain & Grow', time: 'ongoing',
    objective: 'Keep improving through consistent, enjoyable exposure so you don’t lose what you built.',
    success: 'Russian is a maintained habit, not a course you finish. Progress continues as long as the daily exposure does.',
    learn: [
      'Keep the <b>daily drill habit</b> — reviews never stop, even at 10 min/day.',
      'Watch <b>Russian shows/films with subtitles</b> to keep your ear sharp.',
      'Keep <b>weekly conversation</b> going (Tandem partner or a tutor).',
      'Read <b>simple / graded native texts</b> to grow vocabulary in context.',
      'Set your <b>next concrete milestone</b> — e.g. reach A2, or “hold a 5-minute conversation on my trip.”',
    ],
    maintain: [
      'Daily: 10–15 min of drills (reviews first, then a few new cards).',
      'Daily: 5–10 min of Russian audio/video with subtitles.',
      'Weekly: one 20–30 min conversation with a partner or tutor.',
      'Weekly: read one short graded/native text.',
      'Monthly: check progress against your next milestone.',
    ],
    resources: [
      { name: 'OpenRussian — top-500 words (free dictionary)', url: 'https://en.openrussian.org/top-500', note: 'Look up any word: audio, examples, declensions.' },
      { name: 'MasterRussian — 1000 most common words', url: 'http://masterrussian.com/vocabulary/most_common_words.htm', note: 'Frequency list to keep growing vocabulary.' },
      { name: 'Anki (optional) — decks outside MedVault', url: 'https://apps.ankiweb.net/', note: 'Your Drill tab already does spaced repetition.' },
    ],
  },
];

async function initRussianPage() {
  if (!RU.inited) {
    RU.inited = true;
    ruPickVoice();
    ruPronLoadPassed();
    if (window.speechSynthesis) speechSynthesis.onvoiceschanged = () => { ruPickVoice(); };
    // one delegated speaker: any [data-speak] element speaks its text when clicked;
    // clicking a letter tile also jumps the pronunciation practice to that letter.
    document.getElementById('page-russian')?.addEventListener('click', (e) => {
      const s = e.target.closest('[data-speak]');
      if (s) ruSpeakText(s.getAttribute('data-speak'), s);
      const tile = e.target.closest('.ru-letter[data-pron-cyr]');
      if (tile) ruPronounceJump(tile.getAttribute('data-pron-cyr'));
    });
    // drill keyboard: Space flips · 1 = didn't know · 2 = got it
    document.addEventListener('keydown', (e) => {
      if (S.page !== 'russian' || RU.tab !== 'drill') return;
      const tag = document.activeElement?.tagName?.toLowerCase();
      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      const panel = document.getElementById('ru-panel-drill');
      if (!panel || panel.classList.contains('hidden')) return;
      if (e.code === 'Space') { e.preventDefault(); ruFlip(); }
      else if (RU.drill.flipped && e.key === '2') { e.preventDefault(); ruGrade(true); }
      else if (RU.drill.flipped && e.key === '1') { e.preventDefault(); ruGrade(false); }
    });
  }
  await ruLoadWords();     // lazy-seeds the starter deck server-side on first GET
  await ruLoadStats();
  ruShowTab(RU.tab || '0');
}

function ruIndexWords() {
  RU.byPhase = {};
  RU.words.forEach(w => { (RU.byPhase[w.phase] = RU.byPhase[w.phase] || []).push(w); });
}

async function ruLoadWords() {
  try {
    const res = await api('GET', '/api/russian/vocab', null, { quiet: true });
    RU.words = Array.isArray(res.words) ? res.words : [];
  } catch (e) { RU.words = []; }
  ruIndexWords();
}

async function ruLoadStats() {
  try { RU.stats = await api('GET', '/api/russian/stats', null, { quiet: true }); }
  catch (e) { RU.stats = null; }
  ruRenderProgress();
  ruUpdateBadges();
}

function ruUpdateBadges() {
  const due = RU.stats?.due_today ?? 0;
  const set = (id, n) => {
    const el = document.getElementById(id);
    if (el) { el.textContent = n ? n : ''; el.style.display = n ? '' : 'none'; }
  };
  set('ru-nav-due', due);
  set('ru-drill-due', due);
  const hs = document.getElementById('ru-headline-stats');
  if (hs && RU.stats) {
    hs.innerHTML = `<span><b>${RU.stats.due_today}</b> due</span>` +
      `<span><b>${RU.stats.learned}</b> learned</span>` +
      `<span><b>${RU.stats.total}</b> cards</span>`;
  }
}

function ruRenderProgress() {
  const el = document.getElementById('ru-progress');
  if (!el) return;
  const byPhase = RU.stats?.by_phase || {};
  const prog = RU.stats?.progress || {};
  el.innerHTML = RU_CURRICULUM.map(ph => {
    const bp = byPhase[ph.n] || { total: 0, learned: 0, due: 0 };
    const status = prog[ph.n] || 'not_started';
    let pct, sub;
    if (ph.n === 0) {
      // Alphabet is voice-practiced, not SM-2 drilled → show pronunciation-ladder progress
      const said = ruPronPassedCount();
      const total = ruPronTotalItems();
      pct = total ? Math.round(said / total * 100) : 0;
      sub = total ? `${said}/${total} practised` : 'roadmap';
    } else {
      pct = bp.total ? Math.round((bp.learned || 0) / bp.total * 100) : 0;
      sub = bp.total ? `${bp.learned || 0}/${bp.total}${bp.due ? ` · ${bp.due} due` : ''}` : 'roadmap';
    }
    const flag = status === 'done' ? '✓' : status === 'in_progress' ? '…' : '';
    return `<button class="ru-phase-chip ${status} ${RU.tab === String(ph.n) ? 'sel' : ''}" onclick="ruShowTab('${ph.n}')" title="${wrEsc(ph.title)}">
      <span class="ru-phase-chip-n">${ph.icon}</span>
      <span class="ru-phase-chip-body">
        <span class="ru-phase-chip-title">${wrEsc(ph.short)} <span class="ru-phase-flag">${flag}</span></span>
        <span class="ru-phase-chip-bar"><span style="width:${pct}%"></span></span>
        <span class="ru-phase-chip-sub">${sub}</span>
      </span>
    </button>`;
  }).join('');
}

function ruShowTab(tab) {
  RU.tab = tab;
  document.querySelectorAll('#page-russian .ru-tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('ru-tab-btn-' + tab)?.classList.add('active');
  const phase = document.getElementById('ru-panel-phase');
  const drill = document.getElementById('ru-panel-drill');
  const words = document.getElementById('ru-panel-words');
  [phase, drill, words].forEach(p => p?.classList.add('hidden'));
  if (tab === 'drill') { drill?.classList.remove('hidden'); ruStartDrill(); }
  else if (tab === 'words') { words?.classList.remove('hidden'); ruRenderWordFilters(); ruRenderWords(); }
  else { phase?.classList.remove('hidden'); ruRenderPhase(parseInt(tab, 10)); }
  ruRenderProgress();   // keep the selected-phase highlight in sync
}

function ruRenderPhase(n) {
  const ph = RU_CURRICULUM[n];
  const el = document.getElementById('ru-panel-phase');
  if (!ph || !el) return;
  const status = RU.stats?.progress?.[n] || 'not_started';
  const words = RU.byPhase[n] || [];
  const canDrill = n <= 3 && words.length;
  const nextStatus = status === 'in_progress' ? 'done' : 'in_progress';
  const markLabel = status === 'in_progress' ? 'Mark complete ✓' : 'Start this phase';

  let body = `
    <div class="ru-phase-head">
      <div>
        <div class="ru-phase-kicker">Phase ${ph.icon} · ${wrEsc(ph.time)}</div>
        <h2 class="ru-phase-title">${wrEsc(ph.title)}</h2>
      </div>
      <div class="ru-phase-actions">
        ${status !== 'done'
          ? `<button class="btn-secondary text-sm" onclick="ruMarkPhase(${n}, '${nextStatus}')">${markLabel}</button>`
          : `<span class="ru-done-pill">✓ Completed</span>`}
        ${canDrill ? `<button class="btn-primary text-sm" onclick="ruDrillPhase(${n})">Drill this phase →</button>` : ''}
      </div>
    </div>

    <div class="ru-phase-grid">
      <div class="ru-card ru-objective"><h3>Objective</h3><p>${wrEsc(ph.objective)}</p></div>
      <div class="ru-card ru-success"><h3>You’re done when…</h3><p>${wrEsc(ph.success)}</p></div>
    </div>

    <div class="ru-card"><h3>What you’ll actually learn</h3><ul class="ru-learn">${ph.learn.map(li => `<li>${li}</li>`).join('')}</ul></div>

    <div class="ru-resource">
      <div class="ru-resource-icon">🔗</div>
      <div class="ru-resource-body">
        <div class="ru-resource-label">Free resources for this section</div>
        ${(ph.resources || []).map(r => `
          <div class="ru-resource-item">
            <a href="${r.url}" target="_blank" rel="noopener" class="ru-resource-link">${wrEsc(r.name)} ↗</a>
            ${r.note ? `<span class="ru-resource-note">${wrEsc(r.note)}</span>` : ''}
          </div>`).join('')}
      </div>
    </div>

    <div class="ru-srs-callout">🧠 <b>Spaced repetition is built in.</b> The spec uses Anki — here the <button class="ru-inline-link" onclick="ruShowTab('drill')">Drill tab</button> does the same job with MedVault’s own SM-2 engine, seeded from these cards. No separate app needed.</div>
  `;

  if (n === 0) body += ruRenderAlphabet(words);
  else if (n === 4) body += ruRenderMaintain(ph);
  else body += ruRenderPhaseVocab(words);

  el.innerHTML = body;
  if (n === 0) ruPronounceInit(words);
}

function ruRenderAlphabet(letters) {
  const groups = [
    ['look-alike', 'Look-alikes', 'Same shape and sound as English — easy wins, do these first.'],
    ['false-friend', 'False friends', 'Look Latin but sound different — the classic beginner traps.'],
    ['new', 'Brand-new letters', 'New shapes; learn the sound each makes.'],
    ['sign', 'Signs & Ы', 'The silent hard/soft signs and the hard-“i” vowel with no English equivalent.'],
  ];
  let html = `<div class="ru-card"><h3>Cyrillic — tap a letter to hear it</h3>`;
  groups.forEach(([key, name, desc]) => {
    const items = letters.filter(l => l.note === key);
    if (!items.length) return;
    html += `<div class="ru-alpha-group"><div class="ru-alpha-group-head"><b>${name}</b> — ${desc}</div><div class="ru-alpha-grid">`;
    items.forEach(l => {
      html += `<button class="ru-letter" data-speak="${wrEsc(l.example || l.cyrillic)}" data-pron-cyr="${wrEsc(l.cyrillic)}" title="${wrEsc(l.english)} — tap to hear &amp; practise below">
        <span class="ru-letter-cyr">${wrEsc(l.cyrillic)}</span>
        <span class="ru-letter-sound">${wrEsc(l.translit)}</span>
        <span class="ru-letter-eg">${wrEsc(l.example || '')}</span>
      </button>`;
    });
    html += `</div></div>`;
  });
  html += `</div>`;   // close the grid ru-card
  html += `
    <div class="ru-card ru-pron" id="ru-pron">
      <div class="ru-pron-head">
        <div>
          <h3 style="margin:0">🎙 Pronunciation practice — A1 ladder</h3>
          <p class="ru-pron-sub">Six stages, sounds → phrases. Listen &amp; repeat the sounds and syllables (self-mark ✓/↻); whole words and phrases are checked by the mic. Tap any letter above to jump to its sound.</p>
        </div>
        <div class="ru-pron-progress" id="ru-pron-progress"></div>
      </div>
      <div id="ru-pron-body"></div>
    </div>`;
  return html;
}

function ruRenderPhaseVocab(words) {
  if (!words.length) return `<div class="ru-card"><p class="text-slate-400 text-sm">No cards in this phase yet — add some in the Words tab.</p></div>`;
  const cats = {};
  words.forEach(w => { (cats[w.category] = cats[w.category] || []).push(w); });
  let html = `<div class="ru-card"><h3>Phrases &amp; vocabulary — tap 🔊 to hear</h3>`;
  Object.entries(cats).forEach(([cat, items]) => {
    html += `<div class="ru-vocab-cat"><div class="ru-vocab-cat-name">${wrEsc(RU_CATS[cat] || cat)}</div><div class="ru-vocab-list">`;
    items.forEach(w => { html += ruVocabRow(w, false); });
    html += `</div></div>`;
  });
  return html + `</div>`;
}

function ruVocabRow(w, delible) {
  const speak = (w.category === 'letters' && w.example) ? w.example : w.cyrillic;
  return `<div class="ru-vocab-row">
    <button class="ru-speak-sm" data-speak="${wrEsc(speak)}" aria-label="Hear pronunciation">🔊</button>
    <div class="ru-vocab-main"><span class="ru-vocab-cyr">${wrEsc(w.cyrillic)}</span>${w.translit ? `<span class="ru-vocab-tr">${wrEsc(w.translit)}</span>` : ''}</div>
    <div class="ru-vocab-en">${wrEsc(w.english)}${w.note ? `<span class="ru-vocab-note">${wrEsc(w.note)}</span>` : ''}</div>
    ${delible && w.source !== 'seed' ? `<button class="ru-del" onclick="ruDeleteWord(${w.id})" title="Remove" aria-label="Remove">✕</button>` : ''}
  </div>`;
}

function ruRenderMaintain(ph) {
  return `<div class="ru-card"><h3>Keep it alive</h3>
    <p class="text-sm text-slate-500 mb-3">Maintenance beats intensity. Treat these as recurring habits:</p>
    <ul class="ru-checklist">${(ph.maintain || []).map(m => `<li>${wrEsc(m)}</li>`).join('')}</ul></div>`;
}

/* ── Drill (SM-2 review session) ─────────────────────────────── */
async function ruStartDrill() {
  const scope = parseInt(document.getElementById('ru-drill-scope')?.value ?? '-1', 10);
  RU.drill.scope = scope;
  const live = document.getElementById('ru-drill-live');
  const done = document.getElementById('ru-drill-done');
  try {
    const res = await api('GET', `/api/russian/drills?phase=${scope}`, null, { quiet: true });
    RU.drill.cards = Array.isArray(res.cards) ? res.cards : [];
  } catch (e) { RU.drill.cards = []; }
  RU.drill.idx = 0; RU.drill.correct = 0; RU.drill.flipped = false;
  if (!RU.drill.cards.length) {
    live?.classList.add('hidden'); done?.classList.remove('hidden');
    document.getElementById('ru-drill-score').textContent = 'No cards due right now — all caught up! 🎉';
    document.getElementById('ru-drill-progress').textContent = '';
    return;
  }
  live?.classList.remove('hidden'); done?.classList.add('hidden');
  ruShowDrillCard();
}

function ruShowDrillCard() {
  const d = RU.drill;
  if (d.idx >= d.cards.length) { ruDrillDone(); return; }
  const c = d.cards[d.idx];
  d.flipped = false;
  document.getElementById('ru-flip')?.classList.remove('flipped');
  document.getElementById('ru-grade')?.classList.add('hidden');
  document.getElementById('ru-drill-cyr').textContent = c.cyrillic;
  document.getElementById('ru-drill-en').textContent = c.english;
  document.getElementById('ru-drill-translit').textContent = c.translit || '';
  document.getElementById('ru-drill-note').textContent = [c.example, c.note].filter(Boolean).join(' · ');
  document.getElementById('ru-drill-progress').textContent = `Card ${d.idx + 1} of ${d.cards.length}`;
}

function ruFlip() {
  const d = RU.drill;
  if (!d.cards.length || d.idx >= d.cards.length) return;
  d.flipped = !d.flipped;
  document.getElementById('ru-flip')?.classList.toggle('flipped', d.flipped);
  document.getElementById('ru-grade')?.classList.toggle('hidden', !d.flipped);
  if (d.flipped) ruSpeakCurrent();   // auto-hear on reveal
}

async function ruGrade(correct) {
  const d = RU.drill;
  const c = d.cards[d.idx];
  if (!c) return;
  if (correct) d.correct++;
  try { await api('POST', `/api/russian/vocab/${c.id}/result`, { correct }, { quiet: true }); } catch (e) {}
  d.idx++;
  if (d.idx >= d.cards.length) ruDrillDone();
  else ruShowDrillCard();
}

function ruDrillDone() {
  const d = RU.drill;
  document.getElementById('ru-drill-live')?.classList.add('hidden');
  document.getElementById('ru-drill-done')?.classList.remove('hidden');
  const pct = d.cards.length ? Math.round(d.correct / d.cards.length * 100) : 0;
  document.getElementById('ru-drill-score').textContent = `${d.correct} / ${d.cards.length} correct (${pct}%)`;
  document.getElementById('ru-drill-progress').textContent = '';
  ruLoadStats();   // refresh due counts + progress rail
}

function ruSpeakCurrent() {
  const c = RU.drill.cards[RU.drill.idx];
  if (!c) return;
  ruSpeakText((c.category === 'letters' && c.example) ? c.example : c.cyrillic);
}

function ruDrillPhase(n) {
  const sel = document.getElementById('ru-drill-scope');
  if (sel) sel.value = String(n);
  ruShowTab('drill');
}

/* ── Words manager (browse / search / add / remove) ─────────── */
function ruRenderWordFilters() {
  const el = document.getElementById('ru-word-filters');
  if (!el) return;
  const present = Object.keys(RU_CATS).filter(c => RU.words.some(w => w.category === c));
  const cats = ['all', ...present];
  el.innerHTML = cats.map(c =>
    `<button class="ru-chip ${RU.activeCat === c ? 'on' : ''}" onclick="ruSetCat('${c}')">${c === 'all' ? 'All' : wrEsc(RU_CATS[c] || c)}</button>`
  ).join('');
}

function ruSetCat(c) { RU.activeCat = c; ruRenderWordFilters(); ruRenderWords(); }

function ruRenderWords() {
  const el = document.getElementById('ru-words');
  if (!el) return;
  const q = (document.getElementById('ru-search')?.value || '').trim().toLowerCase();
  let list = RU.words.slice();
  if (RU.activeCat !== 'all') list = list.filter(w => w.category === RU.activeCat);
  if (q) list = list.filter(w => (w.cyrillic + ' ' + (w.translit || '') + ' ' + w.english + ' ' + (w.note || '')).toLowerCase().includes(q));
  if (!list.length) { el.innerHTML = `<p class="text-slate-400 text-sm py-6 text-center">No cards match.</p>`; return; }
  const byPhase = {};
  list.forEach(w => { (byPhase[w.phase] = byPhase[w.phase] || []).push(w); });
  el.innerHTML = Object.keys(byPhase).sort().map(p => {
    const ph = RU_CURRICULUM[parseInt(p, 10)];
    const head = ph ? `${ph.icon} ${wrEsc(ph.short)}` : `Phase ${p}`;
    return `<div class="ru-words-phase"><div class="ru-words-phase-head">${head} <span class="ru-words-phase-n">${byPhase[p].length}</span></div>${byPhase[p].map(w => ruVocabRow(w, true)).join('')}</div>`;
  }).join('');
}

async function ruAddWord() {
  const cyr = document.getElementById('ru-add-cyr').value.trim();
  const en = document.getElementById('ru-add-en').value.trim();
  if (!cyr || !en) { toast('Cyrillic and English are both required', 'error'); return; }
  const word = {
    cyrillic: cyr, english: en,
    translit: document.getElementById('ru-add-translit').value.trim(),
    phase: parseInt(document.getElementById('ru-add-phase').value, 10),
    category: document.getElementById('ru-add-cat').value,
    note: document.getElementById('ru-add-note').value.trim(),
  };
  try {
    const res = await api('POST', '/api/russian/vocab', { words: [word] });
    if (res.added) {
      toast('Card added', 'success');
      ['ru-add-cyr', 'ru-add-translit', 'ru-add-en', 'ru-add-note'].forEach(id => { document.getElementById(id).value = ''; });
      await ruLoadWords(); await ruLoadStats();
      ruRenderWordFilters(); ruRenderWords();
    } else { toast('That card already exists', 'info'); }
  } catch (e) { /* api() already toasted */ }
}

async function ruDeleteWord(id) {
  try {
    await api('DELETE', '/api/russian/vocab/' + id);
    RU.words = RU.words.filter(w => w.id !== id);
    ruIndexWords();
    ruRenderWords();
    ruLoadStats();
    toast('Card removed', 'success');
  } catch (e) { /* api() already toasted */ }
}

async function ruMarkPhase(n, status) {
  try {
    await api('POST', '/api/russian/progress', { phase: n, status });
    await ruLoadStats();
    ruRenderPhase(n);
    toast(status === 'done' ? 'Phase marked complete 🎉' : 'Phase started — keep going', 'success');
  } catch (e) { /* api() already toasted */ }
}

/* ── Browser text-to-speech (zero-API pronunciation) ────────── */
function ruPickVoice() {
  if (!window.speechSynthesis) return;
  const voices = speechSynthesis.getVoices();
  RU.voice = voices.find(v => /^ru/i.test(v.lang)) || voices.find(v => /russian/i.test(v.name)) || null;
  const el = document.getElementById('ru-voice-status');
  if (el) el.textContent = RU.voice ? `🔊 ${RU.voice.name}` : '🔇 no Russian voice installed';
}

function ruSpeakText(text, btn) {
  if (!text) return;
  if (!window.speechSynthesis) { toast('Speech isn’t supported in this browser', 'error'); return; }
  speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  if (RU.voice) u.voice = RU.voice;
  u.lang = 'ru-RU';   // hint the engine even when no named ru voice is present
  u.rate = 0.85;
  if (btn) { btn.classList.add('speaking'); u.onend = u.onerror = () => btn.classList.remove('speaking'); }
  speechSynthesis.speak(u);
}

/* ══════════════════════════════════════════════════════════════
   RUSSIAN — alphabet pronunciation practice (browser speech
   recognition, zero-API). You say the letter's example word; the
   ru-RU recognizer transcribes it and we check the match.
   ══════════════════════════════════════════════════════════════ */
function ruSpeechSupported() {
  return !!(window.SpeechRecognition || window.webkitSpeechRecognition);
}

function ruNormalize(s) {
  return (s || '').toLowerCase().replace(/ё/g, 'е')
    .replace(/[^a-zа-я0-9 ]/gi, '').replace(/\s+/g, ' ').trim();
}

// Classic Levenshtein edit distance (small words → cheap).
function ruLev(a, b) {
  const m = a.length, n = b.length;
  if (!m) return n; if (!n) return m;
  let prev = Array.from({ length: n + 1 }, (_, i) => i);
  for (let i = 1; i <= m; i++) {
    const cur = [i];
    for (let j = 1; j <= n; j++) {
      cur[j] = Math.min(prev[j] + 1, cur[j - 1] + 1,
        prev[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    prev = cur;
  }
  return prev[n];
}

// True if any recognizer alternative matches the target (exact, substring, or
// within a small edit distance — tolerant of recognizer noise).
function ruMatch(alts, expected) {
  const exp = ruNormalize(expected);
  if (!exp) return false;
  const tol = exp.length <= 4 ? 1 : 2;
  return (alts || []).some(a => {
    const n = ruNormalize(a);
    if (!n) return false;
    if (n === exp) return true;
    if (n.includes(exp) || exp.includes(n)) return true;
    return ruLev(n, exp) <= tol;
  });
}

// Listen once via the Web Speech API. Resolves {heard, alts, ok} or {error}.
function ruListen(expected) {
  return new Promise((resolve) => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { resolve({ error: 'unsupported' }); return; }
    try { if (window.speechSynthesis) speechSynthesis.cancel(); } catch (e) {}
    const rec = new SR();
    rec.lang = 'ru-RU'; rec.interimResults = false; rec.maxAlternatives = 5; rec.continuous = false;
    let done = false;
    const finish = (r) => { if (done) return; done = true; try { rec.stop(); } catch (e) {} resolve(r); };
    const timer = setTimeout(() => finish({ error: 'timeout' }), 7000);
    rec.onresult = (e) => {
      clearTimeout(timer);
      const alts = [...e.results[0]].map(a => (a.transcript || '').trim()).filter(Boolean);
      finish({ heard: alts[0] || '', alts, ok: ruMatch(alts, expected) });
    };
    rec.onerror = (e) => { clearTimeout(timer); finish({ error: e.error || 'error' }); };
    rec.onend = () => { clearTimeout(timer); finish({ error: 'no-speech' }); };
    try { rec.start(); } catch (e) { clearTimeout(timer); finish({ error: 'start-failed' }); }
  });
}

function ruPronErrMsg(err) {
  switch (err) {
    case 'not-allowed':
    case 'service-not-allowed': return '🎙 Microphone blocked — allow mic access for this site, then try again.';
    case 'no-speech':          return 'Didn’t catch anything — tap the mic and speak clearly.';
    case 'network':            return 'Speech recognition needs an internet connection — check your network.';
    case 'timeout':            return 'Timed out waiting for speech — tap the mic and try again.';
    case 'unsupported':        return 'Pronunciation practice needs Chrome or Edge.';
    default:                   return 'Mic hiccup — tap the mic and try again.';
  }
}

/* ── Progress persistence (client-side, per browser) ────────── */
function ruPronKey(c) { return c && c.cyrillic ? c.cyrillic : ''; }
function ruPronLoadPassed() {
  try { RU.pronPassed = JSON.parse(localStorage.getItem('ru_pron_passed') || '{}') || {}; }
  catch (e) { RU.pronPassed = {}; }
}
function ruPronSavePassed() {
  try { localStorage.setItem('ru_pron_passed', JSON.stringify(RU.pronPassed)); } catch (e) {}
}
/* ── A1 pronunciation ladder — staged runner ─────────────────
   6 stages: sounds → syllables → stress → tricky pairs → words → phrases.
   'repeat' stages are listen-and-repeat + self-mark; 'say' stages are mic-graded. */
const RU_PHONICS = [
  { key: 'sounds', mode: 'repeat', title: 'Sounds',
    blurb: 'Hear each letter’s sound (in a real word) and repeat it. Tap ✓ Got it when it feels right.',
    items: null },   // built from the 33 letters at render time
  { key: 'syllables', mode: 'repeat', title: 'Syllables',
    blurb: 'Consonant + vowel blocks. Hard vowels (а о у ы э) keep the consonant hard; soft vowels (я ё ю и е) soften it. Say both halves.',
    items: [
      { show: 'ба · бя', hint: 'ba · bya (soft)', say: 'ба бя' },
      { show: 'ва · вя', hint: 'va · vya', say: 'ва вя' },
      { show: 'да · дя', hint: 'da · dya', say: 'да дя' },
      { show: 'ла · ля', hint: 'la · lya', say: 'ла ля' },
      { show: 'ма · мя', hint: 'ma · mya', say: 'ма мя' },
      { show: 'на · ня', hint: 'na · nya', say: 'на ня' },
      { show: 'па · пя', hint: 'pa · pya', say: 'па пя' },
      { show: 'ра · ря', hint: 'ra · rya', say: 'ра ря' },
      { show: 'са · ся', hint: 'sa · sya', say: 'са ся' },
      { show: 'та · тя', hint: 'ta · tya', say: 'та тя' },
      { show: 'бо · бё', hint: 'bo · byo', say: 'бо бё' },
      { show: 'ну · ню', hint: 'nu · nyu', say: 'ну ню' },
      { show: 'ты · ти', hint: 'ty · ti', say: 'ты ти' },
      { show: 'сы · си', hint: 'sy · si', say: 'сы си' },
      { show: 'дэ · де', hint: 'de · dye', say: 'дэ де' },
      { show: 'вэ · ве', hint: 've · vye', say: 'вэ ве' },
    ] },
  { key: 'stress', mode: 'say', title: 'Stress & reduction',
    blurb: 'Say the whole word; the mic checks you. Notice the stressed syllable and how unstressed о becomes “a”.',
    items: [
      { show: 'молоко',       say: 'молоко',       hint: 'ma-la-KÓ · milk (о→a)' },
      { show: 'хорошо',       say: 'хорошо',       hint: 'kha-ra-SHÓ · good / well' },
      { show: 'спасибо',      say: 'спасибо',      hint: 'spa-SÍ-ba · thank you' },
      { show: 'собака',       say: 'собака',       hint: 'sa-BÁ-ka · dog' },
      { show: 'Москва',       say: 'Москва',       hint: 'mask-VÁ · Moscow' },
      { show: 'вода',         say: 'вода',         hint: 'va-DÁ · water' },
      { show: 'работа',       say: 'работа',       hint: 'ra-BÓ-ta · work' },
      { show: 'город',        say: 'город',        hint: 'GÓ-rat · city (final д→t)' },
      { show: 'пожалуйста',   say: 'пожалуйста',   hint: 'pa-ZHÁL-sta · please' },
      { show: 'здравствуйте', say: 'здравствуйте', hint: 'ZDRÁST-vuy-tye · hello' },
    ] },
  { key: 'pairs', mode: 'repeat', title: 'Tricky pairs',
    blurb: 'Contrast each pair aloud until you can hear the difference, then self-mark.',
    items: [
      { show: 'ш · щ', hint: 'hard sh · soft shch', say: 'ша ща' },
      { show: 'ы · и', hint: 'hard y · soft i',     say: 'ты ти' },
      { show: 'б · в', hint: 'b · v',               say: 'ба ва' },
      { show: 'т · д', hint: 'voiceless t · voiced d', say: 'та да' },
      { show: 'с · з', hint: 's · z',               say: 'са за' },
      { show: 'х · к', hint: 'kh · k',              say: 'ха ка' },
      { show: 'л · р', hint: 'l · rolled r',        say: 'ла ра' },
      { show: 'п · б', hint: 'p · b',               say: 'па ба' },
      { show: 'г · к', hint: 'g · k',               say: 'га ка' },
      { show: 'э · е', hint: 'e · ye',              say: 'э е' },
      { show: 'о · а', hint: 'stressed o · reduced a', say: 'о а' },
    ] },
  { key: 'words', mode: 'say', title: 'A1 words',
    blurb: 'Say each word; the mic checks you.',
    items: [
      { show: 'привет',     say: 'привет',     hint: 'hi' },
      { show: 'спасибо',    say: 'спасибо',    hint: 'thank you' },
      { show: 'пожалуйста', say: 'пожалуйста', hint: 'please' },
      { show: 'извините',   say: 'извините',   hint: 'excuse me' },
      { show: 'вода',       say: 'вода',       hint: 'water' },
      { show: 'кофе',       say: 'кофе',       hint: 'coffee' },
      { show: 'хлеб',       say: 'хлеб',       hint: 'bread' },
      { show: 'дом',        say: 'дом',        hint: 'house' },
      { show: 'друг',       say: 'друг',       hint: 'friend' },
      { show: 'город',      say: 'город',      hint: 'city' },
      { show: 'книга',      say: 'книга',      hint: 'book' },
      { show: 'работа',     say: 'работа',     hint: 'work' },
      { show: 'деньги',     say: 'деньги',     hint: 'money' },
      { show: 'сегодня',    say: 'сегодня',    hint: 'today' },
      { show: 'хорошо',     say: 'хорошо',     hint: 'good / well' },
    ] },
  { key: 'phrases', mode: 'say', title: 'A1 phrases',
    blurb: 'Say each phrase aloud; the mic checks you.',
    items: [
      { show: 'Привет!',          say: 'привет',          hint: 'Hi!' },
      { show: 'Здравствуйте',     say: 'здравствуйте',    hint: 'Hello (formal)' },
      { show: 'Как дела?',        say: 'как дела',        hint: 'How are you?' },
      { show: 'Меня зовут…',      say: 'меня зовут',      hint: 'My name is…' },
      { show: 'Очень приятно',    say: 'очень приятно',   hint: 'Nice to meet you' },
      { show: 'Большое спасибо',  say: 'большое спасибо', hint: 'Thank you very much' },
      { show: 'До свидания',      say: 'до свидания',     hint: 'Goodbye' },
      { show: 'Я не понимаю',     say: 'я не понимаю',    hint: 'I don’t understand' },
      { show: 'Сколько стоит?',   say: 'сколько стоит',   hint: 'How much is it?' },
      { show: 'Где туалет?',      say: 'где туалет',      hint: 'Where is the toilet?' },
    ] },
];

// Materialise stages (the 'sounds' stage is built from the loaded 33 letters).
function ruPronStages() {
  const letters = RU.byPhase[0] || [];
  return RU_PHONICS.map(st => st.key === 'sounds'
    ? Object.assign({}, st, { items: letters.map(l => ({
        show: l.cyrillic, hint: `${l.translit} · ${l.english}`, say: l.example || l.cyrillic })) })
    : st);
}

function ruPronItemKey(stageKey, item) { return stageKey + ':' + item.show; }
function ruPronPassedCount() {
  let n = 0;
  ruPronStages().forEach(s => s.items.forEach(it => { if (RU.pronPassed[ruPronItemKey(s.key, it)]) n++; }));
  return n;
}
function ruPronTotalItems() { return ruPronStages().reduce((n, s) => n + s.items.length, 0); }

/* ── Runner ─────────────────────────────────────────────────── */
function ruPronounceInit() {
  const stages = ruPronStages();
  if (RU.pron.stageIdx >= stages.length) RU.pron.stageIdx = 0;
  const items = stages[RU.pron.stageIdx].items;
  if (RU.pron.itemIdx >= items.length) RU.pron.itemIdx = 0;
  RU.pron.last = null; RU.pron.listening = false;
  ruPronounceRender();
}

function ruPronounceRender() {
  const prog = document.getElementById('ru-pron-progress');
  const body = document.getElementById('ru-pron-body');
  const stages = ruPronStages();
  if (prog) {
    const said = ruPronPassedCount(), total = ruPronTotalItems();
    const pct = total ? Math.round(said / total * 100) : 0;
    prog.innerHTML = `<span class="ru-pron-count">${said} / ${total} practised</span>` +
      `<span class="ru-pron-bar"><span style="width:${pct}%"></span></span>`;
  }
  if (!body) return;
  const st = stages[RU.pron.stageIdx] || stages[0];
  const pills = stages.map((s, i) => {
    const done = s.items.filter(it => RU.pronPassed[ruPronItemKey(s.key, it)]).length;
    const full = s.items.length && done === s.items.length;
    return `<button class="ru-stage ${i === RU.pron.stageIdx ? 'on' : ''} ${full ? 'full' : ''}" onclick="ruPronounceStage(${i})">
      <span class="ru-stage-t">${i + 1}. ${wrEsc(s.title)}</span>
      <span class="ru-stage-n">${done}/${s.items.length}</span></button>`;
  }).join('');
  body.innerHTML = `<div class="ru-stagebar">${pills}</div>
    <div class="ru-stage-blurb">${wrEsc(st.blurb)}</div>
    ${ruPronItemCard(st)}`;
}

function ruPronItemCard(st) {
  const it = st.items[RU.pron.itemIdx];
  if (!it) return `<p class="text-slate-400 text-sm text-center py-6">No items in this stage yet.</p>`;
  const audio = it.say || it.show;
  const useMic = st.mode === 'say' && ruSpeechSupported();
  const passed = !!RU.pronPassed[ruPronItemKey(st.key, it)];
  const last = RU.pron.last;
  let fb;
  if (RU.pron.listening) fb = `<div class="ru-pron-fb listening">● Listening… say “${wrEsc(audio)}” now</div>`;
  else if (last && last.error) fb = `<div class="ru-pron-fb err">${wrEsc(ruPronErrMsg(last.error))}</div>`;
  else if (last && last.heard !== undefined) fb = `<div class="ru-pron-fb ${last.ok ? 'ok' : (useMic ? 'miss' : 'idle')}">${useMic ? (last.ok ? '✓ Heard' : '✗ Heard') : '👂 Heard'} “${wrEsc(last.heard || '…')}”${useMic ? (last.ok ? ' — matches!' : ' — not quite') : ' — compare, then mark yourself'}</div>`;
  else if (passed) fb = `<div class="ru-pron-fb ok">✓ Practised — go again anytime.</div>`;
  else fb = `<div class="ru-pron-fb idle">${useMic ? 'Tap 🎙 and say it — the recognizer checks you.' : 'Tap 🔊 to hear it, repeat aloud, then mark ✓ / ↻.'}</div>`;

  const controls = useMic
    ? `<button class="ru-mic ${RU.pron.listening ? 'listening' : ''}" onclick="ruPronounceMic()" ${RU.pron.listening ? 'disabled' : ''} aria-label="Tap and speak">🎙</button>`
    : `<div class="ru-mark-row">
         <button class="ru-mark ru-mark-again" onclick="ruPronounceMark(false)">↻ Again</button>
         <button class="ru-mark ru-mark-got" onclick="ruPronounceMark(true)">✓ Got it</button>
         <button class="ru-mic-hint ${RU.pron.listening ? 'listening' : ''}" onclick="ruPronounceMic()" ${RU.pron.listening ? 'disabled' : ''} title="Optional: hear what the recognizer catches">🎙 check</button>
       </div>`;

  return `<div class="ru-pron-card">
      <div class="ru-pron-letter">${wrEsc(it.show)}${passed ? '<span class="ru-pron-tick">✓</span>' : ''}</div>
      ${it.hint ? `<div class="ru-pron-sound">${wrEsc(it.hint)}</div>` : ''}
      <div class="ru-pron-say"><button class="ru-speak-sm" data-speak="${wrEsc(audio)}" title="Hear it" aria-label="Hear it">🔊</button><span>hear &amp; repeat</span></div>
      ${controls}
      ${fb}
      <div class="ru-pron-nav">
        <button class="ru-pron-btn" onclick="ruPronounceNav(-1)" ${RU.pron.itemIdx <= 0 ? 'disabled' : ''}>← Prev</button>
        <span class="ru-pron-pos">${RU.pron.itemIdx + 1} / ${st.items.length}</span>
        <button class="ru-pron-btn" onclick="ruPronounceNav(1)" ${RU.pron.itemIdx >= st.items.length - 1 ? 'disabled' : ''}>Next →</button>
      </div>
    </div>`;
}

function ruPronounceStage(i) {
  RU.pron.stageIdx = i; RU.pron.itemIdx = 0; RU.pron.last = null;
  ruPronounceRender();
}

function ruPronounceNav(delta) {
  const items = ruPronStages()[RU.pron.stageIdx].items;
  RU.pron.itemIdx = Math.max(0, Math.min(items.length - 1, RU.pron.itemIdx + delta));
  RU.pron.last = null;
  ruPronounceRender();
}

// Self-mark (repeat stages): ✓ records a pass and advances; ↻ just re-practises.
function ruPronounceMark(ok) {
  const st = ruPronStages()[RU.pron.stageIdx];
  const it = st.items[RU.pron.itemIdx];
  if (!it) return;
  if (ok) {
    RU.pronPassed[ruPronItemKey(st.key, it)] = true;
    ruPronSavePassed();
    ruRenderProgress();
    if (RU.pron.itemIdx < st.items.length - 1) RU.pron.itemIdx++;
  }
  RU.pron.last = null;
  ruPronounceRender();
}

async function ruPronounceMic() {
  if (RU.pron.listening) return;
  const st = ruPronStages()[RU.pron.stageIdx];
  const it = st.items[RU.pron.itemIdx];
  if (!it || !ruSpeechSupported()) { ruPronounceRender(); return; }
  RU.pron.listening = true; RU.pron.last = null;
  ruPronounceRender();
  const res = await ruListen(it.say || it.show);
  RU.pron.listening = false;
  RU.pron.last = res;
  if (st.mode === 'say' && res && res.ok) {   // auto-pass only on mic-graded stages
    const key = ruPronItemKey(st.key, it);
    if (!RU.pronPassed[key]) { RU.pronPassed[key] = true; ruPronSavePassed(); ruRenderProgress(); }
    if (typeof toast === 'function') toast('Nice — the recognizer heard it ✓', 'success');
  }
  ruPronounceRender();
}

// Tapping a letter tile jumps to that letter in the Sounds stage.
function ruPronounceJump(cyr) {
  const stages = ruPronStages();
  const si = stages.findIndex(s => s.key === 'sounds');
  if (si < 0) return;
  const ii = stages[si].items.findIndex(it => it.show === cyr);
  if (ii < 0) return;
  RU.pron.stageIdx = si; RU.pron.itemIdx = ii; RU.pron.last = null;
  ruPronounceRender();
  document.getElementById('ru-pron')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ── Themes ────────────────────────────────────────────────────────────────
const THEMES = {
  ocean:    { name:'Ocean',    navy:'#071e3d', teal:'#0ea5e9', tealD:'#0284c7', navBg:'rgba(14,165,233,0.22)',  navTxt:'#38bdf8' },
  forest:   { name:'Forest',   navy:'#041a0c', teal:'#10b981', tealD:'#059669', navBg:'rgba(16,185,129,0.22)',  navTxt:'#34d399' },
  sunset:   { name:'Sunset',   navy:'#1a0800', teal:'#f97316', tealD:'#ea580c', navBg:'rgba(249,115,22,0.22)',  navTxt:'#fb923c' },
  charcoal: { name:'Charcoal', navy:'#080a0e', teal:'#8b5cf6', tealD:'#7c3aed', navBg:'rgba(139,92,246,0.22)', navTxt:'#a78bfa' },
  rose:     { name:'Rose',     navy:'#120009', teal:'#f43f5e', tealD:'#e11d48', navBg:'rgba(244,63,94,0.22)',   navTxt:'#fb7185' },
};

// ── State ─────────────────────────────────────────────────────────────────
const S = {
  page: 'dashboard',
  userId: null, username: null,
  materials: [],
  slides: [],    slideIdx: 0,
  flashcards: [], fcIdx: 0, fcFlipped: false, fcCorrect: 0,
  quiz: [],       qIdx: 0,  qCorrect: 0, qAnswered: false,
  quizResults: [], quizDifficulty: 'mixed',
  tutorMode: 'explain',
  sessionId: Math.random().toString(36).slice(2),
  examDates: [],
  charts: {},
};

// ── API helper ────────────────────────────────────────────────────────────
async function api(method, path, body) {
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
  const res = await fetch(path, opts);
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
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

function loading(show, text = 'Generating with AI…') {
  document.getElementById('loading-overlay').classList.toggle('hidden', !show);
  document.getElementById('loading-text').textContent = text;
}

function toast(msg, type = 'info') {
  const colours = { info: 'bg-blue-500', success: 'bg-green-500', error: 'bg-red-500' };
  const el = document.createElement('div');
  el.className = `fixed bottom-24 right-6 ${colours[type]} text-white px-5 py-3 rounded-xl shadow-lg z-50 text-sm font-medium transition-all`;
  el.textContent = msg;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3500);
}

// ── Navigation ────────────────────────────────────────────────────────────
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.add('hidden'));
  document.getElementById(`page-${id}`).classList.remove('hidden');
  document.querySelectorAll('.nav-link').forEach(l => {
    l.classList.toggle('active', l.dataset.page === id);
  });
  const titles = { dashboard:'Dashboard', materials:'Materials', discover:'Discover', slides:'Revision Slides',
    flashcards:'Flashcards', quiz:'Quiz', tutor:'AI Tutor', mindmaps:'Mind Maps', studyplan:'Study Plan', settings:'Settings' };
  document.getElementById('page-title').textContent = titles[id] || id;
  S.page = id;
  if (id === 'dashboard')  loadDashboard();
  if (id === 'materials')  loadMaterials();
  if (id === 'discover')   initDiscoverPage();
  if (id === 'slides')     initSlidesPage();
  if (id === 'flashcards') initFcPage();
  if (id === 'quiz')       initQuizPage();
  if (id === 'tutor')      initTutorPage();
  if (id === 'mindmaps')   initMmPage();
  if (id === 'studyplan')  initStudyPlanPage();
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
});

// ── Dashboard ─────────────────────────────────────────────────────────────
async function loadDashboard() {
  try {
    // Fire all three calls in parallel — was sequential before (3× slower)
    const [p, s, exams] = await Promise.all([
      api('GET', '/api/progress'),
      api('GET', '/api/srs/stats'),
      api('GET', '/api/exam-dates'),
    ]);

    document.getElementById('stat-materials').textContent  = p.counts.materials;
    document.getElementById('stat-flashcards').textContent = p.counts.flashcards;
    document.getElementById('stat-accuracy').textContent   = p.quiz.total ? p.quiz.accuracy + '%' : '—';
    document.getElementById('stat-questions').textContent  = p.quiz.total || 0;

    const topics = (p.combined_topics && p.combined_topics.length) ? p.combined_topics : p.quiz.by_topic;
    renderTopicsChart(topics);
    renderActivityChart(p.daily, p.daily_fc || []);
    renderWeakTopics(topics);
    renderSRSStats(s);
    renderExamCountdown(exams);
  } catch(e) {
    console.error(e);
  }
}

// Standalone fetch+render (used after flashcard sessions, from study-plan page, etc.)
async function loadSRSStats()      { try { renderSRSStats(await api('GET', '/api/srs/stats')); } catch(e) {} }
async function loadExamCountdown() { try { renderExamCountdown(await api('GET', '/api/exam-dates')); } catch(e) {} }

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
  // Navigate to flashcards with due-only mode pre-enabled
  const toggle = document.getElementById('fc-due-only');
  if (toggle) toggle.checked = true;
  showPage('flashcards');
  // loadFlashcards needs a material selected — pick the first if none chosen
  const sel = document.getElementById('fc-material-select');
  if (sel && !sel.value && S.materials.length) {
    sel.value = S.materials[0].id;
  }
  loadFlashcards();
}

function renderTopicsChart(topics) {
  const el = document.getElementById('chart-topics');
  const empty = document.getElementById('chart-topics-empty');
  if (!topics.length) { empty.classList.remove('hidden'); return; }
  empty.classList.add('hidden');

  if (S.charts.topics) S.charts.topics.destroy();
  const labels = topics.slice(0,8).map(t => t.topic);
  const data   = topics.slice(0,8).map(t => Math.round((t.accuracy||0)*100));
  const colors = data.map(v => v < 50 ? '#ef4444' : v < 75 ? '#f59e0b' : '#10b981');

  S.charts.topics = new Chart(el, {
    type: 'bar',
    data: { labels, datasets: [{ data, backgroundColor: colors, borderRadius: 6, borderSkipped: false }] },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11 } } },
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

  S.charts.activity = new Chart(el, {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Cards Reviewed', data: fcRevs,   borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,0.08)',  tension: 0.35, fill: true, pointRadius: 4 },
        { label: 'Quiz Attempted', data: quizAtt,  borderColor: '#94a3b8', backgroundColor: 'rgba(148,163,184,0.08)', tension: 0.35, fill: true, pointRadius: 4 },
        { label: 'Quiz Correct',   data: quizCorr, borderColor: '#0891b2', backgroundColor: 'rgba(8,145,178,0.08)',   tension: 0.35, fill: true, pointRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: { legend: { labels: { font: { size: 11 }, boxWidth: 12 } } },
      scales: {
        x: { grid: { display: false }, ticks: { font: { size: 11 } } },
        y: { beginAtZero: true, ticks: { precision: 0, font: { size: 11 } }, grid: { color: '#f1f5f9' } }
      }
    }
  });
}

function renderWeakTopics(topics) {
  const el = document.getElementById('weak-topics-list');
  if (!topics.length) { el.textContent = 'Complete quizzes to identify weak areas'; return; }
  el.innerHTML = topics.slice(0,5).map(t => {
    const pct = Math.round((t.accuracy||0)*100);
    const col = pct < 50 ? 'bg-red-100 text-red-700' : pct < 75 ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700';
    return `<div class="flex items-center justify-between">
      <span class="text-slate-600 truncate max-w-xs">${t.topic}</span>
      <span class="text-xs font-semibold px-2 py-0.5 rounded-full ${col}">${pct}%</span>
    </div>`;
  }).join('');
}

function renderExamCountdown(exams) {
  S.examDates = exams;
  const el = document.getElementById('exam-countdown-list');
  if (!exams || !exams.length) { el.textContent = 'No exams added yet — go to Study Plan to add one.'; return; }
  const today = new Date(); today.setHours(0,0,0,0);
  el.innerHTML = exams.slice(0,4).map(e => {
    const d = new Date(e.exam_date+'T12:00');
    const days = Math.round((d - today) / 86400000);
    const col = days < 7 ? 'text-red-600 font-bold' : days < 14 ? 'text-amber-600 font-semibold' : 'text-teal-600 font-medium';
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
    S.materials = await api('GET', '/api/materials');
    _matsLastFetched = Date.now();
    renderMaterials();
    populateMaterialSelects();
  } catch(e) { console.error(e); }
}

// Drag-and-drop state
let _dragSrc = null;

function renderMaterials() {
  const el = document.getElementById('materials-list');
  if (!S.materials.length) {
    el.innerHTML = '<p class="text-slate-400 text-sm">No materials uploaded yet.</p>';
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
        <span class="text-xs text-slate-300">${mats.length} file${mats.length !== 1 ? 's' : ''}</span>
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
      <div class="font-medium text-slate-700 text-sm leading-snug">
        <span class="mat-name cursor-pointer hover:text-teal-600" onclick="startInlineEdit(${m.id},'name',this)" title="Click to rename">${sEsc(m.original_name)}</span>
      </div>
      <div class="text-xs text-slate-400 mt-0.5">
        <span class="mat-subject cursor-pointer hover:text-teal-600" onclick="startInlineEdit(${m.id},'subject',this)" title="Click to change subject">${sEsc(m.subject)}</span>
        · ${Math.round((m.chars||0)/1000)}k chars · ${new Date(m.uploaded_at).toLocaleDateString()}
      </div>
      <div class="flex gap-2 mt-2 flex-wrap">
        <button class="gen-btn" onclick="quickGenSlides(${m.id})">Slides</button>
        <button class="gen-btn" onclick="quickGenFlashcards(${m.id})">Flashcards</button>
        <button class="gen-btn" onclick="quickGenQuiz(${m.id})">Quiz</button>
        <button class="gen-btn" onclick="quickGenMindmap(${m.id})">Mind Map</button>
        ${ownerTag}
      </div>
    </div>
    <button onclick="deleteMaterial(${m.id})" class="text-slate-300 hover:text-red-400 transition-colors flex-shrink-0 p-1 mt-0.5" title="${m.is_owner ? 'Delete' : 'Remove from library'}">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
    </button>
  </div>`;
}

function startInlineEdit(mid, field, spanEl) {
  const current = spanEl.textContent;
  const input = document.createElement('input');
  input.type = 'text';
  input.value = current;
  input.className = 'border border-teal-400 rounded px-1.5 py-0.5 text-sm outline-none w-full max-w-xs';
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
    span.className = (field === 'name' ? 'mat-name' : 'mat-subject') + ' cursor-pointer hover:text-teal-600';
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
    const isOptional = id === 'quiz-material-select' || id === 'tutor-material-select';
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
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('border-teal-400','bg-teal-50'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('border-teal-400','bg-teal-50'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('border-teal-400','bg-teal-50');
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
async function quickGenMindmap(id) {
  loading(true, 'Generating mind map…');
  try { await api('POST', `/api/generate/mindmap/${id}`); toast('Mind map ready!', 'success'); }
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
  try {
    S.slides = await api('GET', `/api/slides?material_id=${id}`);
    S.slideIdx = 0;
    if (S.slides.length) {
      document.getElementById('slide-viewer').classList.remove('hidden');
      document.getElementById('slides-empty').classList.add('hidden');
      renderSlide();
    } else {
      document.getElementById('slides-empty').textContent = 'No slides yet — click "Generate Slides"';
      document.getElementById('slides-empty').classList.remove('hidden');
      document.getElementById('slide-viewer').classList.add('hidden');
    }
  } catch(e) { console.error(e); }
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
    comparison: slideComparison, process: slideProcess, mnemonic: slideMnemonic, clinical: slideClinical };
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

// ── HTML diagram builders (replaces SVG — no character limits, reflowable) ──
const DIAG_COLORS = ['#1e3a5f','#0891b2','#7c3aed','#059669','#d97706','#0e7490','#1d4ed8','#dc2626'];

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
  if (!id) { loadSRSStats(); return; }
  try {
    const params = `material_id=${id}&adaptive=${adap}&due_only=${dueOnly}`;
    S.flashcards = await api('GET', `/api/flashcards?${params}`);
    S.fcIdx = 0; S.fcCorrect = 0; S.fcFlipped = false;
    S.fcDueOnly = dueOnly;
    const viewer = document.getElementById('fc-viewer');
    const empty  = document.getElementById('fc-empty');
    if (S.flashcards.length) {
      viewer.classList.remove('hidden'); empty.classList.add('hidden');
      document.getElementById('fc-done').classList.add('hidden');
      showFlashcard();
    } else {
      empty.textContent = dueOnly
        ? '🗓️ All caught up! No cards are due right now. Come back later or switch off "Due only" to review all cards.'
        : 'No flashcards yet — click "Generate Cards"';
      empty.classList.remove('hidden'); viewer.classList.add('hidden');
    }
    loadSRSStats();
  } catch(e) { console.error(e); }
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
  document.getElementById('fc-answer').textContent   = c.answer;
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
  try { await api('POST', `/api/flashcards/${card.id}/result`, { correct }); } catch(e) {}
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
    toast(res.existing ? `${res.count} saved questions loaded (no AI used)` : `${res.count} questions generated!`,
          res.existing ? 'info' : 'success');
    startQuiz();
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

async function startQuiz() {
  const id = document.getElementById('quiz-material-select').value;
  try {
    S.quiz = await api('GET', id ? `/api/quiz?material_id=${id}` : '/api/quiz');
    S.qIdx = 0; S.qCorrect = 0; S.qAnswered = false; S.quizResults = [];
    document.getElementById('quiz-done').classList.add('hidden');
    document.getElementById('quiz-review').classList.add('hidden');
    document.getElementById('quiz-explanation').classList.add('hidden');
    if (S.quiz.length) {
      document.getElementById('quiz-viewer').classList.remove('hidden');
      document.getElementById('quiz-empty').classList.add('hidden');
      showQuestion();
    } else {
      document.getElementById('quiz-empty').textContent = 'No questions yet — click "Generate Quiz"';
      document.getElementById('quiz-empty').classList.remove('hidden');
      document.getElementById('quiz-viewer').classList.add('hidden');
    }
  } catch(e) { console.error(e); }
}

function showQuestion() {
  if (S.qIdx >= S.quiz.length) { showQuizDone(); return; }
  const q = S.quiz[S.qIdx];
  S.qAnswered = false;
  document.getElementById('quiz-progress-text').textContent = `Question ${S.qIdx+1} of ${S.quiz.length}`;
  document.getElementById('quiz-topic-badge').textContent   = q.topic || '';
  document.getElementById('quiz-progress-bar').style.width  = `${(S.qIdx/S.quiz.length)*100}%`;
  document.getElementById('quiz-question').textContent = q.question;
  document.getElementById('quiz-explanation').classList.add('hidden');
  // Difficulty badge
  const diffEl = document.getElementById('quiz-diff-badge');
  const diffMap = { easy:'bg-green-100 text-green-700', medium:'bg-amber-100 text-amber-700', hard:'bg-red-100 text-red-700' };
  if (diffEl && q.difficulty) {
    diffEl.textContent = q.difficulty;
    diffEl.className = `text-xs font-semibold px-2 py-0.5 rounded-full ${diffMap[q.difficulty] || diffMap.medium}`;
    diffEl.classList.remove('hidden');
  } else if (diffEl) { diffEl.classList.add('hidden'); }

  const opts = document.getElementById('quiz-options');
  opts.innerHTML = (q.options || []).map((opt, i) => {
    const letter = ['A','B','C','D'][i];
    return `<button class="quiz-option" onclick="selectAnswer('${letter}', this)">${opt}</button>`;
  }).join('');

  const badge = document.getElementById('quiz-score-badge');
  badge.textContent = `${S.qCorrect} / ${S.qIdx} correct`;
  badge.classList.toggle('hidden', S.qIdx === 0);
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

    const expEl = document.getElementById('quiz-explanation');
    const label = document.getElementById('quiz-result-label');
    label.innerHTML = res.correct
      ? '<span class="text-green-600">✓ Correct!</span>'
      : `<span class="text-red-600">✗ Incorrect</span> — Correct answer: <strong>${res.correct_answer}</strong>`;
    label.className = 'font-semibold mb-2';
    document.getElementById('quiz-explanation-text').textContent = res.explanation || '';
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
  try { await api('DELETE', `/api/chat/${S.sessionId}`); } catch(e) {}
  S.sessionId = Math.random().toString(36).slice(2);
  document.getElementById('chat-messages').innerHTML = `
    <div class="flex justify-start">
      <div class="chat-bubble assistant">
        <p>Chat cleared! Ask me anything about your studies.</p>
      </div>
    </div>`;
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

// ── Mind Maps ─────────────────────────────────────────────────────────────
async function initMmPage() { await loadMaterials(); }

async function generateMindMap(force = false) {
  const id = document.getElementById('mm-material-select').value;
  if (!id) { toast('Please select a material first', 'error'); return; }
  loading(true, force ? 'Regenerating mind map with AI…' : 'Preparing mind map…');
  try {
    const data = await api('POST', `/api/generate/mindmap/${id}${force ? '?force=true' : ''}`);
    toast('Mind map ready!', 'success');
    showMindMap(data, S.materials.find(m => m.id == id)?.original_name || 'Mind Map');
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

document.getElementById('mm-material-select')?.addEventListener('change', async e => {
  if (!e.target.value) return;
  try {
    const maps = await api('GET', `/api/mindmaps?material_id=${e.target.value}`);
    if (maps.length) showMindMap(maps[0].data, maps[0].original_name);
  } catch(err) {}
});

function showMindMap(data, title) {
  document.getElementById('mm-container').classList.remove('hidden');
  document.getElementById('mm-empty').classList.add('hidden');
  document.getElementById('mm-title').textContent = title;
  renderMindMap(data, document.getElementById('mm-svg'));
}

function renderMindMap(node, svg) {
  // ── Colour palette — one colour per branch ─────────────────────────────────
  const PALETTE = [
    { b:'#3b82f6', t:'#fff', lb:'#dbeafe', ls:'#93c5fd', lt:'#1e3a8a' },
    { b:'#10b981', t:'#fff', lb:'#d1fae5', ls:'#6ee7b7', lt:'#064e3b' },
    { b:'#8b5cf6', t:'#fff', lb:'#ede9fe', ls:'#c4b5fd', lt:'#3b0764' },
    { b:'#f59e0b', t:'#fff', lb:'#fef3c7', ls:'#fcd34d', lt:'#451a03' },
    { b:'#ef4444', t:'#fff', lb:'#fee2e2', ls:'#fca5a5', lt:'#450a0a' },
    { b:'#06b6d4', t:'#fff', lb:'#cffafe', ls:'#67e8f9', lt:'#083344' },
  ];

  // ── Layout constants ────────────────────────────────────────────────────────
  const R1    = 170;   // root → branch radius
  const R2    = 155;   // branch → leaf radius
  const OUTER = R1 + R2 + 90; // canvas half-size (includes label overhang)

  const branches = node.children || [];
  const N = Math.max(branches.length, 1);
  const SECTOR = (2 * Math.PI) / N;

  // Set a square viewBox centred at 0,0 — SVG scales to container width
  const VB = OUTER;
  svg.setAttribute('viewBox', `-${VB} -${VB} ${VB*2} ${VB*2}`);
  svg.style.height = Math.min(svg.clientWidth || 800, 720) + 'px';

  // ── Position calculation ────────────────────────────────────────────────────
  const pos = {};  // id → {x,y}
  const col = {};  // id → palette entry
  pos[node.id] = { x: 0, y: 0 };

  branches.forEach((b, i) => {
    const bAngle = SECTOR * i - Math.PI / 2;
    pos[b.id] = { x: R1 * Math.cos(bAngle), y: R1 * Math.sin(bAngle) };
    col[b.id] = PALETTE[i % PALETTE.length];

    const leaves = b.children || [];
    const M = leaves.length;
    // Fan: 70 % of the branch sector, leaves spread around the branch angle
    const fanHalf = M > 1 ? SECTOR * 0.35 : 0;
    leaves.forEach((l, j) => {
      const lAngle = M > 1 ? bAngle + (j / (M - 1) - 0.5) * fanHalf * 2 : bAngle;
      pos[l.id] = {
        x: pos[b.id].x + R2 * Math.cos(lAngle),
        y: pos[b.id].y + R2 * Math.sin(lAngle),
      };
      col[l.id] = col[b.id];
    });
  });

  // ── Helpers ────────────────────────────────────────────────────────────────
  // Split a label into ≤2 lines at word boundaries
  function wrapLabel(text, maxCh) {
    text = String(text || '').trim();
    if (text.length <= maxCh) return [text];
    const words = text.split(/\s+/);
    const lines = [];
    let cur = '';
    for (const w of words) {
      const next = cur ? cur + ' ' + w : w;
      if (next.length > maxCh && cur) { lines.push(cur); cur = w; }
      else cur = next;
    }
    if (cur) lines.push(cur);
    return lines.slice(0, 2);
  }

  // Curved connector (quadratic bezier pulled 30 % toward origin)
  function edge(fx, fy, tx, ty, colour, width, opacity) {
    const mx = (fx + tx) / 2 * 0.7;
    const my = (fy + ty) / 2 * 0.7;
    return `<path d="M${fx},${fy} Q${mx},${my} ${tx},${ty}" fill="none" stroke="${colour}" stroke-width="${width}" opacity="${opacity}" stroke-linecap="round"/>`;
  }

  // Rounded rect + centred multi-line text
  function pill(x, y, lines, rw, rh, rx, fill, textFill, fontSize, fontWeight, stroke, strokeW) {
    const lineH = fontSize + 2;
    const totalH = lines.length * lineH - 2;
    let out = `<rect x="${x - rw}" y="${y - rh/2}" width="${rw*2}" height="${rh}" rx="${rx}" fill="${fill}"`;
    if (stroke) out += ` stroke="${stroke}" stroke-width="${strokeW}"`;
    out += '/>';
    lines.forEach((ln, li) => {
      const ly = y + (li - (lines.length - 1) / 2) * lineH + fontSize * 0.35;
      out += `<text x="${x}" y="${ly}" text-anchor="middle" fill="${textFill}" font-size="${fontSize}" font-weight="${fontWeight}" font-family="Inter,system-ui,sans-serif">${escHtml(ln)}</text>`;
    });
    return out;
  }

  // ── Build SVG ──────────────────────────────────────────────────────────────
  let edgesHTML = '', nodesHTML = '';

  // Edges (drawn first so they appear behind nodes)
  branches.forEach((b, i) => {
    const c = PALETTE[i % PALETTE.length];
    const bp = pos[b.id];
    edgesHTML += edge(0, 0, bp.x, bp.y, c.b, 2.5, 0.8);
    (b.children || []).forEach(l => {
      const lp = pos[l.id];
      edgesHTML += edge(bp.x, bp.y, lp.x, lp.y, c.b, 1.5, 0.5);
    });
  });

  // Root node
  const rootLines = wrapLabel(node.label, 18);
  const rootH = 28 + (rootLines.length - 1) * 14;
  nodesHTML += pill(0, 0, rootLines, 78, rootH, 14, '#1e293b', '#fff', 13, 700, null, 0);

  // Branch + leaf nodes
  branches.forEach((b, i) => {
    const c = PALETTE[i % PALETTE.length];
    const bp = pos[b.id];
    const bLines = wrapLabel(b.label, 16);
    const bRW = Math.max(52, bLines.reduce((m, l) => Math.max(m, l.length * 5.6 + 18), 0));
    const bH = 26 + (bLines.length - 1) * 14;
    nodesHTML += pill(bp.x, bp.y, bLines, bRW, bH, bH / 2, c.b, c.t, 11.5, 600, null, 0);

    (b.children || []).forEach(l => {
      const lp = pos[l.id];
      const lLines = wrapLabel(l.label, 18);
      const lRW = Math.max(44, lLines.reduce((m, ln) => Math.max(m, ln.length * 4.9 + 14), 0));
      const lH = 22 + (lLines.length - 1) * 13;
      nodesHTML += pill(lp.x, lp.y, lLines, lRW, lH, 9, c.lb, c.lt, 10.5, 500, c.ls, 1.5);
    });
  });

  svg.innerHTML = edgesHTML + nodesHTML;
}

// ── Study Plan ────────────────────────────────────────────────────────────
async function initStudyPlanPage() {
  await loadMaterials();
  loadExamDates();
}

async function loadExamDates() {
  try {
    S.examDates = await api('GET', '/api/exam-dates');
    renderExamList();
    populatePlanExamSelect();
  } catch(e) {}
}

function renderExamList() {
  const el = document.getElementById('exam-list');
  if (!S.examDates.length) { el.innerHTML = '<p class="text-slate-400 text-xs">No exams added yet</p>'; return; }
  const today = new Date(); today.setHours(0,0,0,0);
  el.innerHTML = S.examDates.map(e => {
    const days = Math.round((new Date(e.exam_date+'T12:00') - today) / 86400000);
    return `<div class="flex items-center justify-between text-xs">
      <div>
        <div class="font-medium text-slate-700">${e.subject}</div>
        <div class="text-slate-400">${e.exam_date} · ${days < 0 ? 'Past' : days+' days'}</div>
      </div>
      <button onclick="deleteExam(${e.id})" class="text-slate-300 hover:text-red-400 transition-colors">✕</button>
    </div>`;
  }).join('');
}

function populatePlanExamSelect() {
  const el = document.getElementById('plan-exam-select');
  el.innerHTML = '<option value="">Pick an exam…</option>' +
    S.examDates.map(e => `<option value="${e.exam_date}|${e.subject}">${e.subject} — ${e.exam_date}</option>`).join('');
}

async function addExamDate() {
  const subject = document.getElementById('exam-subject').value.trim();
  const date    = document.getElementById('exam-date-input').value;
  const notes   = document.getElementById('exam-notes').value.trim();
  if (!subject || !date) { toast('Please fill in subject and date', 'error'); return; }
  try {
    await api('POST', '/api/exam-dates', { subject, exam_date: date, notes });
    toast('Exam date added!', 'success');
    document.getElementById('exam-date-input').value = '';
    document.getElementById('exam-notes').value = '';
    loadExamDates();
    loadExamCountdown();
  } catch(e) { toast(e.message, 'error'); }
}

async function deleteExam(id) {
  try {
    await api('DELETE', `/api/exam-dates/${id}`);
    loadExamDates();
    loadExamCountdown();
  } catch(e) {}
}

async function generateStudyPlan() {
  const sel = document.getElementById('plan-exam-select').value;
  if (!sel) { toast('Please select an exam first', 'error'); return; }
  const [exam_date, subject] = sel.split('|');
  loading(true, 'Building your personalised study plan…');
  try {
    const plan = await api('POST', '/api/generate/studyplan', { exam_date, subject });
    renderStudyPlan(plan);
  } catch(e) { toast(e.message, 'error'); } finally { loading(false); }
}

function renderStudyPlan(plan) {
  document.getElementById('plan-empty').classList.add('hidden');

  const overview = document.getElementById('plan-overview');
  overview.classList.remove('hidden');
  document.getElementById('plan-overview-text').textContent = plan.overview || '';
  document.getElementById('plan-hours-text').textContent = `Recommended: ${plan.daily_hours} hours/day`;

  const days = document.getElementById('plan-days');
  days.innerHTML = (plan.days || []).map(d => {
    const priorityLabel = { high: '🔴 High priority', medium: '🟡 Medium', low: '🟢 Low' }[d.priority] || '';
    return `<div class="plan-day ${d.priority || 'medium'}">
      <div class="flex items-start justify-between mb-2">
        <div>
          <span class="text-xs font-bold text-slate-400 uppercase">Day ${d.day}</span>
          <h3 class="font-semibold text-slate-800 mt-0.5">${d.focus}</h3>
        </div>
        <span class="text-xs text-slate-400">${priorityLabel}</span>
      </div>
      <ul class="space-y-1.5">
        ${(d.tasks || []).map(t => `<li class="flex gap-2 text-sm text-slate-600"><span class="text-teal-500 mt-0.5">•</span>${t}</li>`).join('')}
      </ul>
    </div>`;
  }).join('');
}

// ── Sidebar collapse ──────────────────────────────────────────────────────
function toggleSidebar() {
  const sb = document.getElementById('sidebar');
  sb.classList.toggle('sb-collapsed');
  const prefs = getSettingsPrefs();
  prefs.sidebarCollapsed = sb.classList.contains('sb-collapsed');
  saveSettingsPrefs(prefs);
}

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
  const t = THEMES[name] || THEMES.ocean;
  const r = document.documentElement;
  r.style.setProperty('--navy',           t.navy);
  r.style.setProperty('--teal',           t.teal);
  r.style.setProperty('--teal-d',         t.tealD);
  r.style.setProperty('--nav-active-bg',  t.navBg);
  r.style.setProperty('--nav-active-text',t.navTxt);
}

function setTheme(name) {
  applyTheme(name);
  document.querySelectorAll('.theme-swatch').forEach(s =>
    s.classList.toggle('active', s.dataset.theme === name));
  const prefs = getSettingsPrefs();
  prefs.theme = name;
  saveSettingsPrefs(prefs);
}

function renderThemePicker() {
  const prefs = getSettingsPrefs();
  const current = prefs.theme || 'ocean';
  const el = document.getElementById('theme-picker');
  if (!el) return;
  el.innerHTML = Object.entries(THEMES).map(([key, t]) => `
    <button class="theme-swatch ${key === current ? 'active' : ''}" data-theme="${key}" onclick="setTheme('${key}')" title="${t.name}">
      <div class="theme-swatch-preview">
        <div class="theme-swatch-sidebar" style="background:${t.navy}"></div>
        <div class="theme-swatch-content">
          <div style="background:${t.teal};height:5px;border-radius:3px;width:60%"></div>
          <div style="background:#e2e8f0;height:4px;border-radius:2px;width:90%;margin-top:4px"></div>
          <div style="background:#e2e8f0;height:4px;border-radius:2px;width:70%;margin-top:3px"></div>
        </div>
      </div>
      <div class="theme-swatch-name">${t.name}</div>
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
        <div class="p-3 bg-teal-50 rounded-xl border border-teal-200 mb-3">
          <div class="flex items-center gap-2 mb-1">
            <span class="text-xs font-bold uppercase tracking-widest text-teal-600">🌐 Internet (Cloudflare Tunnel)</span>
            <span class="text-xs text-teal-400">— live now</span>
          </div>
          <div class="flex items-center gap-2">
            <code class="flex-1 text-sm font-mono text-teal-800 break-all">${data.tunnel_url}</code>
            <button onclick="navigator.clipboard.writeText('${data.tunnel_url}').then(()=>toast('Tunnel URL copied!','success'))"
              class="text-xs bg-teal-500 hover:bg-teal-600 text-white font-semibold px-3 py-1.5 rounded-lg flex-shrink-0">Copy</button>
          </div>
          <p class="text-teal-600 text-xs mt-1.5">Send this to anyone — works from anywhere in the world. Runs automatically on startup.</p>
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
            class="text-xs text-teal-600 hover:text-teal-800 font-medium flex-shrink-0">Copy</button>
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
  if (prefs.theme)    applyTheme(prefs.theme);
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
    const b = await api('GET', url);

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
  let out = `I'm a student studying ${subject}. Below is my study context exported from my study app (UniAssist). `
          + `Please use it to help me — answer questions, quiz me, explain my weak areas, or build a study plan.\n`;

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
          class="flex-1 py-2 text-sm font-semibold transition-colors ${isLogin ? 'bg-teal-500 text-white' : 'bg-white/5 text-slate-400 hover:text-white'}">
          Log in
        </button>
        <button id="tab-register" onclick="_authMode='register';renderAuthUI()"
          class="flex-1 py-2 text-sm font-semibold transition-colors ${!isLogin ? 'bg-teal-500 text-white' : 'bg-white/5 text-slate-400 hover:text-white'}">
          Sign up
        </button>
      </div>
      ${_profiles.length && isLogin ? `
        <div class="flex flex-wrap gap-2 mb-4 justify-center">
          ${_profiles.map(p => `
            <button data-uname="${sEsc(p.username)}" class="profile-card px-3 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-sm transition-colors">
              <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-teal-400 text-white text-xs font-bold mr-1.5">${(p.username[0]||'?').toUpperCase()}</span>
              ${sEsc(p.username)}
            </button>`).join('')}
        </div>` : ''}
      <input id="auth-username" class="w-full px-4 py-3 rounded-xl bg-white/10 text-white placeholder-slate-400 border border-white/20 text-sm outline-none focus:border-teal-400 mb-3"
        placeholder="Username" maxlength="40" autocomplete="username" />
      <input id="auth-password" type="password" class="w-full px-4 py-3 rounded-xl bg-white/10 text-white placeholder-slate-400 border border-white/20 text-sm outline-none focus:border-teal-400 mb-3"
        placeholder="Password" autocomplete="${isLogin ? 'current-password' : 'new-password'}" />
      <p id="auth-error" class="text-red-400 text-sm mb-3 hidden"></p>
      <button onclick="submitAuth()" class="w-full py-3 rounded-xl font-semibold text-white text-sm"
        style="background:var(--teal)">${isLogin ? 'Log in' : 'Create account'} →</button>
      <p class="text-slate-500 text-xs text-center mt-4">
        ${isLogin ? "Don't have an account?" : 'Already have an account?'}
        <a href="#" onclick="_authMode='${isLogin ? 'register' : 'login'}';renderAuthUI();return false" class="text-teal-400 hover:underline">
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
  el.innerHTML = '<p class="text-slate-400 text-sm">Loading…</p>';
  try {
    const mats = await api('GET', '/api/discover');
    renderDiscover(mats);
  } catch(e) { el.innerHTML = `<p class="text-red-400 text-sm">${e.message}</p>`; }
}

function renderDiscover(mats) {
  const el = document.getElementById('discover-list');
  if (!mats.length) {
    el.innerHTML = '<p class="text-slate-400 text-sm">No shared materials yet. When someone marks a material public (Materials → 🔒/🌐 toggle), it appears here.</p>';
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
  try { S.materials = await api('GET', '/api/materials'); } catch(e) {}
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

const barsEl     = document.getElementById('bars');
const cmpEl      = document.getElementById('cmpCount');
const swapEl     = document.getElementById('swapCount');
const stepEl     = document.getElementById('stepCount');
const totalEl    = document.getElementById('totalSteps');
const startBtn   = document.getElementById('startBtn');
const stopBtn    = document.getElementById('stopBtn');
const randomBtn  = document.getElementById('randomBtn');
const sizeSlider = document.getElementById('sizeSlider');
const speedSlider= document.getElementById('speedSlider');
const sizeOut    = document.getElementById('sizeOut');
const speedOut   = document.getElementById('speedOut');

let currentArray = [];
let steps        = [];
let timer        = null;
let running      = false;

// ── Helpers ────────────────────────────────────────────────────────────────

function getDelay() {
  const s = parseInt(speedSlider.value);
  return Math.max(8, Math.round(600 / (s * s)));
}

function renderBars(arr, cmpIdx = [], swapIdx = [], doneIdx = []) {
  const max = Math.max(...arr);
  const cmpSet  = new Set(cmpIdx);
  const swapSet = new Set(swapIdx);
  const doneSet = new Set(doneIdx);

  barsEl.innerHTML = '';
  arr.forEach((v, i) => {
    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.style.height = Math.round((v / max) * 100) + '%';

    if      (doneSet.has(i)) bar.classList.add('done');
    else if (swapSet.has(i)) bar.classList.add('swap');
    else if (cmpSet.has(i))  bar.classList.add('cmp');

    barsEl.appendChild(bar);
  });
}

function resetStats() {
  cmpEl.textContent  = '0';
  swapEl.textContent = '0';
  stepEl.textContent = '0';
  totalEl.textContent = '—';
}

function setRunning(state) {
  running = state;
  startBtn.disabled = state;
  stopBtn.disabled  = !state;
  randomBtn.disabled = state;
}

// ── API calls ──────────────────────────────────────────────────────────────

async function fetchArray() {
  const size = parseInt(sizeSlider.value);
  const mode = document.getElementById('mode').value;
  const res  = await fetch(`/api/array?size=${size}&mode=${mode}`);
  const data = await res.json();
  return data.array;
}

async function fetchSteps(array, algorithm) {
  const res = await fetch('/api/sort', {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify({ array, algorithm }),
  });
  const data = await res.json();
  return data.steps;
}

// ── Playback ───────────────────────────────────────────────────────────────

function playSteps() {
  let idx = 0;

  function tick() {
    if (idx >= steps.length) {
      setRunning(false);
      return;
    }
    const st = steps[idx++];
    renderBars(st.arr, st.cmp, st.swap, st.done);
    cmpEl.textContent  = st.cmps;
    swapEl.textContent = st.swaps;
    stepEl.textContent = idx;
    timer = setTimeout(tick, getDelay());
  }

  tick();
}

// ── Init ───────────────────────────────────────────────────────────────────

async function init() {
  clearTimeout(timer);
  setRunning(false);
  resetStats();
  currentArray = await fetchArray();
  renderBars(currentArray);
}

// ── Event handlers ─────────────────────────────────────────────────────────

randomBtn.addEventListener('click', init);

sizeSlider.addEventListener('input', () => {
  sizeOut.textContent = sizeSlider.value;
  init();
});

speedSlider.addEventListener('input', () => {
  speedOut.textContent = speedSlider.value;
});

startBtn.addEventListener('click', async () => {
  const algo = document.getElementById('algo').value;
  setRunning(true);
  steps = await fetchSteps(currentArray, algo);
  totalEl.textContent = steps.length;
  playSteps();
});

stopBtn.addEventListener('click', () => {
  clearTimeout(timer);
  setRunning(false);
  init();
});

// Start
init();

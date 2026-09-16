const $ = id => document.getElementById(id);
const canvas = $('board'), ctx = canvas.getContext('2d');
let game, state, loading = false, previous = 0, accumulator = 0, pointer = -1, touchAxis = 0;
const keys = new Set();
function draw(s) {
  ctx.fillStyle = '#101523'; ctx.fillRect(0, 0, 900, 540);
  ctx.strokeStyle = '#2c3348'; ctx.lineWidth = 2; ctx.setLineDash([8, 14]);
  ctx.beginPath(); ctx.moveTo(450, 15); ctx.lineTo(450, 525); ctx.stroke(); ctx.setLineDash([]);
  ctx.fillStyle = '#9cf1e2'; ctx.fillRect(36, s.left - 48, 14, 96);
  ctx.fillStyle = '#eb96be'; ctx.fillRect(850, s.right - 48, 14, 96);
  ctx.shadowColor = '#eef3ff'; ctx.shadowBlur = 15; ctx.fillStyle = '#eef3ff';
  ctx.beginPath(); ctx.arc(s.x, s.y, 9, 0, Math.PI * 2); ctx.fill(); ctx.shadowBlur = 0;
}
function sync() {
  const old = state?.status;
  state = JSON.parse(game.snapshot()); draw(state);
  $('you').textContent = String(state.scores[0]).padStart(2, '0');
  $('computer').textContent = String(state.scores[1]).padStart(2, '0');
  $('rally').textContent = state.rally; $('best').textContent = state.best_rally;
  if(old === state.status) return;
  $('overlay').hidden = state.status === 'running';
  $('pause').disabled = state.status !== 'running';
  $('start').disabled = state.status === 'running';
  $('start').textContent = state.status === 'paused' ? 'Resume ↗' : state.status === 'over' ? 'Play again ↗' : 'Start match ↗';
  const copy = {
    ready: ['THE COURT IS YOURS', 'Meet your match.', 'A little timing goes a long way.', 'Ready. You control the left paddle.'],
    running: ['', '', '', 'Keep the rally alive. Space pauses the match.'],
    paused: ['TAKE YOUR TIME', 'A little breather.', 'Your match will be right here.', 'Paused. Select Resume to continue.'],
    over: ['MATCH COMPLETE', state.scores[0] >= 7 ? 'Your court. Your win.' : 'The rematch is yours.', `Final score: ${state.scores[0]} – ${state.scores[1]}`, 'Match complete. Play again for a fresh start.']
  }[state.status];
  [$('overlay-label').textContent, $('overlay-title').textContent, $('overlay-text').textContent, $('status').textContent] = copy;
}
function clearInput() { keys.clear(); touchAxis = 0; pointer = -1; }
function start() { if(!game) return load(); clearInput(); game.start(); previous = 0; accumulator = 0; sync(); canvas.focus({preventScroll:true}); }
function pause() { clearInput(); if(game) { game.pause(); sync(); } }
function reset() { if(game) { clearInput(); game.reset(); previous = 0; accumulator = 0; sync(); } }
function frame(now) {
  if(game && state.status === 'running') {
    accumulator += previous ? Math.min((now - previous) / 1000, .05) : 0;
    const axis = touchAxis || (Number(keys.has('ArrowDown') || keys.has('s')) - Number(keys.has('ArrowUp') || keys.has('w')));
    while(accumulator >= 1/120) { game.step(1/120, axis, pointer); accumulator -= 1/120; }
    sync();
  }
  previous = now; requestAnimationFrame(frame);
}
$('start').addEventListener('click', start); $('pause').addEventListener('click', pause); $('reset').addEventListener('click', reset);
canvas.addEventListener('keydown', event => {
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if(['ArrowUp','ArrowDown','w','s'].includes(key)) { event.preventDefault(); keys.add(key); pointer = -1; }
  if(event.code === 'Space') { event.preventDefault(); if(!event.repeat) state?.status === 'running' ? pause() : start(); }
  if(key === 'r' && !event.repeat) reset();
});
window.addEventListener('keyup', event => keys.delete(event.key.length === 1 ? event.key.toLowerCase() : event.key));
canvas.addEventListener('blur', pause);
function aim(event) { const rect = canvas.getBoundingClientRect(); pointer = Math.max(0, Math.min(540, (event.clientY - rect.top) * 540 / rect.height)); }
canvas.addEventListener('pointerdown', event => { canvas.focus({preventScroll:true}); canvas.setPointerCapture(event.pointerId); aim(event); });
canvas.addEventListener('pointermove', event => { if(canvas.hasPointerCapture(event.pointerId)) aim(event); });
for(const name of ['pointerup','pointercancel','lostpointercapture']) canvas.addEventListener(name, () => { pointer = -1; });
for(const button of document.querySelectorAll('[data-axis]')) {
  button.addEventListener('pointerdown', event => { event.preventDefault(); canvas.focus({preventScroll:true}); button.setPointerCapture(event.pointerId); touchAxis = Number(button.dataset.axis); pointer = -1; });
  for(const name of ['pointerup','pointercancel','lostpointercapture']) button.addEventListener(name, () => { touchAxis = 0; });
}
window.addEventListener('blur', pause); document.addEventListener('visibilitychange', () => { if(document.hidden) pause(); });
async function load() {
  if(loading) return; loading = true; $('start').disabled = true;
  $('status').textContent = 'Loading Python. The first visit may take a moment.';
  try {
    const {loadPyodide} = await import('https://cdn.jsdelivr.net/pyodide/v314.0.7/full/pyodide.mjs');
    const py = await loadPyodide();
    const response = await fetch('engine.py'); if(!response.ok) throw new Error('Game rules unavailable');
    py.runPython(await response.text()); py.runPython('game = Game()'); game = py.globals.get('game');
    $('reset').disabled = false; sync();
  } catch(error) {
    console.error(error); $('overlay-title').textContent = 'Let’s try that again.';
    $('overlay-text').textContent = 'Check your connection, then select Retry.';
    $('status').textContent = 'Python could not load.'; $('start').textContent = 'Retry'; $('start').disabled = false;
  } finally { loading = false; }
}
draw({left:270,right:270,x:450,y:270}); requestAnimationFrame(frame); load();

// DebateClock — Pure state reducer
// No DOM, no sync, no side effects. Takes state → returns new state.
// Timestamps are Date.now() values. Durations are milliseconds.
// All "remaining" values are computed on-the-fly from stored state.

// ─── SPEECH TIMER ────────────────────────────────────────────────────────────

export function currentSpeech(state) {
  return state.speeches[state.currentSpeechIdx] || null;
}

export function currentSpeechDurationMs(state) {
  const sp = currentSpeech(state);
  return sp ? sp.duration * 1000 : 0;
}

// ms elapsed into the current speech, right now
export function speechElapsedMs(state, now = Date.now()) {
  if (state.speechRunning && state.speechStartedAt != null) {
    return state.speechPausedElapsedMs + (now - state.speechStartedAt);
  }
  return state.speechPausedElapsedMs;
}

// ms remaining. Can go negative (overtime).
export function speechRemainingMs(state, now = Date.now()) {
  return currentSpeechDurationMs(state) - speechElapsedMs(state, now);
}

export function startSpeech(state, now = Date.now()) {
  // Starting a speech auto-pauses any active prep
  let next = { ...state };
  if (next.activePrepSide) {
    next = stopPrep(next, now);
  }
  return {
    ...next,
    speechRunning: true,
    speechStartedAt: now,
  };
}

export function pauseSpeech(state, now = Date.now()) {
  if (!state.speechRunning) return state;
  return {
    ...state,
    speechRunning: false,
    speechPausedElapsedMs: speechElapsedMs(state, now),
    speechStartedAt: null,
  };
}

export function resetSpeech(state) {
  return {
    ...state,
    speechRunning: false,
    speechStartedAt: null,
    speechPausedElapsedMs: 0,
  };
}

export function nextSpeech(state, now = Date.now()) {
  // Also stops any active prep when advancing
  let next = state;
  if (next.activePrepSide) next = stopPrep(next, now);
  const nextIdx = Math.min(next.currentSpeechIdx + 1, next.speeches.length - 1);
  return {
    ...next,
    currentSpeechIdx: nextIdx,
    speechRunning: false,
    speechStartedAt: null,
    speechPausedElapsedMs: 0,
  };
}

export function prevSpeech(state, now = Date.now()) {
  let next = state;
  if (next.activePrepSide) next = stopPrep(next, now);
  const prevIdx = Math.max(next.currentSpeechIdx - 1, 0);
  return {
    ...next,
    currentSpeechIdx: prevIdx,
    speechRunning: false,
    speechStartedAt: null,
    speechPausedElapsedMs: 0,
  };
}

export function jumpToSpeech(state, idx, now = Date.now()) {
  let next = state;
  if (next.activePrepSide) next = stopPrep(next, now);
  const clamped = Math.max(0, Math.min(idx, next.speeches.length - 1));
  return {
    ...next,
    currentSpeechIdx: clamped,
    speechRunning: false,
    speechStartedAt: null,
    speechPausedElapsedMs: 0,
  };
}

// Adjust speech elapsed by ±ms (for -30s / +30s buttons)
// deltaMs > 0 means "add time" (reduce elapsed, extend speech)
export function adjustSpeech(state, deltaMs, now = Date.now()) {
  const currentElapsed = speechElapsedMs(state, now);
  const newElapsed = Math.max(0, currentElapsed - deltaMs);
  if (state.speechRunning) {
    return {
      ...state,
      speechStartedAt: now,
      speechPausedElapsedMs: newElapsed,
    };
  }
  return { ...state, speechPausedElapsedMs: newElapsed };
}

// ─── PREP POOL ───────────────────────────────────────────────────────────────

// ms of prep currently consumed for a side (including in-flight if active)
export function prepConsumedMs(state, side, now = Date.now()) {
  const base = state.prepConsumedMs[side] || 0;
  if (state.activePrepSide === side && state.prepStartedAt != null) {
    return base + (now - state.prepStartedAt);
  }
  return base;
}

// ms of prep remaining for a side
export function prepRemainingMs(state, side, now = Date.now()) {
  const total = state.prepPoolTotalMs[side] || 0;
  return Math.max(0, total - prepConsumedMs(state, side, now));
}

export function startPrep(state, side, now = Date.now()) {
  if (!['aff', 'neg'].includes(side)) return state;
  if (prepRemainingMs(state, side, now) <= 0) return state;  // no prep left

  // Starting prep auto-pauses speech
  let next = state;
  if (next.speechRunning) {
    next = pauseSpeech(next, now);
  }
  // If the other side's prep is active, stop it first (saves their consumed ms)
  if (next.activePrepSide && next.activePrepSide !== side) {
    next = stopPrep(next, now);
  }
  return {
    ...next,
    activePrepSide: side,
    prepStartedAt: now,
  };
}

export function stopPrep(state, now = Date.now()) {
  if (!state.activePrepSide || state.prepStartedAt == null) return state;
  const side = state.activePrepSide;
  const consumed = (state.prepConsumedMs[side] || 0) + (now - state.prepStartedAt);
  const capped = Math.min(consumed, state.prepPoolTotalMs[side] || 0);
  return {
    ...state,
    activePrepSide: null,
    prepStartedAt: null,
    prepConsumedMs: {
      ...state.prepConsumedMs,
      [side]: capped,
    },
  };
}

export function resetPrep(state) {
  return {
    ...state,
    activePrepSide: null,
    prepStartedAt: null,
    prepConsumedMs: { aff: 0, neg: 0 },
  };
}

// ─── DISPLAY / UX ────────────────────────────────────────────────────────────

export function toggleBlackout(state) {
  return { ...state, blackout: !state.blackout };
}

export function triggerFlash(state) {
  return { ...state, flash: true };
}

export function clearFlash(state) {
  return { ...state, flash: false };
}

export function toggleVanish(state) {
  return { ...state, vanishAtZero: !state.vanishAtZero };
}

// ─── COLOR PHASE LOGIC ───────────────────────────────────────────────────────
// green (>60s) → yellow (30-60s) → red (0-30s) → flashing red (overtime)

export function speechPhase(state, now = Date.now()) {
  const remaining = speechRemainingMs(state, now);
  if (remaining <= 0) return 'overtime';
  if (remaining <= 30_000) return 'critical';
  if (remaining <= 60_000) return 'warn';
  return 'go';
}

// Parli POI window: 1:00–6:00 into 7-min constructives, POI signal allowed

// POI window check -- works for WSDC, BP, and legacy Parli formats.
// Speeches with POI windows carry poiStartSec / poiEndSec fields.
export function poiWindow(state, now) {
  if (now === undefined) now = Date.now();
  var sp = currentSpeech(state);
  if (!sp) return false;
  var elapsed = speechElapsedMs(state, now);
  if (sp.poiStartSec != null && sp.poiEndSec != null) {
    return elapsed >= sp.poiStartSec * 1000 && elapsed <= sp.poiEndSec * 1000;
  }
  if (state.format === "Parli") {
    if (sp.duration < 420) return false;
    return elapsed >= 60000 && elapsed <= (sp.duration - 60) * 1000;
  }
  return false;
}

// Backward-compat alias
export var parliPOIWindow = poiWindow;

// Legacy (alias above)
export function parliPOIWindow_UNUSED(state, now = Date.now()) {
  const sp = currentSpeech(state);
  if (!sp || state.format !== 'Parli') return false;
  if (sp.duration < 420) return false;  // POI only in 7-min constructives
  const elapsed = speechElapsedMs(state, now);
  return elapsed >= 60_000 && elapsed <= (sp.duration - 60) * 1000;
}

// ─── FORMATTING ──────────────────────────────────────────────────────────────

export function formatClock(ms, showSign = true) {
  const neg = ms < 0;
  const abs = Math.abs(ms);
  const totalSec = Math.floor(abs / 1000);
  const m = Math.floor(totalSec / 60);
  const s = totalSec % 60;
  const str = `${m}:${String(s).padStart(2, '0')}`;
  return neg && showSign ? `-${str}` : str;
}

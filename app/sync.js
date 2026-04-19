// DebateClock — PartyKit client wrapper
// Single module used by both judge controller and debater display.
// Mirrors cuelight pattern: announce role on connect, listen for state broadcasts.

// PartyKit host — update AFTER you run `npx partykit deploy`
// Local dev: automatically uses 127.0.0.1:1999 when serving from localhost
const PROD_HOST = 'debateclock.metriclogic26.partykit.dev';
const DEV_HOST = '127.0.0.1:1999';

function defaultHost() {
  if (typeof location === 'undefined') return PROD_HOST;
  const h = location.hostname;
  if (h === 'localhost' || h === '127.0.0.1' || h.startsWith('192.168.') || h.startsWith('10.')) {
    return DEV_HOST;
  }
  return PROD_HOST;
}

// ─── ROOM CODE HELPERS ──────────────────────────────────────────────────────

export function makeRoomCode() {
  // 6-char uppercase, easy to read aloud (no 0/O, 1/I ambiguity)
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}

export function normalizeRoomCode(input) {
  return String(input || '')
    .toUpperCase()
    .replace(/[^A-Z0-9]/g, '')
    .slice(0, 6);
}

// Deterministic 6-char code from a string — used for /j/[judge-name] paradigm links
export function hashToCode(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = ((h << 5) - h + str.charCodeAt(i)) | 0;
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
  let out = '';
  let v = Math.abs(h) || 1;
  for (let i = 0; i < 6; i++) { out += chars[v % chars.length]; v = Math.floor(v / chars.length) || 1; }
  return out;
}

// ─── WEBSOCKET CLIENT ───────────────────────────────────────────────────────

export class DebateClockSocket {
  constructor({ room, role, host, onState, onDeviceCount, onStatus }) {
    this.room = room;
    this.role = role;  // 'controller' | 'display'
    this.host = host || defaultHost();
    this.onState = onState || (() => {});
    this.onDeviceCount = onDeviceCount || (() => {});
    this.onStatus = onStatus || (() => {});
    this.ws = null;
    this.reconnectAttempts = 0;
    this.reconnectTimer = null;
    this.manualClose = false;
    this.connect();
  }

  _url() {
    const isLocal = this.host.startsWith('127.0.0.1') || this.host.startsWith('localhost');
    const proto = isLocal ? 'ws' : 'wss';
    return `${proto}://${this.host}/parties/main/${encodeURIComponent(this.room)}`;
  }

  connect() {
    this.manualClose = false;
    this.onStatus('connecting');

    try {
      this.ws = new WebSocket(this._url());
    } catch (e) {
      this._scheduleReconnect();
      return;
    }

    this.ws.addEventListener('open', () => {
      this.reconnectAttempts = 0;
      this.onStatus('connected');
      // Announce role
      this.send({
        type: this.role === 'display' ? 'display_join' : 'controller_join',
      });
    });

    this.ws.addEventListener('message', (ev) => {
      try {
        const data = JSON.parse(ev.data);
        if (data.type === 'state' && data.state) {
          this.onState(data.state);
        } else if (data.type === 'device_count') {
          this.onDeviceCount(data.displayCount);
        }
      } catch (e) {}
    });

    this.ws.addEventListener('close', () => {
      this.onStatus('disconnected');
      if (!this.manualClose) this._scheduleReconnect();
    });

    this.ws.addEventListener('error', () => {
      this.onStatus('error');
    });
  }

  _scheduleReconnect() {
    clearTimeout(this.reconnectTimer);
    const delay = Math.min(1000 * Math.pow(1.6, this.reconnectAttempts), 15000);
    this.reconnectAttempts++;
    this.reconnectTimer = setTimeout(() => this.connect(), delay);
  }

  send(obj) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(obj));
      return true;
    }
    return false;
  }

  sendState(state) {
    return this.send({ type: 'state_update', state });
  }

  sendPatch(patch) {
    return this.send({ type: 'state_patch', patch });
  }

  close() {
    this.manualClose = true;
    clearTimeout(this.reconnectTimer);
    if (this.ws) this.ws.close();
  }
}

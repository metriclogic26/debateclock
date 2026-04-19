// DebateClock PartyKit server
// Room-scoped state. Broadcasts timestamps (not countdowns) — clients compute remaining locally.
// Pattern mirrors cuelight/party/index.js

export default class DebateClockServer {
  constructor(room) {
    this.room = room;

    // Authoritative room state. Clients compute everything else from these fields.
    this.state = {
      // Format & speech list
      format: 'LD',                // 'LD' | 'Policy' | 'PF' | 'Parli' | 'custom'
      speeches: [],                // populated by judge on format select
      currentSpeechIdx: 0,

      // Speech timer — timestamp model (drift-proof across devices)
      speechRunning: false,
      speechStartedAt: null,       // Date.now() when last started, else null
      speechPausedElapsedMs: 0,    // ms accumulated before current pause

      // Prep pools (per side). Remaining = poolTotal - consumed.
      prepPoolTotalMs: { aff: 0, neg: 0 },
      prepConsumedMs:  { aff: 0, neg: 0 },
      activePrepSide: null,        // 'aff' | 'neg' | null
      prepStartedAt: null,         // Date.now() when active prep started

      // Display options
      vanishAtZero: true,
      flash: false,
      blackout: false,

      // Metadata
      judgeName: '',
      lastUpdatedBy: null,
      lastUpdatedAt: Date.now(),
    };

    this.displays = new Set();
    this.controllers = new Set();
  }

  onConnect(conn) {
    // Send current full state to new joiner
    conn.send(JSON.stringify({ type: 'state', state: this.state }));
  }

  onMessage(message, sender) {
    try {
      const data = JSON.parse(message);

      // Role announcement
      if (data.type === 'display_join') {
        this.displays.add(sender.id);
        this._broadcastDeviceCount();
        return;
      }
      if (data.type === 'controller_join') {
        this.controllers.add(sender.id);
        this._sendDeviceCountTo(sender);
        return;
      }

      // Ping for connection health
      if (data.type === 'ping') {
        sender.send(JSON.stringify({ type: 'pong', t: Date.now() }));
        return;
      }

      // Full state replacement from judge (controller is authoritative)
      if (data.type === 'state_update' && data.state) {
        this.state = {
          ...data.state,
          lastUpdatedBy: sender.id,
          lastUpdatedAt: Date.now(),
        };
        this.room.broadcast(
          JSON.stringify({ type: 'state', state: this.state }),
          [sender.id]  // don't echo back to sender
        );
        return;
      }

      // Patch update — partial merge, for smaller payloads
      if (data.type === 'state_patch' && data.patch) {
        this.state = {
          ...this.state,
          ...data.patch,
          lastUpdatedBy: sender.id,
          lastUpdatedAt: Date.now(),
        };
        this.room.broadcast(
          JSON.stringify({ type: 'state', state: this.state }),
          [sender.id]
        );
        return;
      }
    } catch (e) {
      // swallow malformed messages
    }
  }

  onClose(conn) {
    const wasDisplay = this.displays.has(conn.id);
    this.displays.delete(conn.id);
    this.controllers.delete(conn.id);
    if (wasDisplay) this._broadcastDeviceCount();
  }

  _broadcastDeviceCount() {
    const msg = JSON.stringify({
      type: 'device_count',
      displayCount: this.displays.size,
    });
    for (const id of this.controllers) {
      try { this.room.getConnection(id)?.send(msg); } catch (e) {}
    }
  }

  _sendDeviceCountTo(conn) {
    try {
      conn.send(JSON.stringify({
        type: 'device_count',
        displayCount: this.displays.size,
      }));
    } catch (e) {}
  }
}

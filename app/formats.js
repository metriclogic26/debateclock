// DebateClock — Format presets (pure data, no logic)
// Durations in seconds. prepPoolSeconds is per-side allocation.
// CX = Cross-Examination (no prep allowed during CX in most formats)

export const FORMATS = {
  LD: {
    id: 'LD',
    name: 'Lincoln-Douglas',
    shortName: 'LD',
    prepPoolSeconds: { aff: 240, neg: 240 },  // 4 min each
    speeches: [
      { id: 'ac',   label: 'Affirmative Constructive (AC)', side: 'aff', duration: 360, isCX: false },
      { id: 'cx1',  label: 'Neg CX of Aff',                  side: 'neg', duration: 180, isCX: true  },
      { id: 'nc',   label: 'Negative Constructive (NC)',     side: 'neg', duration: 420, isCX: false },
      { id: 'cx2',  label: 'Aff CX of Neg',                  side: 'aff', duration: 180, isCX: true  },
      { id: '1ar',  label: '1st Affirmative Rebuttal (1AR)', side: 'aff', duration: 240, isCX: false },
      { id: 'nr',   label: 'Negative Rebuttal (NR)',         side: 'neg', duration: 360, isCX: false },
      { id: '2ar',  label: '2nd Affirmative Rebuttal (2AR)', side: 'aff', duration: 180, isCX: false },
    ],
  },

  Policy: {
    id: 'Policy',
    name: 'Policy Debate (CX)',
    shortName: 'Policy',
    prepPoolSeconds: { aff: 480, neg: 480 },  // 8 min per team
    speeches: [
      { id: '1ac', label: '1st Aff Constructive (1AC)', side: 'aff', duration: 480, isCX: false },
      { id: 'cx1', label: 'Neg CX of 1AC',               side: 'neg', duration: 180, isCX: true  },
      { id: '1nc', label: '1st Neg Constructive (1NC)',  side: 'neg', duration: 480, isCX: false },
      { id: 'cx2', label: 'Aff CX of 1NC',               side: 'aff', duration: 180, isCX: true  },
      { id: '2ac', label: '2nd Aff Constructive (2AC)',  side: 'aff', duration: 480, isCX: false },
      { id: 'cx3', label: 'Neg CX of 2AC',               side: 'neg', duration: 180, isCX: true  },
      { id: '2nc', label: '2nd Neg Constructive (2NC)',  side: 'neg', duration: 480, isCX: false },
      { id: 'cx4', label: 'Aff CX of 2NC',               side: 'aff', duration: 180, isCX: true  },
      { id: '1nr', label: '1st Neg Rebuttal (1NR)',      side: 'neg', duration: 300, isCX: false },
      { id: '1ar', label: '1st Aff Rebuttal (1AR)',      side: 'aff', duration: 300, isCX: false },
      { id: '2nr', label: '2nd Neg Rebuttal (2NR)',      side: 'neg', duration: 300, isCX: false },
      { id: '2ar', label: '2nd Aff Rebuttal (2AR)',      side: 'aff', duration: 300, isCX: false },
    ],
  },

  // PF — corrected NSDA 2025-26 order
  PF: {
    id: 'PF',
    name: 'Public Forum',
    shortName: 'PF',
    prepPoolSeconds: { aff: 180, neg: 180 },  // 3 min per team, distributed freely
    speeches: [
      { id: 'a1',   label: '1st Speaker — Team A (Pro)', side: 'aff',     duration: 240, isCX: false },
      { id: 'b1',   label: '1st Speaker — Team B (Con)', side: 'neg',     duration: 240, isCX: false },
      { id: 'cx1',  label: 'Crossfire #1',                side: 'neutral', duration: 180, isCX: true  },
      { id: 'a2',   label: '2nd Speaker — Team A',        side: 'aff',     duration: 240, isCX: false },
      { id: 'b2',   label: '2nd Speaker — Team B',        side: 'neg',     duration: 240, isCX: false },
      { id: 'cx2',  label: 'Crossfire #2',                side: 'neutral', duration: 180, isCX: true  },
      { id: 'suma', label: 'Summary — Team A',            side: 'aff',     duration: 180, isCX: false },
      { id: 'sumb', label: 'Summary — Team B',            side: 'neg',     duration: 180, isCX: false },
      { id: 'gcx',  label: 'Grand Crossfire',             side: 'neutral', duration: 180, isCX: true  },
      { id: 'ffa',  label: 'Final Focus — Team A',        side: 'aff',     duration: 120, isCX: false },
      { id: 'ffb',  label: 'Final Focus — Team B',        side: 'neg',     duration: 120, isCX: false },
    ],
  },

  Parli: {
    id: 'Parli',
    name: 'Parliamentary (no prep)',
    shortName: 'Parli',
    prepPoolSeconds: { aff: 0, neg: 0 },  // no prep in Parli
    // POI window: 1:00–6:00 into 7-min constructives (visual cue, handled in display)
    speeches: [
      { id: 'pmc', label: 'Prime Minister Constructive (PMC)',       side: 'aff', duration: 420, isCX: false },
      { id: 'loc', label: 'Leader of Opposition Constructive (LOC)', side: 'neg', duration: 420, isCX: false },
      { id: 'mgc', label: 'Member of Government Constructive (MGC)', side: 'aff', duration: 420, isCX: false },
      { id: 'moc', label: 'Member of Opposition Constructive (MOC)', side: 'neg', duration: 420, isCX: false },
      { id: 'lor', label: 'Leader of Opposition Rebuttal (LOR)',     side: 'neg', duration: 240, isCX: false },
      { id: 'pmr', label: 'Prime Minister Rebuttal (PMR)',           side: 'aff', duration: 240, isCX: false },
    ],
  },

  WSDC: {
    id: 'WSDC',
    name: 'World Schools (WSDC)',
    shortName: 'WSDC',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // POI window: min 1-7 of each 8-min constructive. Reply speeches have no POI.
    // Bell schedule: 1:00 (POIs open), 7:00 (POIs close), 8:00 (double bell).
    speeches: [
      { id: 'p1',     label: '1st Proposition',   side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o1',     label: '1st Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'p2',     label: '2nd Proposition',    side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o2',     label: '2nd Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'p3',     label: '3rd Proposition',    side: 'aff', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'o3',     label: '3rd Opposition',     side: 'neg', duration: 480, isCX: false, poiStartSec: 60, poiEndSec: 420 },
      { id: 'oreply', label: 'Opposition Reply',   side: 'neg', duration: 240, isCX: false },
      { id: 'preply', label: 'Proposition Reply',  side: 'aff', duration: 240, isCX: false },
    ],
  },

  BPUni: {
    id: 'BPUni',
    name: 'British Parliamentary (Uni / WUDC)',
    shortName: 'BP',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // 4 teams: OG (Opening Gov) = aff, OO (Opening Opp) = neg,
    //          CG (Closing Gov) = aff, CO (Closing Opp) = neg
    // POI window: min 1-6 of each 7-min speech.
    speeches: [
      { id: 'pm',  label: 'Prime Minister (OG)',              side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'lo',  label: 'Leader of Opposition (OO)',        side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'dpm', label: 'Deputy Prime Minister (OG)',       side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'dlo', label: 'Deputy Leader of Opposition (OO)', side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'mg',  label: 'Member for Government (CG)',       side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'mo',  label: 'Member for Opposition (CO)',       side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'gw',  label: 'Government Whip (CG)',             side: 'aff', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
      { id: 'ow',  label: 'Opposition Whip (CO)',             side: 'neg', duration: 420, isCX: false, poiStartSec: 60, poiEndSec: 360 },
    ],
  },

  BPHS: {
    id: 'BPHS',
    name: 'British Parliamentary (High School)',
    shortName: 'BP-HS',
    prepPoolSeconds: { aff: 0, neg: 0 },
    // 5-min speeches. POI window: 0:30 to 4:30 (30s protected at start AND end).
    // Explicitly not supported by Debatekeeper per user reviews.
    speeches: [
      { id: 'pm',  label: 'Prime Minister (OG)',              side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'lo',  label: 'Leader of Opposition (OO)',        side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'dpm', label: 'Deputy Prime Minister (OG)',       side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'dlo', label: 'Deputy Leader of Opposition (OO)', side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'mg',  label: 'Member for Government (CG)',       side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'mo',  label: 'Member for Opposition (CO)',       side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'gw',  label: 'Government Whip (CG)',             side: 'aff', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
      { id: 'ow',  label: 'Opposition Whip (CO)',             side: 'neg', duration: 300, isCX: false, poiStartSec: 30, poiEndSec: 270 },
    ],
  },
};

export const FORMAT_LIST = Object.values(FORMATS);

// Helper: fresh state for a format
export function initialStateForFormat(formatId) {
  const fmt = FORMATS[formatId] || FORMATS.LD;
  return {
    format: fmt.id,
    speeches: fmt.speeches.map(s => ({ ...s })),
    currentSpeechIdx: 0,
    speechRunning: false,
    speechStartedAt: null,
    speechPausedElapsedMs: 0,
    prepPoolTotalMs: {
      aff: fmt.prepPoolSeconds.aff * 1000,
      neg: fmt.prepPoolSeconds.neg * 1000,
    },
    prepConsumedMs: { aff: 0, neg: 0 },
    activePrepSide: null,
    prepStartedAt: null,
    vanishAtZero: true,
    flash: false,
    blackout: false,
    judgeName: '',
    lastUpdatedBy: null,
    lastUpdatedAt: Date.now(),
  };
}

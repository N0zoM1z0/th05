// Observed EX-Alice ordinary boss-phase and attack submode values.
#ifndef TH05_MAIN_BOSS_EXALICE_UPDATE_PHASES_HPP
#define TH05_MAIN_BOSS_EXALICE_UPDATE_PHASES_HPP

static const unsigned char EXALICE_PHASE_SETUP = 0;
static const unsigned char EXALICE_PHASE_READY = 1;
static const unsigned char EXALICE_PHASE_WAVE1_REGULAR = 2;
static const unsigned char EXALICE_PHASE_WAVE1_APPROACH = 3;
static const unsigned char EXALICE_PHASE_WAVE1_CHARGE = 4;
static const unsigned char EXALICE_PHASE_WAVE2_APPROACH_FIRST = 5;
static const unsigned char EXALICE_PHASE_WAVE2_REGULAR = 6;
static const unsigned char EXALICE_PHASE_WAVE2_APPROACH_SECOND = 7;
static const unsigned char EXALICE_PHASE_WAVE2_CHARGE = 8;
static const unsigned char EXALICE_PHASE_WAVE3_APPROACH_FIRST = 9;
static const unsigned char EXALICE_PHASE_WAVE3_REGULAR = 10;
static const unsigned char EXALICE_PHASE_WAVE3_APPROACH_SECOND = 11;
static const unsigned char EXALICE_PHASE_WAVE3_CHARGE = 12;
static const unsigned char EXALICE_PHASE_WAVE4_APPROACH_FIRST = 13;
static const unsigned char EXALICE_PHASE_WAVE4_REGULAR = 14;
static const unsigned char EXALICE_PHASE_WAVE4_APPROACH_SECOND = 15;
static const unsigned char EXALICE_PHASE_WAVE4_CHARGE = 16;
static const unsigned char EXALICE_PHASE_FINAL_FAN = 17;

// The per-wave pattern table has four entries, reused across regular and charge phases.
static const unsigned char EXALICE_WAVE_1 = 0;
static const unsigned char EXALICE_WAVE_2 = 1;
static const unsigned char EXALICE_WAVE_3 = 2;
static const unsigned char EXALICE_WAVE_4 = 3;
static const unsigned char EXALICE_MODE_REPOSITION = 0;
static const unsigned char EXALICE_MODE_CHARGE = 1;


// `exalice_phase_next()` copies the previous phase_end_hp into current hp
// before installing the *next* boundary. These thresholds are a sequential
// eight-attack HP ladder, not direct writes to boss.hp at each transition.
static const int EXALICE_HP_INITIAL = 26500;
static const int EXALICE_HP_SETUP_END = 23800;
static const int EXALICE_HP_WAVE1_REGULAR_END = 21000;
static const int EXALICE_HP_WAVE1_CHARGE_END = 18100;
static const int EXALICE_HP_WAVE2_REGULAR_END = 15100;
static const int EXALICE_HP_WAVE2_CHARGE_END = 12600;
static const int EXALICE_HP_WAVE3_REGULAR_END = 9600;
static const int EXALICE_HP_WAVE3_CHARGE_END = 6800;
static const int EXALICE_HP_WAVE4_REGULAR_END = 3400;
static const int EXALICE_HP_LAST_CHARGE_END = 0;

// Original phase deadlines; comparison strictness is meaningful (`>`, `<=`).
static const int EXALICE_SETUP_END_FRAME = 192;
static const int EXALICE_READY_END_FRAME = 64;
static const int EXALICE_RANDOM_FLYSTEP_LEAD_FRAMES = 32;
static const int EXALICE_REGULAR_PATTERN_LIMIT = 32;
static const int EXALICE_REGULAR_PATTERN_ALTERNATION_MASK = 1;
static const int EXALICE_CHARGE_TIMEOUT_FRAME = 4000;
static const int EXALICE_FINAL_CHARGE_PATTERN_LAST = 8;
static const int EXALICE_FINAL_FAN_TIMEOUT_FRAME = 5000;

#endif

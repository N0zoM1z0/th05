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

#endif

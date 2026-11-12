// Original stage-six wing/Devil combat timing, per-playchar damage geometry,
// and four active Devil laser slots. These are compiler constants, not state.
#ifndef TH05_SHINKI_WING_HITBOXES_HPP
#define TH05_SHINKI_WING_HITBOXES_HPP

static const int SHINKI_FIRST_HP_FRAME = 1;
static const int SHINKI_HP_FILL_EXTRA_FRAMES = 64;
static const int SHINKI_PALETTE_BRIGHTEN_TICK = 0;
static const int SHINKI_PALETTE_DARKEN_TICK = 0;
static const int SHINKI_DEFEAT_FLASH_EVEN_FRAME = 0;
static const int SHINKI_DEFEAT_SCORE_BONUS = 65;

// Spell these as float-valued compile-time tokens to preserve the original
// to_sp(float) conversion and its Borland 4.02 codegen path.
#define SHINKI_WING_HITBOX_REIMU_PX (50.0f)
#define SHINKI_WING_HITBOX_MARISA_PX (35.0f)
#define SHINKI_WING_HITBOX_MIMA_PX (45.0f)
#define SHINKI_WING_HITBOX_YUUKA_PX (50.0f)
#define SHINKI_RESET_Y_VELOCITY_PX (0.0f)

// Four laser slots are spawned by the Devil callback; the shared Boss
// update explicitly shuts down all four on the final pattern transition.
enum ShinkiDevilLasers {
    SHINKI_DEVIL_LASER_SLOT_A = 0,
    SHINKI_DEVIL_LASER_SLOT_B = 1,
    SHINKI_DEVIL_LASER_SLOT_C = 2,
    SHINKI_DEVIL_LASER_SLOT_D = 3
};

#endif

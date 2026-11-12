// Complete original Boss defeat choreography and near player-collision geometry.
// Macro constants are compile-time gameplay rules, not new physical state.
#ifndef TH05_GENERIC_BOSS_DEFEAT_COMBAT_RULES_HPP
#define TH05_GENERIC_BOSS_DEFEAT_COMBAT_RULES_HPP

#define GDEF_INITIAL_EXPLOSION_SE 13
#define GDEF_BIG_SHAKE_END_FRAME 12
#define GDEF_SHAKE_NEGATIVE_X_MOD2 0
#define GDEF_SHAKE_NEGATIVE_Y_LAST_MOD4 1
#define GDEF_SHAKE_DISTANCE_PX 4
#define GDEF_SLOWDOWN_FACTOR 2
#define GDEF_BIG_SPRITE_ADVANCE_FRAMES 8
#define GDEF_FINAL_PALETTE_TONE 60
#define GDEF_SONG_FADE_PARAMETER 10
#define GDEF_NEXT_STAGE_WAIT_FRAMES 1

// Original DOS register-lvalue collision passes DY first, then DX.
// Both original boss dimensions are 64 pixels; preserve their separate
// semantic origins instead of rearranging the canonical AX/DX consumers.
#define GDEF_CONTACT_HEIGHT_RADIUS_PX (BOSS_H / 2)
#define GDEF_CONTACT_WIDTH_RADIUS_PX (BOSS_W / 2)

#endif

// Complete Alice callback state and observed foreign interfaces.
#ifndef TH05_MAIN_BOSS_ALICE_UPDATE_HPP
#define TH05_MAIN_BOSS_ALICE_UPDATE_HPP

// Preserve this real main_01 callback context before setup.hpp declares it.
#pragma codeseg BOSS_BG_TEXT main_01
void pascal near alice_bg_render(void);
#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/boss/alice/beam.hpp"
#include "src/main/gather/gather.hpp"

enum explosion_type_t {
    ET_NONE = -1, ET_CIRCLE = 0, ET_NW_SE = 1, ET_SW_NE = 2,
    ET_HORIZONTAL = 3, ET_VERTICAL = 4,
    _explosion_type_t_FORCE_INT16 = 0x7FFF
};

typedef bool (near pascal *near AlicePuppetPattern)(AlicePuppet near &puppet);
typedef void (near *near AlicePattern)(void);
extern AlicePuppetPattern alice_puppet_pattern0;
extern AlicePuppetPattern alice_puppet_pattern1;
extern AlicePattern alice_pattern_current;
// Existing semantic callback table; no entries or asset payload are defined.
extern AlicePattern alice_pattern_table[4][3];
extern SPPoint homing_target;
extern unsigned char bullet_clear_time;
extern nearfunc_t_near bg_render_bombing_func;

// The actual puppet dispatcher pushes a near reference, consumes AL and the
// four real foreign callback entries all return RET2.
bool pascal near alice_puppet_initial(AlicePuppet near &puppet);
bool pascal near alice_puppet_spread(AlicePuppet near &puppet);
bool pascal near alice_puppet_rings(AlicePuppet near &puppet);
bool pascal near alice_puppet_hold(AlicePuppet near &puppet);
void near alice_puppets_entrance(void);
void near alice_puppets_update(void);
void near alice_pattern_opening(void);
bool near boss_hittest_shots(void);
void near boss_hittest_shots_invincible(void);
void pascal near boss_score_bonus(unsigned int units);
void near boss_items_drop(void);
void pascal near boss_explode_small(explosion_type_t type);
void pascal near boss_defeat_update(unsigned int bonus_units);
void pascal near hud_hp_update_and_render(int hp, int total);
void near alice_pattern_final_spread(void);

static const int ALICE_HP_TOTAL = 9600;
static const int ALICE_PUPPET_HP = 500;
static const unsigned char ALICE_PHASE_EXPLODE_SMALL = 253;
static const unsigned char ALICE_PHASE_EXPLODE_BIG = 254;

typedef char alice_puppet_pattern_pointer_is_near[(sizeof(AlicePuppetPattern) == 2) ? 1 : -1];
typedef char alice_pattern_pointer_is_near[(sizeof(AlicePattern) == 2) ? 1 : -1];
typedef char alice_pattern_table_is_24[(sizeof(alice_pattern_table) == 24) ? 1 : -1];

#endif

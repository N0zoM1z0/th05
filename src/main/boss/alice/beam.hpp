// TH05 Alice puppet-beam algorithm: real full storage and foreign interfaces.
#ifndef TH05_MAIN_BOSS_ALICE_BEAM_HPP
#define TH05_MAIN_BOSS_ALICE_BEAM_HPP

#pragma codeseg B4_UPDATE_TEXT main_03
#include "src/main/stage/setup.hpp"
#include "src/main/bullet/template.hpp"
#include "src/main/bullet/cheeto.hpp"

#if GAME != 5 || BINARY != 'M'
#error This owner requires TH05 MAIN
#endif

// Complete original puppet overlay of a26-byte canonical custom-entity slot.
struct AlicePuppet {
    unsigned char flag;
    unsigned char angle;
    PlayfieldMotion pos;
    unsigned int phase_frame;
    union {
        int radius_motion;
        int radius_gather;
    } radius;
    int patnum;
    int hp;
    int damage_this_frame;
    int unused_24;
};
#define alice_puppet0 (reinterpret_cast<AlicePuppet &>(custom_entities[0]))
#define alice_puppet1 (reinterpret_cast<AlicePuppet &>(custom_entities[1]))

extern unsigned int alice_beam_frame;
extern unsigned int alice_beam_burst_window;
extern SPPoint shot_hitbox_center;
extern SPPoint shot_hitbox_radius;
extern BulletTemplate bullet_template;
extern nearfunc_t_near bullet_template_tune;

#pragma codeseg MAIN_01_TEXT main_01
// Real no-argument far-cdecl hitbox consumer; damage is returned in AX.
int far shots_hittest_laser(void);
#pragma codeseg SHARED
extern "C" void pascal far snd_se_play(int sound);
#pragma codeseg B4_UPDATE_TEXT main_03
extern "C" void near bullets_add_regular(void);
void near alice_puppet_beam_pattern(void);

typedef char alice_puppet_is_full_slot[(sizeof(AlicePuppet) == sizeof(custom_t)) ? 1 : -1];
typedef char alice_puppet_is_26[(sizeof(AlicePuppet) == 26) ? 1 : -1];
typedef char alice_puppet_motion_at_2[(offsetof(AlicePuppet, pos) == 2) ? 1 : -1];
typedef char alice_puppet_frame_at_14[(offsetof(AlicePuppet, phase_frame) == 14) ? 1 : -1];
typedef char alice_puppet_radius_at_16[(offsetof(AlicePuppet, radius) == 16) ? 1 : -1];
typedef char alice_puppet_patnum_at_18[(offsetof(AlicePuppet, patnum) == 18) ? 1 : -1];
typedef char alice_puppet_hp_at_20[(offsetof(AlicePuppet, hp) == 20) ? 1 : -1];
typedef char alice_puppet_damage_at_22[(offsetof(AlicePuppet, damage_this_frame) == 22) ? 1 : -1];
typedef char alice_puppet_unused_at_24[(offsetof(AlicePuppet, unused_24) == 24) ? 1 : -1];
typedef char alice_point_storage_is_four[(sizeof(PlayfieldPoint) == sizeof(uint32_t)) ? 1 : -1];

#endif

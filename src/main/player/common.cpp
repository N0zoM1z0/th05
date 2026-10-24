// Natural common shot control from ReC98 th05/p_common.cpp,
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
#pragma option -zCMAIN_01_TEXT -zPmain_01
#include "src/main/player/common.hpp"
#pragma option -a2

char near shot_cycle_init(void)
{
    char cycle = 0;
    switch(shot_time) {
    case 18:
        cycle = SC_6X | SC_3X | SC_2X | SC_1X;
        snd_se_play(1);
        break;
    case 15:
        cycle = SC_6X;
        break;
    case 12:
        cycle = SC_6X | SC_3X;
        snd_se_play(1);
        break;
    case 9:
        cycle = SC_6X | SC_2X;
        break;
    case 6:
        cycle = SC_6X | SC_3X;
        snd_se_play(1);
        break;
    case 3:
        cycle = SC_6X;
        break;
    default:
        return 0;
    }
    shot_ptr = shots;
    shot_last_id = 0;
    return cycle;
}

void pascal near shot_l0(void)
{
    if((shot_cycle_init() & SC_3X) == 0) {
        return;
    }
    Shot near *shot;
    if((shot = shots_add()) != 0) {
        shot->damage = 10;
    }
}

void pascal near shot_l1(void)
{
    if((shot_cycle_init() & SC_3X) == 0) {
        return;
    }
    Shot near *shot;
    if((shot = shots_add()) != 0) {
        shot_velocity_set(&shot->pos.velocity, randring1_next8_ge_lt(-0x44, -0x3C));
        shot->damage = 10;
    }
}

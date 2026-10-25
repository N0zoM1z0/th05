// Natural TH04 stage_state_init algorithm, actual TH05 full typed pools/state.
// The donor's DWORD storage aliases are deliberately not used.
#pragma option -zCSTAGE_STATE_TEXT -zPmain_01
#include "src/main/runtime/stage_state_init.hpp"

extern "C" void near stage_state_init(void)
{
    hitshot_next_free_id = shots_alive_count = 0;
    frames_unused = 0;
    stage_frame = 0;
    stage_frame_mod2 = 0;
    stage_frame_mod4 = 0;
    stage_frame_mod8 = 0;
    stage_frame_mod16 = 0;
    slowdown_factor = 1;
    slowdown_caused_by_bullets = false;
    quit = Q_KEEP_RUNNING;
    palette_changed = false;
    bullet_zap.active = false;
    stage_graze = 0;
    circles_color = 13;

    grc_setclip(32, 16, (32 + 384 - 1), (16 + 368 - 1));
    clear_dwords(hitshots, sizeof(hitshots) / sizeof(unsigned long));
    clear_dwords(lasers, sizeof(lasers) / sizeof(unsigned long));
    clear_dwords(shots, sizeof(shots) / sizeof(unsigned long));
    clear_dwords(enemies, sizeof(enemies) / sizeof(unsigned long));
    clear_dwords(sparks, sizeof(sparks) / sizeof(unsigned long));
    clear_dwords(bullets, sizeof(bullets) / sizeof(unsigned long));
    clear_dwords(custom_entities, sizeof(custom_entities) / sizeof(unsigned long));
    clear_dwords(circles, sizeof(circles) / sizeof(unsigned long));
    clear_dwords(items, sizeof(items) / sizeof(unsigned long));
    clear_dwords(pointnums, sizeof(pointnums) / sizeof(unsigned long));
    clear_dwords(gather_circles, sizeof(gather_circles) / sizeof(unsigned long));

    gather_template.ring_points = 8;
    gather_template.col = 9;
    gather_template.radius.v = 64 * 16;
    gather_template.angle_delta = 2;
    gather_template.velocity.x.v = 0;
    gather_template.velocity.y.v = 0;
}

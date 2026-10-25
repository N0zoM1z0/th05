// Natural TH04 maintained miss-state donor, with original TH05 dream decay,
// performance cap and separate remaining-life/bomb state independently reviewed.
#pragma option -zCPLAYER_MISS_TEXT -zPmain_01
#include "src/main/player/miss.hpp"
#pragma codeseg PLAYER_MISS_TEXT main_01

void near player_miss_update(void)
{
    unsigned char power_loss;

    miss_time--;
    if(miss_time > PLAYER_MISS_ANIMATION_FRAMES) {
        return;
    }
    if(miss_time == PLAYER_MISS_ANIMATION_FRAMES) {
        player_pos.velocity.x.v = 0;
        player_pos.velocity.y.v = 0;
        power_overflow = 0;
        miss_explosion_radius = 0;
        items_miss_add();

        power_loss = (power / 4);
        if(power_loss > 16) {
            power_loss = 16;
        }
        power -= power_loss;
        shot_level_update();
        snd_se_play(2);
        if(playperf > 38) {
            playperf = 38;
        }
        playperf_lower(4);
        resident->miss_count++;
    }

    if(dream > 2) {
        if((boss.phase == PLAYER_MISS_BOSS_HP_FILL) || (stage_frame_mod2 != 0)) {
            dream = dream + static_cast<unsigned char>(-2);
        }
    } else {
        dream = 1;
    }
    hud_dream_put();
    miss_explosion_radius += PLAYER_MISS_RADIUS_STEP;
    miss_explosion_angle = miss_explosion_angle + PLAYER_MISS_ANGLE_STEP;
    if(miss_time >= PLAYER_MISS_FLASH_FRAME_COUNT) {
        return;
    }
    if(lives > 1) {
        if(miss_time & 1) {
            PaletteTone = 150;
        } else {
            PaletteTone = 100;
        }
        palette_changed = true;
    }
    if(miss_time != 0) {
        return;
    }

    player_pos.cur.x.v = (192 * 16);
    player_pos.prev.x.v = (192 * 16);
    player_pos.cur.y.v = (368 * 16);
    player_pos.prev.y.v = (368 * 16);
    player_pos.velocity.x.v = 0;
    player_pos.velocity.y.v = -32;

    if(lives > 1) {
        lives--;
        hud_lives_put();
        bombs = resident->credit_bombs;
        hud_bombs_put();
        bullet_clear_time = 32;
        return;
    }
    quit = static_cast<quit_t>(gameover_run());
}

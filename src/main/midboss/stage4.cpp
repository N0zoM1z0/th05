// Natural TH05 stage-four patterns and callback. The three preceding real
// patterns retain the original compiler contribution's switch-table phase.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/stage4.hpp"
// Preserve the original word-aligned compiler table after all ABI types.
#pragma option -a2

#define patterns_done boss_statebyte[13]
#define pattern boss_statebyte[14]
#define vulnerable boss_statebyte[15]

void near midboss4_pattern_random_clouds(void)
{
    if(midboss.phase_frame == 16) {
        snd_se_play(8);
        bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.spread = 7;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
    }
    if(midboss.phase_frame >= 48 && midboss.phase_frame <= 80 &&
        (midboss.phase_frame % 8) == 0) {
        bullet_template.speed.v = 8;
        for(int i = 0; i < 4; i++) {
            bullet_template.patnum = ((i & 1) ? MIDBOSS4_V_BLUE : 0);
            bullet_template.origin.x.v = randring2_next16_mod(to_sp(48)) +
                midboss.pos.cur.x.v - to_sp(24);
            bullet_template.origin.y.v = randring2_next16_mod(to_sp(48)) +
                midboss.pos.cur.y.v - to_sp(32);
            bullets_add_regular_fixedspeed();
            bullet_template.speed.v += to_sp(1);
        }
        snd_se_play(15);
    }
    if(midboss.phase_frame >= 96) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = 0;
    }
}

void near midboss4_pattern_spiral_rings(void)
{
    if(midboss.phase_frame == 16) {
        snd_se_play(8);
        bullet_template.group = BG_RING;
        bullet_template.spread = 16;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
        bullet_template.patnum = MIDBOSS4_V_RED;
    }
    if(midboss.phase_frame >= 48 && midboss.phase_frame <= 80 &&
        (midboss.phase_frame % 4) == 0) {
        if((midboss.phase_frame % 8) == 0) {
            bullet_template.speed.v = to_sp(3) + 8;
            bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS;
        } else {
            bullet_template.speed.v = to_sp(2) + 8;
            bullet_template.spawn_type = BST_NORMAL;
        }
        bullets_add_regular();
        bullet_template.angle += 4;
        snd_se_play(3);
    }
    if(midboss.phase_frame >= 96) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = 0;
    }
}

void near midboss4_pattern_aimed_stacks(void)
{
    if(midboss.phase_frame == 16) {
        snd_se_play(8);
        bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS | MIDBOSS4_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.angle = 0x20;
        // These are the four adjacent semantic spread/stack fields: three
        // directions, eight angular units, four bullets, four speed units.
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            3UL | (8UL << 8) | (4UL << 16) | (4UL << 24);
        bullet_template.speed.v = to_sp(1);
        bullet_template.patnum = MIDBOSS4_BALL_BLUE;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
    }
    if(midboss.phase_frame >= 48 && midboss.phase_frame <= 80 &&
        (midboss.phase_frame % 4) == 0) {
        bullets_add_regular();
        bullet_template.speed.v += 12;
        bullet_template.angle -= 8;
        snd_se_play(15);
    }
    if(midboss.phase_frame >= 96) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = 0;
    }
}

void pascal far midboss4_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case 0:
        if(midboss.phase_frame == 1) {
            vulnerable = 1;
        }
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(24), to_sp(24), 10);
        if(midboss.phase_frame >= 192) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            pattern = 1;
            patterns_done = 0;
            midboss.pos.velocity.x.v = 0;
        }
        break;

    case 1:
        midboss.pos.prev = midboss.pos.cur;
        switch(pattern) {
        case 0:
            if(midboss4_pattern_transition()) {
                midboss.phase_frame = 0;
                patterns_done++;
                pattern = ((patterns_done % 3) + 1);
                if(patterns_done >= MIDBOSS4_PATTERN_BUDGET) {
                    goto defeat;
                }
            }
            break;
        case 1: midboss4_pattern_random_clouds(); break;
        case 2: midboss4_pattern_spiral_rings(); break;
        case 3: midboss4_pattern_aimed_stacks(); break;
        }
        if(vulnerable) {
            stage4_midboss_hittest_shots(to_sp(24), to_sp(24));
        }
        if(midboss.hp > 0) {
            break;
        }
        bullet_zap.active = true;
        midboss_score_bonus(15);
        items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);
defeat:
        midboss.phase = MIDBOSS4_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS4_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(8), 48);
        snd_se_play(12);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS4_HP_TOTAL);
        return;
    }

    hud_hp_update_and_render(midboss.hp, MIDBOSS4_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}

#undef vulnerable
#undef pattern
#undef patterns_done

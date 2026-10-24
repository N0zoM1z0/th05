// Natural TH05 stage1 midboss algorithm from ReC98 b6ba5b0a m1.cpp.
// Missing geometry/template setters expand to their real canonical fields.
#pragma option -zCMIDBOSS1_TEXT -zPmain_03
#include "src/main/midboss/stage1.hpp"
#pragma codeseg MIDBOSS1_TEXT main_03

void near midboss1_move(void)
{
    midboss.pos.prev.x = midboss.pos.cur.x;
    midboss.pos.prev.y = midboss.pos.cur.y;
    // This original pattern repurposes velocity.x as distance from center.
    midboss.pos.cur.x.v = polar((PLAYFIELD_W * 16) / 2,
        midboss.pos.velocity.x.v, CosTable8[midboss.angle]);
    midboss.pos.cur.y.v = polar(((PLAYFIELD_H * 6) / 23) * 16,
        midboss.pos.velocity.x.v, SinTable8[midboss.angle]);
    midboss.angle -= 0x02;
}

void near midboss1_pattern(void)
{
    int interval = 16;
    if(midboss.hp <= 200) {
        interval = 12;
    }
    if((midboss.phase_frame % interval) == 0) {
        bullet_template.spawn_type = MIDBOSS1_SPAWN_NORMAL;
        bullet_template.patnum = 0;
        bullet_template.speed.v = 2 * 16;
        bullet_template.group = BG_SPREAD;
        bullet_template.special_motion = BSM_EXACT_LINEAR;
        // Canonical set_spread() writes the adjacent count/delta pair.
        reinterpret_cast<uint16_t &>(bullet_template.spread) =
            (4 | (0x02 << 8));
        bullet_template.angle = boss.angle;
        boss.angle += 0x14;
        bullet_template_tune();
        bullets_add_special();

        bullet_template.group = BG_SINGLE;
        bullet_template.spawn_type = MIDBOSS1_SPAWN_CLOUD_FORWARDS;
        bullet_template.speed.v = 24; //1.5 pixels per frame in Q12.4.
        bullet_template.patnum = MIDBOSS1_BLUE_BALL;
        bullet_template_tune();
        bullet_template.angle = randring2_next16();
        bullet_template.origin.x.v = polar(midboss.pos.cur.x.v,
            MIDBOSS1_W, CosTable8[bullet_template.angle]);
        bullet_template.origin.y.v = polar(midboss.pos.cur.y.v,
            MIDBOSS1_H, SinTable8[bullet_template.angle]);
        bullets_add_regular();
    }
}

#pragma option -a2

void pascal far midboss1_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    midboss.phase_frame++;
    switch(midboss.phase) {
    case 0:
        if(midboss.phase_frame >= (MIDBOSS1_HP_FILL_FRAMES + 128)) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.sprite = MIDBOSS1_SPRITE;
        }
        break;
    case 1:
    case 2:
        midboss_hittest_shots_damage(
            MIDBOSS1_W / 2 - MIDBOSS1_W / 8,
            MIDBOSS1_H / 2 - MIDBOSS1_H / 8, 10);
        if(midboss.phase_frame >= 64) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.pos.velocity.x.v = 0;
            boss.angle = -0x20;
        }
        break;
    case 3:
        midboss1_pattern();
        midboss.damage_this_frame = midboss_hittest_shots_damage(
            MIDBOSS1_W - MIDBOSS1_W / 4,
            MIDBOSS1_H - MIDBOSS1_H / 4, 4);
        // Actual TH05 subtracts the truncated damage byte, not the full int.
        midboss.hp -= midboss.damage_this_frame;
        // Preserve signed16 subtraction before unsigned32 multiplication.
        midboss.pos.velocity.x.v =
            ((MIDBOSS1_HP_TOTAL - midboss.hp) * 64UL * 16) / MIDBOSS1_HP_TOTAL;
        midboss1_move();
        if(midboss.phase_frame < 1500) {
            if(midboss.hp > 0) {
                break;
            }
            bullet_zap.active = true;
            midboss_score_bonus(5);
            items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BIGPOWER);
        }
        midboss.phase = MIDBOSS1_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS1_KILL_PATTERN;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y,
            MIDBOSS1_W / 4, 48);
        snd_se_play(12);
        break;
    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS1_HP_TOTAL);
        return;
    }
    hud_hp_update_and_render(midboss.hp, MIDBOSS1_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}

// Complete puppet entrance followed by the movement/pattern dispatcher.
#pragma option -zCALICE_PMV_TEXT -zPmain_03
#include "src/main/boss/alice/puppet_motion.hpp"

void near alice_puppets_entrance(void)
{
    alice_puppet0.pos.cur.x.v = polar(to_sp(96),
        alice_puppet0.radius.radius_motion, CosTable8[alice_puppet0.angle]);
    alice_puppet0.pos.cur.y.v = polar(to_sp(96),
        alice_puppet0.radius.radius_motion, SinTable8[alice_puppet0.angle]);
    alice_puppet0.angle -= 2;
    alice_puppet0.radius.radius_motion -= to_sp(2);
    alice_puppet1.pos.cur.x.v = polar(to_sp(288),
        alice_puppet1.radius.radius_motion, CosTable8[alice_puppet1.angle]);
    alice_puppet1.pos.cur.y.v = polar(to_sp(96),
        alice_puppet1.radius.radius_motion, SinTable8[alice_puppet1.angle]);
    alice_puppet1.angle += 2;
    alice_puppet1.radius.radius_motion -= to_sp(2);
    alice_puppet0.pos.prev = alice_puppet0.pos.cur;
    alice_puppet1.pos.prev = alice_puppet1.pos.cur;
}

void near alice_puppets_update(void)
{
    int i;
    int value;
    AlicePuppet near *p;
    shot_hitbox_radius.x.v = to_sp(20);
    shot_hitbox_radius.y.v = to_sp(20);
    p = &alice_puppet0;
    for(i = 0; i < 2; i++, p++) {
        if(p->flag == 0) {
            continue;
        }
        if(p->flag == 1) {
            if(reinterpret_cast<uint32_t &>(p->pos.cur) !=
                reinterpret_cast<uint32_t &>(p->pos.prev)) {
                value = p->pos.prev.x.v - p->pos.cur.x.v;
                if((value / to_sp(2)) != 0) {
                    p->pos.cur.x.v += value / to_sp(2);
                } else if((value / 4) != 0) {
                    p->pos.cur.x.v += value / 4;
                } else {
                    p->pos.cur.x = p->pos.prev.x;
                }
                value = p->pos.prev.y.v - p->pos.cur.y.v;
                if((value / to_sp(2)) != 0) {
                    p->pos.cur.y.v += value / to_sp(2);
                } else if((value / 4) != 0) {
                    p->pos.cur.y.v += value / 4;
                } else {
                    p->pos.cur.y = p->pos.prev.y;
                }
                p->patnum = 192;
            } else {
                p->patnum = 190;
                if(i == 0) {
                    value = alice_puppet_pattern0(*p);
                } else {
                    value = alice_puppet_pattern1(*p);
                }
                if(value) {
                    p->pos.prev.x.v = randring2_next16_mod(to_sp(320)) + to_sp(32);
                    p->pos.prev.y.v = randring2_next16_mod(to_sp(160)) + to_sp(16);
                    if(i == 0) {
                        alice_puppet_pattern0 = alice_puppet_pattern_table[
                            randring2_next16_and(3)];
                    } else {
                        alice_puppet_pattern1 = alice_puppet_pattern_table[
                            randring2_next16_and(3)];
                    }
                    p->phase_frame = 0;
                } else {
                    p->phase_frame++;
                }
            }
            if(static_cast<unsigned int>(p->pos.cur.x.v - player_pos.cur.x.v + to_sp(12)) < to_sp(24) &&
                static_cast<unsigned int>(p->pos.cur.y.v - player_pos.cur.y.v + to_sp(12)) < to_sp(24)) {
                player_is_hit = true;
            }
            if(boss_statebyte[9] != 3) {
                shot_hitbox_center = p->pos.cur;
                p->damage_this_frame = shots_hittest();
                if(p->damage_this_frame != 0) {
                    snd_se_play(4);
                }
                p->hp -= p->damage_this_frame;
                if(p->hp < 0) {
                    p->flag++;
                    p->patnum = 4;
                    p->damage_this_frame = 0;
                    snd_se_play(12);
                    score_delta += 100;
                }
            } else {
                p->damage_this_frame = 0;
            }
        } else {
            if((p->flag % 4) == 0) {
                p->patnum++;
                if(p->patnum >= 12) {
                    p->flag = 0;
                    p->pos.cur.x.v = to_sp(192);
                    p->pos.cur.y.v = to_sp(-256);
                    p->pos.prev.x.v = to_sp(192);
                    p->pos.prev.y.v = to_sp(-16);
                    p->hp = 500;
                    p->patnum = 192;
                    if(i == 0) {
                        alice_puppet_pattern0 = alice_puppet_recover;
                    } else {
                        alice_puppet_pattern1 = alice_puppet_recover;
                    }
                    boss.hp -= 300;
                }
            }
            p->flag++;
        }
    }
}

// Full shot damage, bomb contribution and laser-reflected bullet collisions.
#pragma option -zCSHOT_HIT_TEXT -zPmain_01
#include "src/main/player/shot_runtime.hpp"

extern BulletTemplate bullet_template;

int far shots_hittest(void)
{
    int i;
    subpixel_t left = shot_hitbox_center.x.v - shot_hitbox_radius.x.v;
    subpixel_t top = shot_hitbox_center.y.v - shot_hitbox_radius.y.v;
    unsigned int width = shot_hitbox_radius.x.v * 2;
    unsigned int height = shot_hitbox_radius.y.v * 2;
    unsigned int damage = 0;
    unsigned char hits = 0;
    shot_alive_t near *alive = shots_alive;
    for(i = 0; i < shots_alive_count; i++, alive++) {
        if(static_cast<unsigned int>(alive->pos.x.v - left) <= width &&
           static_cast<unsigned int>(alive->pos.y.v - top) <= height) {
            hits++;
            damage += (static_cast<unsigned char>(alive->shot->damage) / hits)
                ? (static_cast<unsigned char>(alive->shot->damage) / hits) : 1;
            shot_hit_spark_cycle++;
            if(shot_hit_spark_cycle & 1) {
                sparks_add_random(alive->pos.x, alive->pos.y, 8 * 16, 1);
            }
            hitshot_from(alive->shot);
            alive->pos.x.v = SHOT_SUBPIXEL_NONE;
        }
    }
    if(bombing) {
        if(shots_hittest_against_boss) {
            damage = damage / 4;
        }
        if(stage_frame_mod4 == 0) {
            damage += select_for_playchar(3, 4, 15, 3);
        }
        if(playchar == SHOT_PLAYCHAR_MARISA &&
           bomb_frame >= 16 && bomb_frame < 80 && bomb_frame % 4 == 0 &&
           static_cast<unsigned int>(player_pos.cur.x.v - left) <= width &&
           static_cast<unsigned int>(player_pos.cur.y.v) >= static_cast<unsigned int>(top)) {
            damage += 22;
        }
    }
    if(shots_hittest_against_boss) {
        if(playchar <= SHOT_PLAYCHAR_REIMU || playchar >= SHOT_PLAYCHAR_YUUKA) {
            if(stage_id == 6) {
                damage *= 5;
                damage = damage / 4;
            } else if(playchar == SHOT_PLAYCHAR_REIMU) {
                damage *= 8;
                damage /= 7;
            }
        } else {
            damage *= 4;
            damage /= 5;
        }
    } else {
        if(stage_id == 6 && playchar == SHOT_PLAYCHAR_REIMU) {
            damage *= 4;
            damage /= 5;
        }
        if(playchar == SHOT_PLAYCHAR_YUUKA) {
            damage *= 4;
            damage /= 5;
        }
    }
    score_delta += damage;
    return damage;
}

int far shots_hittest_laser(void)
{
    int i;
    subpixel_t left = shot_hitbox_center.x.v - shot_hitbox_radius.x.v;
    subpixel_t top = shot_hitbox_center.y.v - shot_hitbox_radius.y.v;
    unsigned int width = shot_hitbox_radius.x.v * 2;
    unsigned int height = shot_hitbox_radius.y.v * 2;
    unsigned int damage = 0;
    unsigned char hits = 0;
    shot_alive_t near *alive = shots_alive;
    for(i = 0; i < shots_alive_count; i++, alive++) {
        if(static_cast<unsigned int>(alive->pos.x.v - left) <= width &&
           static_cast<unsigned int>(alive->pos.y.v - top) <= height) {
            hits++;
            damage += (static_cast<unsigned char>(alive->shot->damage) / hits)
                ? (static_cast<unsigned char>(alive->shot->damage) / hits) : 1;
            shot_hit_spark_cycle++;
            if(shot_hit_spark_cycle & 1) {
                sparks_add_random(alive->pos.x, alive->pos.y, 8 * 16, 1);
            }
            if(rank != 0 || stage_frame_mod4 == 0) {
                static_cast<SPPoint &>(bullet_template.origin) = alive->pos;
                bullet_template.angle = randring1_next16();
                bullets_add_regular_far();
            }
            hitshot_from(alive->shot);
            alive->pos.x.v = SHOT_SUBPIXEL_NONE;
        }
    }
    score_delta += damage;
    return damage;
}

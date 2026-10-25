// Natural TH05 enemy lifecycle, adapted from maintained TH04 algorithms.
// Original behavior independently reviewed against the pinned TH05 artifact.
#pragma option -zCENEMY_SPAWN_TEXT -zPmain_03
#include "src/main/enemy/lifecycle.hpp"
#pragma codeseg ENEMY_SPAWN_TEXT main_03

#include "src/main/enemy/spawn.inl"

#pragma samecodeseg midboss_activate_if_stage_frame_is_midboss_start_frame
void pascal far std_run(void)
{
    unsigned char spawn_count;
    midboss_activate_if_stage_frame_is_midboss_start_frame();
    if(*reinterpret_cast<unsigned int far *>(std_ip) != stage_frame) {
        return;
    }
    std_ip_offset += sizeof(unsigned int);
    spawn_count = *reinterpret_cast<unsigned char far *>(std_ip);
    std_ip_offset++;
    do {
        if(midboss_active == false) {
            enemies_add();
        }
        std_ip_offset += sizeof(StdEnemySpawnRecord);
        spawn_count--;
    } while(spawn_count > 0);
    if(*reinterpret_cast<unsigned int far *>(std_ip) == 0) {
        stage_vm = nullfunc_far;
    }
}

// The original 24-byte REP MOVSW template-copy function remains foreign.
#pragma codeseg ENEMY_UPDATE_TEXT main_03
#pragma samecodeseg sparks_add_random
extern "C" void pascal far enemies_update(void)
{
    unsigned char value;
    unsigned char dream_recharge;
    register enemy_t near *enemy;
    register int i;

    homing_target.x.v = ENEMY_HOMING_NONE;
    homing_target.y.v = ENEMY_HOMING_NONE;
    shot_hitbox_radius.x.v = TO_SP(16);
    shot_hitbox_radius.y.v = TO_SP(12);
    dream_recharge = 0; // First counts eligible enemies; becomes interval below.
    enemy = enemies;
    i = 0;

    for(; i < ENEMY_COUNT; (i++, enemy++)) {
        if(enemy->flag == EF_FREE) {
            goto next_enemy;
        }
        if(enemy->flag == EF_KILLED) {
            enemy->flag = EF_FREE;
            goto next_enemy;
        }

        enemy_cur = enemy;
        if(enemy->flag >= EF_KILL_ANIM) {
            goto kill_animation;
        }

        enemy_script_update();

        if(enemy->kills_player_on_collision == false) {
            goto collision_done;
        }
        if(static_cast<unsigned int>(
            enemy->pos.cur.x.v - player_pos.cur.x.v + TO_SP(12)
        ) >= TO_SP(24)) {
            goto collision_done;
        }
        if(static_cast<unsigned int>(
            enemy->pos.cur.y.v - player_pos.cur.y.v + TO_SP(12)
        ) >= TO_SP(24)) {
            goto collision_done;
        }
        player_is_hit = true;
        goto kill_enemy;

    collision_done:
        if(enemy->can_be_damaged == false) {
            goto autofire;
        }
        if(enemy->hp == -1) {
            goto autofire;
        }
        if(static_cast<unsigned int>(enemy->pos.cur.x.v + TO_SP(16)) >=
            TO_SP(PLAYFIELD_RIGHT)) {
            goto autofire;
        }
        if(static_cast<unsigned int>(enemy->pos.cur.y.v + TO_SP(16)) >=
            TO_SP(PLAYFIELD_BOTTOM)) {
            goto autofire;
        }

        dream_recharge++;
        if(enemy->pos.cur.y.v > homing_target.y.v) {
            homing_target.x.v = enemy->pos.cur.x.v;
            homing_target.y.v = enemy->pos.cur.y.v;
        }

        shot_hitbox_center = enemy->pos.cur;
        value = static_cast<unsigned char>(shots_hittest());
        if(value != 0) {
            if(enemy->hp != -2) {
                if(value < enemy->hp) {
                    enemy->hp -= value;
                } else {
                kill_enemy:
                    enemy->flag = EF_KILL_ANIM;
                    enemy->anim_cels = 1;
                    enemy->can_be_damaged = false;
                    enemy->kills_player_on_collision = false;
                    enemy->pos.velocity.x.v = 0;
                    enemy->pos.velocity.y.v = 0;
                    if(enemy->item != IT_NONE) {
                        items_add(enemy->pos.cur.x.v, enemy->pos.cur.y.v, enemy->item);
                    }
                    snd_se_play(3);
                    score_delta += static_cast<unsigned long>(
                        static_cast<unsigned int>(enemy->score)
                    );
                    sparks_add_random(enemy->pos.cur.x, enemy->pos.cur.y, TO_SP(4), 7);
                    enemies_gone++;
                    enemies_killed++;
                    goto next_enemy;

                }
                enemy->damaged_this_frame = true;
            } else {
                snd_se_play(10);
            }
        }
        goto autofire;

    autofire:
        if(enemy->autofire == false) {
            goto no_autofire;
        }
        enemy->autofire_cur_frame++;
        if(enemy->autofire_cur_frame < enemy->autofire_interval) {
            goto no_autofire;
        }
        if(enemy->pos.cur.y.v >= TO_SP(304)) {
            goto no_autofire;
        }
        if(static_cast<unsigned int>(
            enemy->pos.cur.x.v - player_pos.cur.x.v + TO_SP(48)
        ) >= TO_SP(96)) {
            goto fire;
        }
        if(static_cast<unsigned int>(
            enemy->pos.cur.y.v - player_pos.cur.y.v + TO_SP(48)
        ) < TO_SP(96)) {
            goto no_autofire;
        }

    fire:
        enemy->autofire_cur_frame = 0;
        enemy_bullet_template_push(enemy->bullet_template);
        bullet_template.origin.x.v += enemy->pos.cur.x.v;
        bullet_template.origin.y.v += enemy->pos.cur.y.v;
        bullet_template_tune();
        bullets_add_regular();

    no_autofire:
        enemy->age++;
        goto next_enemy;

    kill_animation:
        enemy->pos.update_seg3();
        value = ++enemy->flag;
        value = static_cast<unsigned char>(
            ((value - EF_KILL_ANIM) / 4) + PAT_ENEMY_KILL
        );
        enemy->patnum_base = value;
        if(value < (PAT_ENEMY_KILL + ENEMY_KILL_CELS)) {
            goto next_enemy;
        }
        enemy->flag = EF_KILLED;

    next_enemy:
        ;
    }

    // TH05's homing/dream feedback uses the byte count as a recharge interval.
    // Keep its real byte subtraction and wrap behavior before the lower clamp.
    if(homing_target.x.v != ENEMY_HOMING_NONE) {
        if(dream_recharge >= 8) {
            dream_recharge = 80;
        } else {
            dream_recharge = (144 - (dream_recharge << 3));
        }
        dream_recharge -= (stage_id << 4);
        if((dream_recharge > 144) || (dream_recharge < 4)) {
            dream_recharge = 4;
        }
        if(((stage_frame % dream_recharge) == 0) && (dream < 128)) {
            dream++;
            hud_dream_put();
        }
    }
}

// Natural TH05 stage-two midboss state machine, recovered from the original
// callback at 1527:0B7B. Foreign movement/pattern bodies remain separate owners.
#include "src/main/midboss/stage2.hpp"
#include "src/main/midboss/stage2_scratch.hpp"

// Exact phase, reward and defeat timing for the three-stage controller.
static const int MIDBOSS2_ENTRANCE_END_FRAME = 256;
static const int MIDBOSS2_ORBIT_TIMEOUT_FRAMES = 1000;
static const int MIDBOSS2_ORBIT_HP_THRESHOLD = 400;
static const int MIDBOSS2_ORBIT_SCORE_BONUS = 5;
static const int MIDBOSS2_BULLET_CLEAR_MIN = 20;
static const int MIDBOSS2_HIT_RADIUS_PX = 24;
static const int MIDBOSS2_INVINCIBLE_HIT_SOUND = 10;
static const int MIDBOSS2_ORBIT_SPARK_RADIUS_PX = 4;
static const int MIDBOSS2_ORBIT_SPARK_COUNT = 32;
static const int MIDBOSS2_ORBIT_TRANSITION_SOUND = 15;
static const int MIDBOSS2_ORBIT_TARGET_X_PX = 192;
static const int MIDBOSS2_ORBIT_TARGET_Y_PX = 64;
static const int MIDBOSS2_FINAL_TIMEOUT_FRAMES = 800;
static const int MIDBOSS2_FINAL_SCORE_BONUS = 15;
static const int MIDBOSS2_FINAL_SPARK_RADIUS_PX = 8;
static const int MIDBOSS2_FINAL_SPARK_COUNT = 48;
static const int MIDBOSS2_FINAL_TRANSITION_SOUND = 12;

void pascal far midboss2_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case MIDBOSS2_PHASE_ENTRANCE:
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(MIDBOSS2_HIT_RADIUS_PX), to_sp(MIDBOSS2_HIT_RADIUS_PX), MIDBOSS2_INVINCIBLE_HIT_SOUND);
        if(midboss.phase_frame >= MIDBOSS2_ENTRANCE_END_FRAME) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            midboss2_scratch.orbit_contracting = MIDBOSS2_ORBIT_EXPANDING;
            midboss2_scratch.orbit_center_drift = MIDBOSS2_ORBIT_DRIFT_INITIAL;
            midboss.pos.velocity.x.v = 0;
            midboss2_orbit_center.x.v = to_sp(192);
            midboss2_orbit_center.y = midboss.pos.cur.y;
        }
        break;

    case MIDBOSS2_PHASE_ORBIT_ATTACK:
        midboss2_pattern();
        midboss2_move();
        stage2_midboss_hittest_shots(to_sp(24), to_sp(24));
        if(midboss.phase_frame < MIDBOSS2_ORBIT_TIMEOUT_FRAMES) {
            if(midboss.hp > MIDBOSS2_ORBIT_HP_THRESHOLD) {
                break;
            }
            midboss_score_bonus(MIDBOSS2_ORBIT_SCORE_BONUS);
            if(bullet_clear_time < MIDBOSS2_BULLET_CLEAR_MIN) {
                bullet_clear_time = MIDBOSS2_BULLET_CLEAR_MIN;
            }
        }
        midboss.phase++;
        midboss.sprite = MIDBOSS2_SPRITE_DAMAGED;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS2_ORBIT_SPARK_RADIUS_PX), MIDBOSS2_ORBIT_SPARK_COUNT);
        snd_se_play(MIDBOSS2_ORBIT_TRANSITION_SOUND);
        vector2_between_plus(midboss.pos.cur.x.v, midboss.pos.cur.y.v,
            to_sp(MIDBOSS2_ORBIT_TARGET_X_PX), to_sp(MIDBOSS2_ORBIT_TARGET_Y_PX), 0,
            midboss.pos.velocity.x.v, midboss.pos.velocity.y.v, 1);
        break;

    case MIDBOSS2_PHASE_FINAL_ATTACK:
        midboss2_pattern_final();
        midboss.pos.update_seg3();
        stage2_midboss_hittest_shots(to_sp(24), to_sp(24));
        if(midboss.phase_frame < MIDBOSS2_FINAL_TIMEOUT_FRAMES) {
            if(midboss.hp > 0) {
                break;
            }
            bullet_zap.active = true;
            midboss_score_bonus(MIDBOSS2_FINAL_SCORE_BONUS);
            items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);
        }
        midboss.phase = MIDBOSS2_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS2_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS2_FINAL_SPARK_RADIUS_PX), MIDBOSS2_FINAL_SPARK_COUNT);
        snd_se_play(MIDBOSS2_FINAL_TRANSITION_SOUND);
        break;

    default:
        midboss_defeat_update();
        hud_hp_update_and_render(midboss.hp, MIDBOSS2_HP_TOTAL);
        return;
    }

    hud_hp_update_and_render(midboss.hp, MIDBOSS2_HP_TOTAL);
    homing_target.x = midboss.pos.cur.x;
    homing_target.y = midboss.pos.cur.y;
}

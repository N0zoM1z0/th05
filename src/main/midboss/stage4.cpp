// Natural TH05 stage-four patterns and callback. The three preceding real
// patterns retain the original compiler contribution's switch-table phase.
#pragma option -zCB4_UPDATE_TEXT -zPmain_03
#include "src/main/midboss/stage4.hpp"
#include "src/main/midboss/stage4_scratch.hpp"
// Preserve the original word-aligned compiler table after all ABI types.
#pragma option -a2

// Real two-phase dispatcher and four per-pattern submodes, with original
// numeric values preserved in the compiler-generated switch table.
static const unsigned char MIDBOSS4_PHASE_ENTRANCE = 0;
static const unsigned char MIDBOSS4_PHASE_PATTERNS = 1;
static const unsigned char MIDBOSS4_PATTERN_TRANSITION = 0;
static const unsigned char MIDBOSS4_PATTERN_RANDOM_CLOUDS = 1;
static const unsigned char MIDBOSS4_PATTERN_SPIRAL_RINGS = 2;
static const unsigned char MIDBOSS4_PATTERN_AIMED_STACKS = 3;

// Each of the three native patterns uses a 16-frame telegraph followed by
// a bounded 48..80-frame volley and a 96-frame return to repositioning.
// Preserve the existing phase-frame signs and original integer modulo width.
static const int MIDBOSS4_PATTERN_CHARGE_FRAME = 16;
static const int MIDBOSS4_PATTERN_VOLLEY_FIRST = 48;
static const int MIDBOSS4_PATTERN_VOLLEY_LAST = 80;
static const int MIDBOSS4_PATTERN_FINISH_FRAME = 96;
static const int MIDBOSS4_RING_VOLLEY_CADENCE = 4;
static const int MIDBOSS4_CLOUD_VOLLEY_CADENCE = 8;
static const int MIDBOSS4_SPIRAL_ALTERNATE_CADENCE = 8;
static const int MIDBOSS4_ENTRANCE_FIRST_FRAME = 1;
static const int MIDBOSS4_ENTRANCE_END_FRAME = 192;
static const int MIDBOSS4_PATTERN_VARIANT_MODULUS = 3;
static const int MIDBOSS4_HIT_RADIUS_PIXELS = 24;
static const int MIDBOSS4_HIT_EFFECT = 10;
static const int MIDBOSS4_DEFEAT_SPARK_COUNT = 48;
static const int MIDBOSS4_DEFEAT_SCORE_UNITS = 15;

// Exact projectile setup values for the three real Stage 4 attack leaves.
static const int MIDBOSS4_CHARGE_SOUND = 8;
static const int MIDBOSS4_CLOUD_SPREAD_COUNT = 7;
static const int MIDBOSS4_CLOUD_BULLET_COUNT = 4;
static const int MIDBOSS4_CLOUD_INITIAL_SPEED_SP = 8;
static const int MIDBOSS4_CLOUD_SPEED_STEP_PX = 1;
static const int MIDBOSS4_CLOUD_ORIGIN_RANGE_PX = 48;
static const int MIDBOSS4_CLOUD_ORIGIN_X_OFFSET_PX = 24;
static const int MIDBOSS4_CLOUD_ORIGIN_Y_OFFSET_PX = 32;
static const int MIDBOSS4_CLOUD_VOLLEY_SOUND = 15;
static const int MIDBOSS4_RING_BULLET_COUNT = 16;
static const int MIDBOSS4_SPIRAL_FAST_SPEED_PX = 3;
static const int MIDBOSS4_SPIRAL_SLOW_SPEED_PX = 2;
static const int MIDBOSS4_SPIRAL_BASE_SPEED_SP = 8;
static const int MIDBOSS4_SPIRAL_ANGLE_STEP = 4;
static const int MIDBOSS4_SPIRAL_VOLLEY_SOUND = 3;
static const int MIDBOSS4_STACK_INITIAL_ANGLE = 0x20;
static const int MIDBOSS4_STACK_BASE_SPEED_PX = 1;
static const int MIDBOSS4_STACK_SPEED_STEP_SP = 12;
static const int MIDBOSS4_STACK_ANGLE_STEP = 8;
static const int MIDBOSS4_STACK_VOLLEY_SOUND = 15;
static const int MIDBOSS4_DEFEAT_SPARK_RADIUS_PX = 8;
static const int MIDBOSS4_DEFEAT_SOUND = 12;
#define patterns_done midboss4_scratch.completed_patterns
#define pattern midboss4_scratch.current_pattern
#define vulnerable midboss4_scratch.shot_vulnerable

void near midboss4_pattern_random_clouds(void)
{
    if(midboss.phase_frame == MIDBOSS4_PATTERN_CHARGE_FRAME) {
        snd_se_play(MIDBOSS4_CHARGE_SOUND);
        bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS;
        bullet_template.group = BG_RANDOM_ANGLE_AND_SPEED;
        bullet_template.spread = MIDBOSS4_CLOUD_SPREAD_COUNT;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_VOLLEY_FIRST && midboss.phase_frame <= MIDBOSS4_PATTERN_VOLLEY_LAST &&
        (midboss.phase_frame % MIDBOSS4_CLOUD_VOLLEY_CADENCE) == 0) {
        bullet_template.speed.v = MIDBOSS4_CLOUD_INITIAL_SPEED_SP;
        for(int i = 0; i < MIDBOSS4_CLOUD_BULLET_COUNT; i++) {
            bullet_template.patnum = ((i & 1) ? MIDBOSS4_V_BLUE : 0);
            bullet_template.origin.x.v = randring2_next16_mod(to_sp(MIDBOSS4_CLOUD_ORIGIN_RANGE_PX)) +
                midboss.pos.cur.x.v - to_sp(MIDBOSS4_CLOUD_ORIGIN_X_OFFSET_PX);
            bullet_template.origin.y.v = randring2_next16_mod(to_sp(MIDBOSS4_CLOUD_ORIGIN_RANGE_PX)) +
                midboss.pos.cur.y.v - to_sp(MIDBOSS4_CLOUD_ORIGIN_Y_OFFSET_PX);
            bullets_add_regular_fixedspeed();
            bullet_template.speed.v += to_sp(MIDBOSS4_CLOUD_SPEED_STEP_PX);
        }
        snd_se_play(MIDBOSS4_CLOUD_VOLLEY_SOUND);
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_FINISH_FRAME) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = MIDBOSS4_PATTERN_TRANSITION;
    }
}

void near midboss4_pattern_spiral_rings(void)
{
    if(midboss.phase_frame == MIDBOSS4_PATTERN_CHARGE_FRAME) {
        snd_se_play(MIDBOSS4_CHARGE_SOUND);
        bullet_template.group = BG_RING;
        bullet_template.spread = MIDBOSS4_RING_BULLET_COUNT;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
        bullet_template.patnum = MIDBOSS4_V_RED;
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_VOLLEY_FIRST && midboss.phase_frame <= MIDBOSS4_PATTERN_VOLLEY_LAST &&
        (midboss.phase_frame % MIDBOSS4_RING_VOLLEY_CADENCE) == 0) {
        if((midboss.phase_frame % MIDBOSS4_SPIRAL_ALTERNATE_CADENCE) == 0) {
            bullet_template.speed.v = to_sp(MIDBOSS4_SPIRAL_FAST_SPEED_PX) + MIDBOSS4_SPIRAL_BASE_SPEED_SP;
            bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS;
        } else {
            bullet_template.speed.v = to_sp(MIDBOSS4_SPIRAL_SLOW_SPEED_PX) + MIDBOSS4_SPIRAL_BASE_SPEED_SP;
            bullet_template.spawn_type = BST_NORMAL;
        }
        bullets_add_regular();
        bullet_template.angle += MIDBOSS4_SPIRAL_ANGLE_STEP;
        snd_se_play(MIDBOSS4_SPIRAL_VOLLEY_SOUND);
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_FINISH_FRAME) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = MIDBOSS4_PATTERN_TRANSITION;
    }
}

void near midboss4_pattern_aimed_stacks(void)
{
    if(midboss.phase_frame == MIDBOSS4_PATTERN_CHARGE_FRAME) {
        snd_se_play(MIDBOSS4_CHARGE_SOUND);
        bullet_template.spawn_type = MIDBOSS4_CLOUD_FORWARDS | MIDBOSS4_NO_DECELERATE;
        bullet_template.group = BG_SPREAD_STACK_AIMED;
        bullet_template.angle = MIDBOSS4_STACK_INITIAL_ANGLE;
        // These are the four adjacent semantic spread/stack fields: three
        // directions, eight angular units, four bullets, four speed units.
        reinterpret_cast<uint32_t &>(bullet_template.spread) =
            3UL | (8UL << 8) | (4UL << 16) | (4UL << 24);
        bullet_template.speed.v = to_sp(MIDBOSS4_STACK_BASE_SPEED_PX);
        bullet_template.patnum = MIDBOSS4_BALL_BLUE;
        bullet_template_tune();
        midboss.sprite = MIDBOSS4_SPRITE_CAST;
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_VOLLEY_FIRST && midboss.phase_frame <= MIDBOSS4_PATTERN_VOLLEY_LAST &&
        (midboss.phase_frame % MIDBOSS4_RING_VOLLEY_CADENCE) == 0) {
        bullets_add_regular();
        bullet_template.speed.v += MIDBOSS4_STACK_SPEED_STEP_SP;
        bullet_template.angle -= MIDBOSS4_STACK_ANGLE_STEP;
        snd_se_play(MIDBOSS4_CLOUD_VOLLEY_SOUND);
    }
    if(midboss.phase_frame >= MIDBOSS4_PATTERN_FINISH_FRAME) {
        midboss.sprite = MIDBOSS4_SPRITE_STILL;
        midboss.phase_frame = 0;
        pattern = MIDBOSS4_PATTERN_TRANSITION;
    }
}

void pascal far midboss4_update(void)
{
    bullet_template.origin = midboss.pos.cur;
    gather_template.center = midboss.pos.cur;
    midboss.phase_frame++;

    switch(midboss.phase) {
    case MIDBOSS4_PHASE_ENTRANCE:
        if(midboss.phase_frame == MIDBOSS4_ENTRANCE_FIRST_FRAME) {
            vulnerable = 1;
        }
        midboss.pos.update_seg3();
        midboss_hittest_shots_damage(to_sp(MIDBOSS4_HIT_RADIUS_PIXELS), to_sp(MIDBOSS4_HIT_RADIUS_PIXELS), MIDBOSS4_HIT_EFFECT);
        if(midboss.phase_frame >= MIDBOSS4_ENTRANCE_END_FRAME) {
            midboss.phase++;
            midboss.phase_frame = 0;
            midboss.angle = 0;
            pattern = MIDBOSS4_PATTERN_RANDOM_CLOUDS;
            patterns_done = 0;
            midboss.pos.velocity.x.v = 0;
        }
        break;

    case MIDBOSS4_PHASE_PATTERNS:
        midboss.pos.prev = midboss.pos.cur;
        switch(pattern) {
        case MIDBOSS4_PATTERN_TRANSITION:
            if(midboss4_pattern_transition()) {
                midboss.phase_frame = 0;
                patterns_done++;
                pattern = ((patterns_done % MIDBOSS4_PATTERN_VARIANT_MODULUS) + MIDBOSS4_PATTERN_RANDOM_CLOUDS);
                if(patterns_done >= MIDBOSS4_PATTERN_BUDGET) {
                    goto defeat;
                }
            }
            break;
        case MIDBOSS4_PATTERN_RANDOM_CLOUDS: midboss4_pattern_random_clouds(); break;
        case MIDBOSS4_PATTERN_SPIRAL_RINGS: midboss4_pattern_spiral_rings(); break;
        case MIDBOSS4_PATTERN_AIMED_STACKS: midboss4_pattern_aimed_stacks(); break;
        }
        if(vulnerable) {
            stage4_midboss_hittest_shots(to_sp(MIDBOSS4_HIT_RADIUS_PIXELS), to_sp(MIDBOSS4_HIT_RADIUS_PIXELS));
        }
        if(midboss.hp > 0) {
            break;
        }
        bullet_zap.active = true;
        midboss_score_bonus(MIDBOSS4_DEFEAT_SCORE_UNITS);
        items_add(midboss.pos.cur.x.v, midboss.pos.cur.y.v, IT_BOMB);
defeat:
        midboss.phase = MIDBOSS4_PHASE_EXPLODE_BIG;
        midboss.sprite = MIDBOSS4_SPRITE_EXPLODE;
        midboss.phase_frame = 0;
        sparks_add_circle(midboss.pos.cur.x, midboss.pos.cur.y, to_sp(MIDBOSS4_DEFEAT_SPARK_RADIUS_PX), MIDBOSS4_DEFEAT_SPARK_COUNT);
        snd_se_play(MIDBOSS4_DEFEAT_SOUND);
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

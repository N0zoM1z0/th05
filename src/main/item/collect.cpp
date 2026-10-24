// Natural item collection/miss algorithms adapted from maintained TH04 source.
// TH05 dream, point scoring, globals and counters independently reconstructed.
#pragma option -zCITEM_REWARD_TEXT -zPmain_03
#include "src/main/item/update.hpp"
#pragma codeseg ITEM_REWARD_TEXT main_03

void pascal near item_collect(item_t near *item)
{
    int point_relative_y;
    bool use_yellow_point_number;
    register item_t near *collected_item = item;
    register unsigned int base_points;
    use_yellow_point_number = false;

    switch(collected_item->type) {
    case IT_POWER:
        if(power < ITEM_POWER_MAX) {
            if(power == (ITEM_POWER_MAX - 1)) {
                ITEM_SHOW_POPUP(POPUP_ID_FULL_POWERUP);
                ITEM_CLEAR_BULLETS();
            }
            power++;
            shot_level_update();
            base_points = 1;
            break;
        }
        power_overflow++;
        if(static_cast<unsigned int>(power_overflow) >= ITEM_POWER_OVERFLOW_MAX) {
            power_overflow = ITEM_POWER_OVERFLOW_MAX;
            use_yellow_point_number = true;
            if((items_pull_to_player == false) && (dream < 128)) {
                dream++;
            }
        }
        base_points = POWER_OVERFLOW_BONUS[power_overflow];
        hud_dream_put();
        break;

    case IT_POINT:
        if(dream < 128) {
            point_relative_y = collected_item->pos.cur.y.v - (dream * 24) - 896;
            base_points = 5120;
        } else {
            point_relative_y = 0;
            base_points = item_point_score_at_full_dream;
        }
        if(point_relative_y <= 0) {
            item_playperf_raise++;
            if(items_pull_to_player == false) {
                // Preserve the real byte addition before its upper clamp.
                dream = static_cast<unsigned char>(dream +
                    (6 - collected_item->pos.cur.y.v / TO_SP(64)));
                if(dream > 128) {
                    dream = 128;
                }
                hud_dream_put();
            }
            total_max_valued_point_items_collected++;
            use_yellow_point_number = true;
        } else {
            base_points = 2800 - (point_relative_y / 2);
        }
        item_playperf_raise++;
        extend_point_items_collected++;
        total_point_items_collected++;
        // This actual executable has an unconditional byte increment, not
        // the saturating word-counter path in the reference listing.
        stage_point_items_collected++;
        item_extend_check();
        hud_point_items_put();
        break;

    case IT_DREAM:
        if(dream >= 128) {
            base_points = 12800;
            use_yellow_point_number = true;
        } else {
            base_points = 1;
            dream = 128;
        }
        hud_dream_put();
        item_playperf_raise += 2;
        if(items_pull_to_player) {
            item_playperf_raise += 2;
        }
        break;

    case IT_BIGPOWER:
        if(power < ITEM_POWER_MAX) {
            power += 10;
            if(power >= ITEM_POWER_MAX) {
                power = ITEM_POWER_MAX;
                ITEM_SHOW_POPUP(POPUP_ID_FULL_POWERUP);
                ITEM_CLEAR_BULLETS();
            }
            shot_level_update();
            base_points = 1;
            break;
        }
        power_overflow += 5;
        // Historical order: the table read precedes the clamp. Above-cap
        // values are immediately replaced with the fixed2560 reward below.
        base_points = POWER_OVERFLOW_BONUS[power_overflow];
        if(static_cast<unsigned int>(power_overflow) > ITEM_POWER_OVERFLOW_MAX) {
            power_overflow = ITEM_POWER_OVERFLOW_MAX;
        }
        if(power_overflow == ITEM_POWER_OVERFLOW_MAX) {
            base_points = 2560;
            use_yellow_point_number = true;
        }
        break;

    case IT_BOMB:
        bombs++;
        base_points = 100;
        hud_bombs_put();
        break;

    case IT_1UP:
        playperf_raise(3);
        lives++;
        hud_lives_put();
        snd_se_play(7);
        ITEM_SHOW_POPUP(POPUP_ID_EXTEND);
        base_points = 100;
        break;

    case IT_FULLPOWER:
        ITEM_CLEAR_BULLETS();
        ITEM_SHOW_POPUP(POPUP_ID_FULL_POWERUP);
        power = ITEM_POWER_MAX;
        shot_level_update();
        base_points = 100;
        break;
    }

    // TH05 adds the base reward directly; the display latch does not double
    // score_delta here. The explicit unsigned-long conversion zero-extends it.
    score_delta += static_cast<unsigned long>(base_points);
    if(use_yellow_point_number == false) {
        pointnums_add_white(collected_item->pos.cur.x.v,
            collected_item->pos.cur.y.v, base_points);
    } else {
        pointnums_add_yellow(collected_item->pos.cur.x.v,
            collected_item->pos.cur.y.v, base_points);
    }
    if(item_playperf_raise >= 32) {
        item_playperf_raise -= 32;
        playperf_raise(1);
    }
    items_collected++;
}

void pascal near item_miss_penalty(item_t near *item)
{
    register item_t near *missed_item = item;
    switch(missed_item->type) {
    case IT_POINT:
        if((dream > 1) && (dream < 128)) {
            dream--;
        }
        break;
    case IT_BOMB:
        playperf_lower(2);
        break;
    case IT_1UP:
        playperf_lower(4);
        break;
    }
    hud_dream_put();
}

// Item spawning: single items, and the five items dropped when losing a life.
// Part of the item family translation unit (family.cpp).
#ifndef TH05_ITEM_FAMILY_CONTEXT
#pragma option -zCITEM_SPAWN_TEXT -zPmain_03
#endif
#include "src/main/item/spawn.hpp"
#ifndef TH05_ITEM_FAMILY_CONTEXT
#pragma codeseg ITEM_SPAWN_TEXT main_03
#endif

void pascal near items_add(subpixel_t x, subpixel_t y, item_type_t type)
{
    register item_t near *item;
    register int i;

    // While a bomb pulls items to the player, power, point and dream items
    // and automatic drops all become power items. The unsigned byte
    // comparison leaves IT_NONE (0xFE) alone.
    if(items_pull_to_player &&
        ((static_cast<unsigned char>(type) < IT_BIGPOWER) ||
         (type == IT_ENEMY_DROP_NEXT))) {
        type = IT_POWER;
    }

    if(type == IT_ENEMY_DROP_NEXT) {
        // Scripted enemies can request the next automatic drop instead of a
        // concrete item. Only every second request creates an item. The byte
        // counter and modulo make the 64-entry table repeat after 128 requests.
        item_drop_cycle++;
        if((item_drop_cycle & 1) != 0) {
            return;
        }
        type = static_cast<item_type_t>(ENEMY_DROPS[(item_drop_cycle / 2) % 64]);
    }

    item = items;
    i = 0;
    for(; i < ITEM_COUNT; (i++, item++)) {
        if(item->flag != F_FREE) {
            continue;
        }
        item->flag = F_ALIVE;
        item->unknown = 0;
        item->pos.cur.x.v = x;
        item->pos.cur.y.v = y;
        item->pos.velocity.x.v = 0;
        item->pos.velocity.y.v = -TO_SP(3);
        item->type = type;
        item->patnum = ITEM_PATNUM[static_cast<unsigned char>(type)];
        item_splashes_add(reinterpret_cast<Subpixel &>(x), reinterpret_cast<Subpixel &>(y));
        item->pulled_to_player = false;
        items_spawned++;
        return;
    }
}

extern "C" void pascal far items_miss_add(void)
{
    int pool_index;
    int miss_velocity_field;
    int big_power_slot;
    int type;
    int discarded_distinct_slot;
    register item_t near *item;
    register int spawned_count;

    big_power_slot = randring2_next16_mod(ITEM_MISS_COUNT);
    // ZUN bloat: a second slot, different from the first, is picked and never
    // used. It still advances the random ring.
    do {
        discarded_distinct_slot = randring2_next16_mod(ITEM_MISS_COUNT);
    } while(discarded_distinct_slot == big_power_slot);

    if(player_pos.cur.x.v < TO_SP(PLAYFIELD_W / 3)) {
        miss_velocity_field = MISS_FIELD_LEFT;
    } else if(player_pos.cur.x.v <= TO_SP((PLAYFIELD_W / 3) * 2)) {
        miss_velocity_field = MISS_FIELD_CENTER;
    } else {
        miss_velocity_field = MISS_FIELD_RIGHT;
    }

    // Spawn up to five items into free slots; if the pool is full, fewer
    // items drop. Every item except the big power one draws another random
    // number, even if it is replaced by a full power item on the last life.
    spawned_count = 0;
    item = items;
    pool_index = 0;
    while(pool_index < ITEM_COUNT) {
        if(item->flag == F_FREE) {
            item->flag = F_ALIVE;
            item->unknown = 0;
            item->pos.cur.x.v = player_pos.cur.x.v;
            item->pos.cur.y.v = player_pos.cur.y.v;
            item->pos.velocity.y = ITEM_MISS_VELOCITIES[miss_velocity_field][0][spawned_count];
            item->pos.velocity.x = ITEM_MISS_VELOCITIES[miss_velocity_field][1][spawned_count];
            item->pulled_to_player = false;
            if(big_power_slot != spawned_count) {
                type = randring2_next16_and(IT_POINT);
            } else {
                type = IT_BIGPOWER;
            }
            if(lives == 1) {
                type = IT_FULLPOWER;
            }
            item->type = static_cast<unsigned char>(type);
            item->patnum = ITEM_PATNUM[type];
            spawned_count++;
            items_spawned++;
            if(spawned_count >= ITEM_MISS_COUNT) {
                return;
            }
        }
        pool_index++;
        item++;
    }
}


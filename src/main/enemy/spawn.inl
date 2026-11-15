// Spawns the enemy described by the STD record at std_ip into the first free
// slot. Does nothing if all slots are in use.
extern "C" void pascal near enemies_add(void)
{
    int i;
    subpixel_t center_y;
    register subpixel_t center_x = current_spawn.center_x;
    center_y = current_spawn.center_y;
    register enemy_t near *enemy = enemies;

    for(i = 0; i < ENEMY_COUNT; i++, enemy++) {
        if(enemy->flag != EF_FREE) {
            continue;
        }
        enemy->flag = EF_ALIVE_FIRST_FRAME;
        enemy->age = 0;
        enemy->cur_instr_frame = 0;
        enemy->loop_i = 0;
        enemy->script_ip = 0;
        enemy->script = reinterpret_cast<unsigned char near *>(
            std_enemy_scripts[current_spawn.script]);

        // 999 means a random position.
        if(center_x == TO_SP(999)) {
            center_x = randring2_next16_mod(TO_SP(PLAYFIELD_W));
        }
        enemy->pos.cur.x.v = center_x;
        enemy->spawned_in_left_half = ((center_x < TO_SP(PLAYFIELD_W / 2))
            ? static_cast<unsigned char>(1) : static_cast<unsigned char>(0));
        if(center_y == TO_SP(999)) {
            center_y = randring2_next16_mod(TO_SP(PLAYFIELD_H));
        }
        enemy->pos.cur.y.v = center_y;
        enemy->item = static_cast<item_type_t>(current_spawn.item);
        enemy->subtype = current_spawn.subtype;
        enemy->damaged_this_frame = false;
        enemy->autofire = (rank == RANK_LUNATIC);
        enemy->clip = 0;
        enemy->anim_cels = 1;
        enemy->anim_frames_per_cel = 4;
        enemy->anim_cur_cel = 0;
        enemy->can_be_damaged = false;
        enemy->kills_player_on_collision = false;
        enemy->autofire_cur_frame = randring2_next16();   // truncated to 8 bits
        enemy->autofire_interval = 128;
        enemy->bullet_template.group = BG_FORCESINGLE_AIMED;
        enemy->bullet_template.spawn_type = BST_NORMAL;
        enemy->bullet_template.speed.v = (TO_SP(2) + 10);   // 2.625 pixels
        enemy->bullet_template.origin.x.v = 0;
        enemy->bullet_template.origin.y.v = 0;
        enemy->bullet_template.patnum = 0;
        return;
    }
}


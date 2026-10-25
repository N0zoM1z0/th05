void near bomb_reset(void)
{
    bombing = false;
    bg_render_bombing = nullfunc_near;
}

extern "C" void pascal near player_bomb(void)
{
    if(bombing || !bombs || bombing_disabled) {
        return;
    }
    if(miss_time != 0) {
        if(miss_time <= BOMB_RUNTIME_MISS_FRAMES) {
            return;
        }
        miss_time = 0;
        player_is_hit = false;
        player_respawn_motion_time = 0;
    }
    bombs--;
    hud_bombs_put();
    bombing = true;
    bomb_frame = 0;
    player_invincibility_time = select_for_playchar(192, 160, 144, 224);
    bullet_clear_time = select_for_playchar(192, 128, 96, 192);
    bg_render_bombing = bg_render_bombing_func;
    snd_se_play(13);
    items_pull_to_player = true;
    resident->bombs_used++;
    playperf_lower(1);
}

extern "C" void pascal near bb_playchar_put(int cel)
{
    // TH05 preserves the existing tile-mask color; only GAME4 sets it here.
    tiles_bb_seg = bb_playchar_seg;
    tiles_bb_put_raw(cel);
}

void near bomb_dream_decay(void)
{
    if((bomb_frame % 2) != 0) {
        return;
    }
    if((boss.phase != BOMB_RUNTIME_BOSS_HP_FILL) && ((bomb_frame % 4) == 0)) {
        return;
    }
    if(dream > 1) {
        dream--;
    }
    hud_dream_put();
}

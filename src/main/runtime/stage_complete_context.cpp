// Four true original-order MAIN functions; the 803-byte initializer is the new source owner.
#pragma option -zCDEMO_TEXT
// Declare the real empty compiler segments before the original SHARED externs.
#pragma codeseg RUNTIME_MAIN01_TEXT main_01
#pragma codeseg SESSION_MAIN01_TEXT main_01
#pragma codeseg SESSION_INIT_TEXT main_01
#pragma codeseg STAGE_SESSION_TEXT main_01
#pragma codeseg SHARED
#pragma codeseg RUNTIME_MAIN03_TEXT main_03
#pragma codeseg BULLET_A_TEXT main_03
#pragma codeseg STAGE_SESSION_MAIN03_CONTEXT main_03
#pragma codeseg DEMO_TEXT main_01
void main(void);
void near gameplay_loop(void);
void near gameplay_session_init(void);
void near stage_session_init(void);
#define TH05_RUNTIME_COMBINED 1
#include "src/main/runtime/entry.cpp"
#include "src/main/runtime/gameplay_loop.cpp"
#undef TH05_RUNTIME_COMBINED

// Natural new-game initialization adapted from maintained TH04 core source.
// TH05's four-character and rank/demo behavior follows the actual target.

#include "src/main/runtime/gameplay_session_init.hpp"
#pragma codeseg DEMO_TEXT main_01

void near gameplay_session_init(void)
{
    resident->graze = 0;
    resident->miss_count = 0;
    resident->bombs_used = 0;
    resident->end_sequence = 0x37; // ES_INGAME
    playchar = resident->playchar;
    bombs = resident->credit_bombs;
    lives = resident->credit_lives;
    for(int i = 0; i < SCORE_DIGITS; i++) {
        score.digits[i] = 0;
    }
    power = 1;
    dream = 1;
    bb_txt_load();

    switch(playchar) {
    case SESSION_REIMU:
        playchar_speed_aligned = 56;
        playchar_speed_diagonal = 40;
        playchar_bomb_func = bomb_reimu;
        break;
    case SESSION_MARISA:
        playchar_speed_aligned = 64;
        playchar_speed_diagonal = 48;
        playchar_bomb_func = bomb_marisa;
        break;
    case SESSION_MIMA:
        playchar_speed_aligned = 72;
        playchar_speed_diagonal = 52;
        playchar_bomb_func = bomb_mima;
        break;
    case SESSION_YUUKA:
        playchar_speed_aligned = 56;
        playchar_speed_diagonal = 40;
        playchar_bomb_func = bomb_yuuka;
        break;
    }
    playchar_shot_funcs = SHOT_FUNCS[playchar];

    if(resident->demo_num != 0) {
        if(resident->demo_num < 5) {
            playperf = 40;
            rank = SESSION_LUNATIC;
        } else {
            playperf = 32;
            rank = SESSION_EXTRA;
        }
        turbo_mode = true;
    } else {
        playperf = 32;
        if(stage_id == 6) {
            rank = SESSION_EXTRA;
            turbo_mode = true;
        } else {
            rank = resident->rank;
            turbo_mode = resident->turbo_mode;
        }
    }

    score_reset();
    hiscore_load();
    switch(rank) {
    case SESSION_EASY:
        item_point_score_at_full_dream = 6000;
        graze_score = 25;
        playperf_min = 16;
        playperf_max = 32;
        bullet_template_tune = bullet_template_tune_easy;
        break;
    case SESSION_NORMAL:
        item_point_score_at_full_dream = 10000;
        graze_score = 50;
        playperf_min = 24;
        playperf_max = 40;
        bullet_template_tune = bullet_template_tune_normal;
        break;
    case SESSION_HARD:
        item_point_score_at_full_dream = 15000;
        playperf = 44;
        graze_score = 100;
        playperf_min = 44;
        playperf_max = 54;
        bullet_template_tune = bullet_template_tune_hard;
        break;
    case SESSION_LUNATIC:
        item_point_score_at_full_dream = 20000;
        graze_score = 200;
        playperf = 48;
        playperf_min = 48;
        playperf_max = 58;
        bullet_template_tune = bullet_template_tune_lunatic;
        break;
    case SESSION_EXTRA:
        item_point_score_at_full_dream = 40000u;
        graze_score = 500;
        playperf_min = 32;
        playperf_max = 36;
        bullet_template_tune = bullet_template_tune_normal;
        break;
    }
}

// Natural stage entry adapted from maintained TH04 session_init.cpp,
// with TH05's actual debug/demo, four-character and resource behavior.

#include "src/main/runtime/stage_session_context.hpp"
#pragma codeseg DEMO_TEXT main_01
// Keep all canonical object types complete before compiler table alignment.
#pragma option -a2

// Real PC-98 graphics-page hardware boundary, as in the maintained master API.
#define graph_accesspage(page) outportb(0xA6, (page))
#define graph_showpage(page) outportb(0xA4, (page))

void near stage_session_init(void)
{
    int i;
    load_playchar_resources = 0;
    vsync_Count2 = 0;
    stage_id = resident->stage;
    if(stage_id == 0 || stage_id == 6) {
        load_playchar_resources = 1;
        text_fillca(' ', 0x05); // Black reversed TRAM cells.
        input_sense_hook = reinterpret_cast<StageInputCallback>(nullfunc_near);
        gameplay_session_init();
        if(resident->debug) {
            resident->stage = resident->debug_stage;
            stage_id = resident->stage;
            power = resident->debug_power;
            resident->debug = false;
            debug_frame_step_enabled = true;
        }
        if(resident->demo_num != 0) {
            demo_load();
            stage_id = (resident->stage = resident->demo_stage);
            if(resident->demo_num != 5) {
                power = 128;
            }
            input_sense_hook = DemoPlay;
            random_seed = 318;
        }
    }
    clear_blue_vram_pages();
    graph_accesspage(0);
    graph_showpage(0);
    palette_entry_rgb(SESSION_EYE_RGB);
    palette_show();
    PaletteTone = 0;
    palette_show();
    clear_blue_vram_pages();
    overlay_wipe();
    stage_runtime_init();
    hud_put();
    eyecatch_animate();
    midboss_reset();

    if(load_playchar_resources != 0) {
        bb_cheeto_load();
        bomb_bg_load__ems_preload_playchar_cdgs();
        bb_playchar_load();
        switch(playchar) {
        case 0: super_entry_bfnt(SESSION_REIMU_BFT); break;
        case 1: super_entry_bfnt(SESSION_MARI_BFT); break;
        case 2: super_entry_bfnt(SESSION_MIMA_BFT); break;
        case 3: super_entry_bfnt(SESSION_YUKA_BFT); break;
        }
        super_entry_bfnt(SESSION_MIKOD_BFT);
        super_entry_bfnt(SESSION_MIKO32_BFT);
        switch(playchar) {
        case 0: super_entry_bfnt(SESSION_REIMU16_BFT); break;
        case 1: super_entry_bfnt(SESSION_MARI16_BFT); break;
        case 2: super_entry_bfnt(SESSION_MIMA16_BFT); break;
        case 3: super_entry_bfnt(SESSION_YUKA16_BFT); break;
        }
        super_entry_bfnt(SESSION_MIKO16_BFT);
        for(i = 12; i < 172; i++) {
            super_convert_tiny(i);
        }
        if(playchar == 3) {
            super_entry_bfnt(SESSION_BOMB_YUUKA_BFT);
        } else {
            super_entry_bfnt(SESSION_BOMB_BFT);
        }
    }
    tiles_activate();
    pellet_bottom_col = 9;
    switch(stage_id) {
    case 0:
        ems_preload_boss_faceset(SESSION_BSS0_CD2);
        super_entry_bfnt(SESSION_ST00_BFT);
        stage1_setup();
        mpn_load(SESSION_ST00_MPN);
        break;
    case 1:
        ems_preload_boss_faceset(SESSION_BSS1_CD2);
        super_entry_bfnt(SESSION_ST01_BFT);
        stage2_setup();
        mpn_load(SESSION_ST01_MPN);
        break;
    case 2:
        ems_preload_boss_faceset(SESSION_BSS2_CD2);
        super_entry_bfnt(SESSION_ST02_BFT);
        stage3_setup();
        mpn_load(SESSION_ST02_MPN);
        break;
    case 3:
        ems_preload_boss_faceset(SESSION_BSS3_CD2);
        super_entry_bfnt(SESSION_ST03_BFT);
        stage4_setup();
        mpn_load(SESSION_ST03_MPN);
        break;
    case 4:
        ems_preload_boss_faceset(SESSION_BSS4_CD2);
        super_entry_bfnt(SESSION_ST04_BFT);
        stage5_setup();
        mpn_load(SESSION_ST04_MPN);
        break;
    case 5:
        ems_preload_boss_faceset(SESSION_BSS4_CD2_REPEAT);
        super_entry_bfnt(SESSION_ST04_BFT_REPEAT);
        stage6_setup();
        bg_render_not_bombing = shinki_bg_render;
        bg_render_bombing_func = shinki_bg_render;
        break;
    case 6:
        shot_level_update();
        ems_preload_boss_faceset(SESSION_BSS6_CD2);
        super_entry_bfnt(SESSION_ST06_BFT);
        stagex_setup();
        mpn_load(SESSION_ST06_MPN);
        break;
    }
    map_load();
    std_load();
    dialog_load();
    tiles_fill_initial();
    graph_accesspage(0);
    while(vsync_Count2 < 128) {
    }
    palette_black_out(1);
    PaletteTone = 100;
    palette_show();
    overlay_black();
    tiles_render_all();
    page_back = 1;
    page_front = 0;
    graph_accesspage(1);
    graph_showpage(0);
    tiles_render_all();
    if(resident->demo_num == 0 || resident->demo_num == 5) {
        stage_bgm_name[2] = '0';
        stage_bgm_name[3] = '0' + stage_id;
        snd_load(stage_bgm_name, SND_LOAD_SONG);
        snd_kaja_interrupt(0); // KAJA_SONG_PLAY
    }
    overlay1 = overlay_stage_enter_update_and_render;
    overlay2 = nullfunc_near;
}

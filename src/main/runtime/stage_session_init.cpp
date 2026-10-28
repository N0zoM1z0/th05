// Natural stage entry adapted from maintained TH04 session_init.cpp,
// with TH05's actual debug/demo, four-character and resource behavior.
#pragma option -zCSTAGE_SESSION_TEXT -zPmain_01
#include "src/main/runtime/stage_session_init.hpp"
#pragma codeseg STAGE_SESSION_TEXT main_01
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

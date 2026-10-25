// Natural C++ candidate: pinned ReC98 b6ba5b0a th05/res_kso.cpp.
// The real producer is tiny model; its explicit 286 option precedes all tokens.
#pragma option -2
#include "src/zun/resident/config.hpp"

char near cfg_init(resident_t __seg *resident_seg)
{
    const char *fn = ZUN_CFG_FILENAME;
    cfg_options_t opts = OPTS_DEFAULT;
    cfg_t cfg_in;
    resident_t far *resident = resident_seg;

    if(!file_ropen(fn)) {
recreate:
        if(!file_create(fn)) {
            return 1;
        }
        file_write(&opts, sizeof(opts));
        resident->rank = ZUN_CFG_SHOW_SETUP_MENU;
        resident->cfg_lives = ZUN_CFG_LIVES_DEFAULT;
        resident->cfg_bombs = ZUN_CFG_BOMBS_DEFAULT;
        resident->bgm_mode = ZUN_CFG_BGM_FM26;
        resident->se_mode = ZUN_CFG_SE_FM;
        resident->turbo_mode = true;
    } else {
        file_read(&cfg_in, sizeof(cfg_in));
        file_close();
        if((cfg_in.opts.rank + cfg_in.opts.lives + cfg_in.opts.bombs +
            cfg_in.opts.bgm_mode + cfg_in.opts.se_mode + cfg_in.opts.turbo_mode)
            != cfg_in.opts_sum) {
            goto recreate;
        }
        resident->rank = cfg_in.opts.rank;
        resident->cfg_lives = cfg_in.opts.lives;
        resident->cfg_bombs = cfg_in.opts.bombs;
        resident->bgm_mode = cfg_in.opts.bgm_mode;
        resident->se_mode = cfg_in.opts.se_mode;
        resident->turbo_mode = cfg_in.opts.turbo_mode;
        if(resident->cfg_lives > ZUN_CFG_LIVES_MAX || resident->cfg_lives == 0) {
            goto recreate;
        }
        if(resident->cfg_bombs > ZUN_CFG_BOMBS_MAX) {
            goto recreate;
        }
        if(resident->bgm_mode >= ZUN_CFG_BGM_MODE_COUNT) {
            goto recreate;
        }
        if(resident->se_mode >= ZUN_CFG_SE_MODE_COUNT) {
            goto recreate;
        }
        if(!file_append(fn)) {
            return 1;
        }
        file_seek(offsetof(cfg_t, resident), 0);
    }
    if(!file_write(&resident_seg, sizeof(resident_seg))) {
        return 1;
    }
    file_write(&debug, sizeof(debug));
    // Original defect: cfg_in.opts_sum is uninitialized for a missing file.
    // Recreating an invalid existing file also retains its original checksum.
    file_write(&cfg_in.opts_sum, sizeof(cfg_in.opts_sum));
    file_close();
    return 0;
}

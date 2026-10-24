// TH05's real 10-byte configuration file structure and master.lib I/O ABI.
// Natural-source provenance: ReC98@b6ba5b0a529edbb31efdf8c0e939263804f8ee47,
// th02/formats/cfg.hpp, th03/formats/cfg_impl.hpp, th04/formats/cfg.hpp.
#ifndef TH05_OP_CONFIG_HPP
#define TH05_OP_CONFIG_HPP

#include "src/op/main/menu.hpp"

#if GAME != 5 || BINARY != 'O'
#error This owner is the TH05 OP configuration implementation
#endif

typedef int int16_t;
#define CFG_FN "MIKO.CFG"
#define SEEK_SET 0

struct cfg_options_t {
    int8_t rank;
    int8_t lives;
    int8_t bombs;
    int8_t bgm_mode;
    int8_t se_mode;
    int8_t turbo_mode;

    int8_t sum(void) const {
        return (rank + lives + bombs + bgm_mode + se_mode + turbo_mode);
    }
};

struct cfg_t {
    cfg_options_t opts;
    resident_t __seg *resident;
    int8_t debug;
    int8_t opts_sum;
};

extern "C" {
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buf, unsigned int wsize);
    int pascal far file_append(const char far *filename);
    int pascal far file_write(const void far *buf, unsigned int wsize);
    void pascal far file_seek(long pos, int dir);
    void pascal far file_close(void);
}

// The ordinary master.lib implementation is the one called by OP cfg_load.
// The unused RES_KSO-specific register/DOS implementation is not part of this
// owner. The near segment handle is converted to the canonical far pointer.
static inline resident_t __seg* cfg_load_and_set_resident(
    cfg_t& cfg, const char* fn
) {
    file_ropen(fn);
    file_read(&cfg, sizeof(cfg));
    file_close();

    resident_t __seg *resident_seg = cfg.resident;
    resident = resident_seg;
    return resident_seg;
}

typedef char th05_cfg_options_are_6[(sizeof(cfg_options_t) == 6) ? 1 : -1];
typedef char th05_cfg_rank_at_0[(offsetof(cfg_options_t, rank) == 0) ? 1 : -1];
typedef char th05_cfg_lives_at_1[(offsetof(cfg_options_t, lives) == 1) ? 1 : -1];
typedef char th05_cfg_bombs_at_2[(offsetof(cfg_options_t, bombs) == 2) ? 1 : -1];
typedef char th05_cfg_bgm_at_3[(offsetof(cfg_options_t, bgm_mode) == 3) ? 1 : -1];
typedef char th05_cfg_se_at_4[(offsetof(cfg_options_t, se_mode) == 4) ? 1 : -1];
typedef char th05_cfg_turbo_at_5[(offsetof(cfg_options_t, turbo_mode) == 5) ? 1 : -1];
typedef char th05_cfg_segment_handle_is_2[
    (sizeof(resident_t __seg*) == 2) ? 1 : -1];
typedef char th05_cfg_file_is_10[(sizeof(cfg_t) == 10) ? 1 : -1];
typedef char th05_cfg_options_at_0[(offsetof(cfg_t, opts) == 0) ? 1 : -1];
typedef char th05_cfg_resident_at_6[(offsetof(cfg_t, resident) == 6) ? 1 : -1];
typedef char th05_cfg_debug_at_8[(offsetof(cfg_t, debug) == 8) ? 1 : -1];
typedef char th05_cfg_checksum_at_9[(offsetof(cfg_t, opts_sum) == 9) ? 1 : -1];

#endif

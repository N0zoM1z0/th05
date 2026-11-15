// Layout of the 10-byte MIKO.CFG file and the master.lib file functions used
// to read and write it. Based on ReC98 th02/formats/cfg.hpp,
// th03/formats/cfg_impl.hpp and th04/formats/cfg.hpp.
#ifndef TH05_OP_CONFIG_HPP
#define TH05_OP_CONFIG_HPP

#include "src/op/main/menu.hpp"

#if GAME != 5 || BINARY != 'O'
#error This header is for TH05 OP.EXE only
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
    // Segment of the resident structure. RES_KSO.COM stores it here so that
    // every game binary can find the structure.
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

// Reads the whole file and points [resident] at the segment stored in it.
// (ReC98's cfg_impl.hpp also has a raw DOS version of this, which is only used
// by RES_KSO.COM.)
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
typedef char th05_cfg_file_is_10[(sizeof(cfg_t) == 10) ? 1 : -1];

#endif

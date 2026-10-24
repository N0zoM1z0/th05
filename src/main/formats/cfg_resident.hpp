// Candidate local ABI, adapted from nmlgc/ReC98@b6ba5b0a529edbb3:
// th04/formats/cfg.hpp, th02/formats/cfg.hpp and th03/formats/cfg_impl.hpp.
#ifndef TH05_MAIN_FORMATS_CFG_RESIDENT_HPP
#define TH05_MAIN_FORMATS_CFG_RESIDENT_HPP

#include "src/shared/abi.hpp"

// This producer loads a segment reference, without accessing resident fields.
// Keep the referenced type opaque until a resident-field owner needs it.
struct resident_t;

struct cfg_options_t {
    char rank;
    char lives;
    char bombs;
    char bgm_mode;
    char se_mode;
    char turbo_mode;

    char sum(void) const {
        return (rank + lives + bombs + bgm_mode + se_mode + turbo_mode);
    }
};

struct cfg_t {
    cfg_options_t opts;
    resident_t __seg *resident;
    char debug;
    char opts_sum;
};

extern resident_t far *resident;
extern cfg_t cfg;
extern const char CFG_FN[];

resident_t __seg *near cfg_load_resident_ptr(void);

typedef char th05_cfg_options_is_6[(sizeof(cfg_options_t) == 6) ? 1 : -1];
typedef char th05_cfg_is_10[(sizeof(cfg_t) == 10) ? 1 : -1];
typedef char th05_cfg_resident_at_6[(offsetof(cfg_t, resident) == 6) ? 1 : -1];
typedef char th05_cfg_debug_at_8[(offsetof(cfg_t, debug) == 8) ? 1 : -1];
typedef char th05_cfg_checksum_at_9[(offsetof(cfg_t, opts_sum) == 9) ? 1 : -1];
typedef char th05_cfg_segment_pointer_is_2[(sizeof(resident_t __seg *) == 2) ? 1 : -1];
typedef char th05_cfg_far_pointer_is_4[(sizeof(resident_t far *) == 4) ? 1 : -1];

#endif

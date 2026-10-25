// Full shared resident/configuration types; original tiny-model file interfaces.
#ifndef TH05_ZUN_RESIDENT_CONFIG_HPP
#define TH05_ZUN_RESIDENT_CONFIG_HPP
#include "src/main/hud/resident.hpp"
#include "src/main/formats/cfg_resident.hpp"

enum ZunConfigLimits {
    ZUN_CFG_LIVES_DEFAULT = 3,
    ZUN_CFG_LIVES_MAX = 6,
    ZUN_CFG_BOMBS_DEFAULT = 3,
    ZUN_CFG_BOMBS_MAX = 3,
    ZUN_CFG_BGM_FM26 = 1,
    ZUN_CFG_BGM_MODE_COUNT = 3,
    ZUN_CFG_SE_FM = 1,
    ZUN_CFG_SE_MODE_COUNT = 3,
    ZUN_CFG_SHOW_SETUP_MENU = 0xFF
};
extern char debug;
extern const cfg_options_t OPTS_DEFAULT;
extern const char ZUN_CFG_FILENAME[];

extern "C" {
    int pascal near file_ropen(const char near *filename);
    int pascal near file_create(const char near *filename);
    int pascal near file_append(const char near *filename);
    int pascal near file_read(void far *buffer, unsigned count);
    int pascal near file_write(const void far *buffer, unsigned count);
    void pascal near file_seek(long offset, int origin);
    void pascal near file_close(void);
}
char near cfg_init(resident_t __seg *resident_seg);
#endif

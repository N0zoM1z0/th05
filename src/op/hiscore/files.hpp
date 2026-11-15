// File and song names used by the High Score viewer. They are grouped into
// one structure because regist_view_menu() is compiled in two translation
// units (view.cpp and menu.cpp), and both must reference the same strings.
#ifndef TH05_HISCORE_FILES_HPP
#define TH05_HISCORE_FILES_HPP
#include "src/shared/abi.hpp"

struct hiscore_filenames_t {
    char score_file[11];
    char hiscore_bgm[5];
    char hiscore_background[8];
    char menu_background[7];
    char menu_bgm[3];
    char number_font[10];
    char rank_font[9];
};
extern const hiscore_filenames_t near hi_filenames;

#endif

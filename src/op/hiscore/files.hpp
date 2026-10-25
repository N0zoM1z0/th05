// One complete semantic filename pool, shared by the real high-score owners.
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

typedef char hiscore_files_are_53[(sizeof(hiscore_filenames_t) == 53) ? 1 : -1];
typedef char hiscore_name_at_11[(offsetof(hiscore_filenames_t, hiscore_bgm) == 11) ? 1 : -1];
typedef char hiscore_background_at_16[(offsetof(hiscore_filenames_t, hiscore_background) == 16) ? 1 : -1];
typedef char hiscore_menu_at_24[(offsetof(hiscore_filenames_t, menu_background) == 24) ? 1 : -1];
typedef char hiscore_music_at_31[(offsetof(hiscore_filenames_t, menu_bgm) == 31) ? 1 : -1];
typedef char hiscore_numbers_at_34[(offsetof(hiscore_filenames_t, number_font) == 34) ? 1 : -1];
typedef char hiscore_ranks_at_44[(offsetof(hiscore_filenames_t, rank_font) == 44) ? 1 : -1];
#endif

// Semantic display order and the seven real screen-line counts.
// Every table entry names a complete foreign UI string object; no raw addresses.
#pragma option -zCALLCAST_LINES_DATA_TEXT -zPgroup_01
#include "src/maine/allcast/credits_data.hpp"

const uint8_t far *LINES[ALLCAST_CREDIT_LINE_COUNT] = {
    allcast_project,
    allcast_th01_title,
    allcast_th01_reimu,
    allcast_th02_title,
    allcast_th02_reimu,
    allcast_th02_rika,
    allcast_th02_meira,
    allcast_th02_marisa,
    allcast_th02_mima,
    allcast_th03_title,
    allcast_th03_reimu,
    allcast_th03_marisa,
    allcast_th03_mima,
    allcast_th03_ellen,
    allcast_th03_kotohime,
    allcast_th03_kana,
    allcast_th03_rikako,
    allcast_th03_chiyuri,
    allcast_th03_yumemi,
    allcast_th04_title,
    allcast_th04_reimu,
    allcast_th04_marisa,
    allcast_th04_orange,
    allcast_th04_kurumi,
    allcast_th04_elly,
    allcast_th04_yuuka,
    allcast_th04_mugetsu,
    allcast_th04_gengetsu,
    allcast_th05_title,
    allcast_th05_reimu,
    allcast_th05_marisa,
    allcast_th05_mima,
    allcast_th05_yuuka,
    allcast_th05_sara,
    allcast_th05_louise,
    allcast_th05_alice,
    allcast_th05_yuki,
    allcast_th05_mai,
    allcast_th05_yumeko,
    allcast_th05_shinki,
    allcast_credit_program,
    allcast_credit_graphics,
    allcast_credit_music,
    allcast_credit_pmd,
    allcast_credit_thanks,
    allcast_credit_makers,
    allcast_credit_players,
};

int allcast_lines_per_screen[7] = {
    1, 2, 6, 10, 9, 12, 7
};

typedef char allcast_pointer_table_is_188[(sizeof(LINES) == 188) ? 1 : -1];
typedef char allcast_screen_counts_are_14[
    (sizeof(allcast_lines_per_screen) == 14) ? 1 : -1];

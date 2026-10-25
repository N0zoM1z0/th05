// Semantic all-cast UI text, its real far pointer table, and seven counts.
// Canonical text source is UTF-8; compiler staging must explicitly use CP932.
#ifndef TH05_ALLCAST_DATA_HPP
#define TH05_ALLCAST_DATA_HPP
#include "src/shared/abi.hpp"
#if GAME != 5 || BINARY != 'E'
#error This owner requires the TH05 MAINE data context
#endif

static const int ALLCAST_CREDIT_LINE_COUNT = 47;
extern uint8_t allcast_project[];
extern uint8_t allcast_th01_title[];
extern uint8_t allcast_th01_reimu[];
extern uint8_t allcast_th02_title[];
extern uint8_t allcast_th02_reimu[];
extern uint8_t allcast_th02_rika[];
extern uint8_t allcast_th02_meira[];
extern uint8_t allcast_th02_marisa[];
extern uint8_t allcast_th02_mima[];
extern uint8_t allcast_th03_title[];
extern uint8_t allcast_th03_reimu[];
extern uint8_t allcast_th03_marisa[];
extern uint8_t allcast_th03_mima[];
extern uint8_t allcast_th03_ellen[];
extern uint8_t allcast_th03_kotohime[];
extern uint8_t allcast_th03_kana[];
extern uint8_t allcast_th03_rikako[];
extern uint8_t allcast_th03_chiyuri[];
extern uint8_t allcast_th03_yumemi[];
extern uint8_t allcast_th04_title[];
extern uint8_t allcast_th04_reimu[];
extern uint8_t allcast_th04_marisa[];
extern uint8_t allcast_th04_orange[];
extern uint8_t allcast_th04_kurumi[];
extern uint8_t allcast_th04_elly[];
extern uint8_t allcast_th04_yuuka[];
extern uint8_t allcast_th04_mugetsu[];
extern uint8_t allcast_th04_gengetsu[];
extern uint8_t allcast_th05_title[];
extern uint8_t allcast_th05_reimu[];
extern uint8_t allcast_th05_marisa[];
extern uint8_t allcast_th05_mima[];
extern uint8_t allcast_th05_yuuka[];
extern uint8_t allcast_th05_sara[];
extern uint8_t allcast_th05_louise[];
extern uint8_t allcast_th05_alice[];
extern uint8_t allcast_th05_yuki[];
extern uint8_t allcast_th05_mai[];
extern uint8_t allcast_th05_yumeko[];
extern uint8_t allcast_th05_shinki[];
extern uint8_t allcast_credit_program[];
extern uint8_t allcast_credit_graphics[];
extern uint8_t allcast_credit_music[];
extern uint8_t allcast_credit_pmd[];
extern uint8_t allcast_credit_thanks[];
extern uint8_t allcast_credit_makers[];
extern uint8_t allcast_credit_players[];

extern const uint8_t far *LINES[ALLCAST_CREDIT_LINE_COUNT];
extern int allcast_lines_per_screen[7];

typedef char allcast_data_pointer_is_far[
    (sizeof(const uint8_t far *) == 4) ? 1 : -1];
typedef char allcast_data_count_is_word[(sizeof(int) == 2) ? 1 : -1];
#endif

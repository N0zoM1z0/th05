// Complete TH05 score-section ABI, corroborated by natural ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th04/formats/scoredat/scoredat.hpp.
#ifndef TH05_OP_HISCORE_VIEW_HPP
#define TH05_OP_HISCORE_VIEW_HPP

#include "src/op/main/menu.hpp"
#include "src/op/main/strings.hpp"

#define SCOREDAT_FN "GENSOU.SCR"
#define SCOREDAT_PLACES 5
#define SCOREDAT_NAME_LEN 8
#define SCOREDAT_NOT_CLEARED 18
#define SCOREDAT_CLEARED 0x80
#define GAIJI_W 16
#define BFNT_ASSUMED_MAX_W 64
#define BGM_HISCORE_FN "name"
#define HISCORE_BG_FN "hi01.pi"
#define HISCORE_STATIC_ASSERT(condition_value) ((void)sizeof(char[1 - 2*!(condition_value)]))
#define palette_settone(tone_value) (PaletteTone = tone_value, palette_show())
static const uint8_t INPUT_NONE = 0;
typedef int playchar2;

// These are semantic glyph identifiers. The complete value domain is the
// original one-byte gaiji domain, including the FF empty sentinel.
enum hiscore_gaiji_t {
    g_NULL = 0,
    gb_0 = 0xA0,
    gb_1 = 0xA1,
    gb_5 = 0xA5,
    gb_6 = 0xA6,
    gs_DOT = 0xC4,
    g_HISCORE_STAGE_EMPTY = 0xEF,
    g_NONE = 0xFF
};

struct scoredat_t {
    unsigned char g_name[SCOREDAT_PLACES][SCOREDAT_NAME_LEN + 1];
    score_lebcd_t g_score[SCOREDAT_PLACES];
    unsigned char g_stage[SCOREDAT_PLACES];
    unsigned char cleared;
    unsigned char unused_1;
};
struct scoredat_section_t {
    char key1;
    char key2;
    int score_sum;
    scoredat_t score;
};
extern scoredat_section_t hi;
extern scoredat_section_t hi2;
extern unsigned char rank;
extern unsigned char cleared_with[PLAYCHAR_COUNT][RANK_COUNT];
uint8_t pascal near scoredat_decode(void);
void pascal near scoredat_encode(void);
#define scoredat_decode_func scoredat_decode
#define scoredat_encode_func scoredat_encode
void near scoredat_recreate(void);
bool pascal near hiscore_scoredat_load_for(playchar2 playchar);

extern "C" {
    int pascal far file_ropen(const char far *filename);
    int pascal far file_read(void far *buffer, unsigned int bytes);
    int pascal far file_create(const char far *filename);
    int pascal far file_write(const void far *buffer, unsigned int bytes);
    void pascal far file_seek(long offset, int origin);
    void pascal far file_close(void);
    int pascal far file_exist(const char far *filename);
    void pascal far graph_gaiji_putc(screen_x_t left, vram_y_t top, int glyph, vc2 color);
    void pascal far graph_gaiji_puts(screen_x_t left, vram_y_t top, pixel_t step,
        const char far *text, vc2 color);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far super_put(int left, int top, int patnum);
    void pascal far palette_black_in(unsigned int speed);
}

typedef char th05_hiscore_payload_is_92[(sizeof(scoredat_t) == 92) ? 1 : -1];
typedef char th05_hiscore_names_at_0[(offsetof(scoredat_t, g_name) == 0) ? 1 : -1];
typedef char th05_hiscore_scores_at_45[(offsetof(scoredat_t, g_score) == 45) ? 1 : -1];
typedef char th05_hiscore_stages_at_85[(offsetof(scoredat_t, g_stage) == 85) ? 1 : -1];
typedef char th05_hiscore_cleared_at_90[(offsetof(scoredat_t, cleared) == 90) ? 1 : -1];
typedef char th05_hiscore_unused_at_91[(offsetof(scoredat_t, unused_1) == 91) ? 1 : -1];
typedef char th05_hiscore_section_is_96[(sizeof(scoredat_section_t) == 96) ? 1 : -1];
typedef char th05_hiscore_key1_at_0[(offsetof(scoredat_section_t, key1) == 0) ? 1 : -1];
typedef char th05_hiscore_key2_at_1[(offsetof(scoredat_section_t, key2) == 1) ? 1 : -1];
typedef char th05_hiscore_sum_at_2[(offsetof(scoredat_section_t, score_sum) == 2) ? 1 : -1];
typedef char th05_hiscore_score_at_4[(offsetof(scoredat_section_t, score) == 4) ? 1 : -1];
typedef char th05_hiscore_gaiji_is_1[(sizeof(hiscore_gaiji_t) == 1) ? 1 : -1];
typedef char th05_hiscore_playchar_parameter_is_2[(sizeof(playchar2) == 2) ? 1 : -1];

#endif

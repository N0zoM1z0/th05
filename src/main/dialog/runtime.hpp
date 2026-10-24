// Natural TH05 dialog interpreter/box ABI, independent of accepted file.cpp.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th04/main/dialog/shared.cpp,
// th05/main/dialog/dialog.cpp, th05/formats/dialog.hpp and master.lib headers.
#ifndef TH05_MAIN_DIALOG_RUNTIME_HPP
#define TH05_MAIN_DIALOG_RUNTIME_HPP
#include "src/main/hud/resident.hpp"
#include "src/main/dialog/file.hpp"

typedef uint8_t shiftjis_t;
typedef int screen_x_t;
typedef int screen_y_t;
typedef int dialog_x_t;
typedef int dialog_y_t;
typedef unsigned int uscreen_x_t;
typedef unsigned int uvram_y_t;

// Complete TX2 sprite command payload. The original byte-packed header is
// declared before the TU's later -a2 switch-table alignment pragma.
struct tx2_op_06_params {
    screen_x_t left;
    screen_y_t top;
    uint8_t patnum;
};
// All command bytes are described;07/08 are reserved and return false.
enum dialog_opcode_t {
    DIALOG_SIDE_PLAYCHAR = 0x00,
    DIALOG_SIDE_BOSS = 0x01,
    DIALOG_FACE = 0x02,
    DIALOG_LOAD_SPRITES = 0x03,
    DIALOG_CLEAR_STAGE_SPRITES = 0x04,
    DIALOG_MUSIC = 0x05,
    DIALOG_PUT_SPRITE = 0x06,
    DIALOG_RESERVED_07 = 0x07,
    DIALOG_RESERVED_08 = 0x08,
    DIALOG_WHITE_OUT = 0x09,
    DIALOG_WHITE_IN = 0x0A,
    DIALOG_LINEBREAK = 0x0B,
    DIALOG_GAIJI = 0x0C,
    DIALOG_BOX_BEGIN = 0x0D,
    DIALOG_BOX_WIPE = 0x0E,
    DIALOG_END = 0xFF
};
struct DialogCursor {
    dialog_x_t x;
    dialog_y_t y;
};
enum dialog_side_t {
    SIDE_PLAYCHAR = 0, SIDE_BOSS = 1, _dialog_side_t_FORCE_INT16 = 0x7FFF
};
extern DialogCursor dialog_cursor;
extern dialog_side_t dialog_side;
extern shiftjis_t near dialog_kanji_buf[3];
extern unsigned int key_det;

static const int PLAYFIELD_LEFT = 32;
static const int PLAYFIELD_RIGHT = 416;
static const int PLAYFIELD_BOTTOM = 384;
static const int PLAYFIELD_W = 384;
static const int FACE_W = 128;
static const int FACE_H = 128;
static const int GLYPH_HALF_W = 8;
static const int GLYPH_FULL_W = 16;
static const int GLYPH_H = 16;
static const int GAIJI_W = 16;
static const int BOX_W = 320;
static const int BOX_H = 48;
static const int BOX_TRAM_H = BOX_H / GLYPH_H;
static const int BOX_TILE_COUNT = 3;
static const int MARGIN = 16;
static const int TEXT_W = PLAYFIELD_W - MARGIN - FACE_W;
static const int TEXT_TRAM_W = TEXT_W / GLYPH_HALF_W;
static const screen_x_t BOX_PLAYCHAR_LEFT = PLAYFIELD_RIGHT - MARGIN - BOX_W;
static const screen_y_t BOX_PLAYCHAR_TOP = PLAYFIELD_BOTTOM - MARGIN - BOX_H;
static const screen_x_t TEXT_PLAYCHAR_LEFT = PLAYFIELD_RIGHT - MARGIN - TEXT_W;
static const screen_y_t TEXT_PLAYCHAR_TOP = BOX_PLAYCHAR_TOP;
static const screen_x_t FACE_PLAYCHAR_LEFT = TEXT_PLAYCHAR_LEFT - FACE_W;
static const screen_y_t FACE_PLAYCHAR_TOP = PLAYFIELD_BOTTOM - MARGIN - FACE_H;
static const screen_x_t BOX_BOSS_LEFT = PLAYFIELD_LEFT + MARGIN;
static const screen_y_t BOX_BOSS_TOP = BOX_PLAYCHAR_TOP - FACE_H;
static const screen_x_t TEXT_BOSS_LEFT = BOX_BOSS_LEFT;
static const screen_y_t TEXT_BOSS_TOP = BOX_BOSS_TOP;
static const screen_x_t FACE_BOSS_LEFT = TEXT_BOSS_LEFT + TEXT_W;
static const screen_y_t FACE_BOSS_TOP = FACE_PLAYCHAR_TOP - FACE_H;
static const unsigned int TX_BLUE = 0x21;
static const unsigned int TX_WHITE = 0xE1;
static const int PAT_STAGE = 180;
static const int PAT_STAGE_last = 319;
static const unsigned char STAGE_EXTRA = 6;
static const int KAJA_SONG_PLAY = 0;
static const int KAJA_SONG_STOP = 1;
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };

inline dialog_x_t to_dialog_x(screen_x_t x) { return x / GLYPH_HALF_W; }
inline dialog_y_t to_dialog_y(screen_y_t y) { return y / GLYPH_H; }
inline int to_tram_x(dialog_x_t x) { return x; }
inline int to_tram_y(dialog_y_t y) { return y; }

extern "C" {
    extern unsigned int vsync_Count1;
    void pascal far text_putca(unsigned x, unsigned y, unsigned character, unsigned attribute);
    void pascal far text_putsa(unsigned x, unsigned y, const char far *text, unsigned attribute);
    void pascal far text_boxfilla(unsigned x1, unsigned y1, unsigned x2, unsigned y2, unsigned attribute);
    void pascal far gaiji_putca(unsigned x, unsigned y, unsigned glyph, unsigned attribute);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far super_clean(int first, int end);
    void pascal far super_roll_put(int left, int top, int patnum);
    void pascal far palette_white_out(unsigned speed);
    void pascal far palette_white_in(unsigned speed);
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
    int pascal far snd_kaja_interrupt(int ax);
}
void pascal far frame_delay(int frames);
int far input_reset_sense(void);
int far input_sense(void);
int pascal far input_wait_for_change(int frames);
void near overlay_wipe(void);
// Genuine foreign routines: box_put retains its original compiler-body ASM
// and the face loader calls the original hardware unblitter. No bodies here.
void pascal near dialog_box_put(uscreen_x_t left, uvram_y_t top, int tile);
void pascal near dialog_face_load_unput_put_free_8(screen_x_t left, screen_y_t top, int face);
void near main_pat_exalice_override_and_super_clean_stage(void);

void pascal near dialog_box_wipe(dialog_x_t left, dialog_y_t top);
void near dialog_box_fade_in_animate(void);
bool pascal near dialog_op(uint8_t command);
void near dialog_run(void);

inline void dialog_text_put(shiftjis_t *const &text) {
    text_putsa(to_tram_x(dialog_cursor.x), to_tram_y(dialog_cursor.y),
        reinterpret_cast<const char far *>(text), TX_WHITE);
    dialog_cursor.x += to_dialog_x(GLYPH_FULL_W);
}
template <class T> inline void dialog_op_gaiji(const T &glyph) {
    gaiji_putca(to_tram_x(dialog_cursor.x), to_tram_y(dialog_cursor.y), glyph, TX_WHITE);
    dialog_cursor.x += to_dialog_x(GAIJI_W);
}
inline void dialog_op_linebreak(void) {
    dialog_cursor.y += to_dialog_y(GLYPH_H);
    dialog_cursor.x = (dialog_side == SIDE_PLAYCHAR)
        ? to_dialog_x(TEXT_PLAYCHAR_LEFT) : to_dialog_x(TEXT_BOSS_LEFT);
}
#define snd_kaja_func(function, parameter) snd_kaja_interrupt(((function) << 8) | static_cast<uint8_t>(parameter))
#define dialog_op_super_clean_stage() { super_clean(PAT_STAGE, PAT_STAGE_last + 1); }
#define dialog_delay(speedup_cycle) { \
    if(key_det == 0) { frame_delay(2); } \
    else if(speedup_cycle & 1) { frame_delay(1); } \
}

typedef char th05_dialog_cursor_is_4[(sizeof(DialogCursor) == 4) ? 1 : -1];
typedef char th05_dialog_cursor_y_at_2[(offsetof(DialogCursor, y) == 2) ? 1 : -1];
typedef char th05_dialog_side_is_2[(sizeof(dialog_side_t) == 2) ? 1 : -1];
typedef char th05_dialog_command_is_1[(sizeof(dialog_opcode_t) == 1) ? 1 : -1];
typedef char th05_dialog_sprite_command_is_5[(sizeof(tx2_op_06_params) == 5) ? 1 : -1];
typedef char th05_dialog_sprite_top_at_2[(offsetof(tx2_op_06_params, top) == 2) ? 1 : -1];
typedef char th05_dialog_sprite_patnum_at_4[(offsetof(tx2_op_06_params, patnum) == 4) ? 1 : -1];
typedef char th05_dialog_kanji_buffer_is_3[(sizeof(dialog_kanji_buf) == 3) ? 1 : -1];
#endif

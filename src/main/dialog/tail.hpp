// Natural remaining TH05 dialog-animation/face/exit/sprite-owner ABI.
// ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
#ifndef TH05_MAIN_DIALOG_TAIL_HPP
#define TH05_MAIN_DIALOG_TAIL_HPP
#include "src/main/ems/ems.hpp"
#include "src/main/demo/demo.hpp"

// demo.hpp declares its genuine code contexts. Capture all new owner
// functions only after restoring this TU's one real contribution.
#pragma codeseg DIALOG_TAIL_TEXT main_01

enum dialog_side_t {
    SIDE_PLAYCHAR = 0, SIDE_BOSS = 1, _dialog_side_t_FORCE_INT16 = 0x7FFF
};
extern dialog_side_t dialog_side;
extern signed char dialog_sequence_id;
extern unsigned char page_front;
extern unsigned char page_back;
extern char near faceset_boss_format[];
extern char near faceset_playchar_format[];
extern const char near st06_bb1[];
extern const char near st06_bb2[];
extern const char near BGM_EXTRA_BOSS_FN[];
extern const char near DEMO_EXTRA_PART_2_FN[];
extern const char near DIALOG_BINARY_OP[];
extern const char near BOMB_BG_REIMU_FN[];
extern const char near BOMB_BG_MARISA_FN[];
extern const char near BOMB_BG_MIMA_FN[];
extern const char near BOMB_BG_YUUKA_FN[];
extern const char near BOMB_SHAPE_FN_2[];
extern const char near BOMB_SHAPE_YUUKA_FN_2[];
extern const char near MIKO16_EXALICE_FN[];

static const uint8_t FACE_NONE = 0xFF;
static const int TINY_MIKO16_START = 36;
static const int TINY_MIKO16_END = 172;
static const int PAT_MAX = 320;
static const int KAJA_SONG_PLAY = 0;
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
extern "C" {
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
    int pascal far snd_kaja_interrupt(int ax);
    int pascal far super_entry_bfnt(const char far *filename);
    void pascal far super_clean(int first, int end);
    int pascal far super_convert_tiny(int patnum);
    void pascal far cdg_load_single(int slot, const char far *filename, int n);
    void pascal far cdg_put_8(int left, int top, int slot);
}
void pascal far frame_delay(int frames);
void near overlay_wipe(void);
void near playfield_copy_front_to_back(void);
void pascal near dialog_face_unput_8(unsigned left, unsigned top);
void near dialog_box_fade_in_animate(void);
void near dialog_run(void);
// Preserve the genuine near first declaration of this late sprite owner.
void near main_pat_exalice_override_and_super_clean_stage(void);
void far dialog_animate(void);
void pascal near dialog_face_load_unput_put_free_8(int left, int top, int face_id);
void near dialog_exit(void);

#define graph_accesspage(page) outportb(0xA6, page)
#define snd_kaja_func(function, parameter) snd_kaja_interrupt(((function) << 8) | static_cast<uint8_t>(parameter))
inline void dialog_pre(void) {
    overlay_wipe();
    palette_settone(100);
    graph_accesspage(page_front);
    dialog_box_fade_in_animate();
    playfield_copy_front_to_back();
}
inline void dialog_post(void) {
    graph_accesspage(page_back);
    frame_delay(1);
}
inline void playchar_bomb_bg_load_from_ems(void) {
    size_t size = cdg_slots[CDG_BG_PLAYCHAR_BOMB].bitplane_size * PLANE_COUNT;
    allocate_and_load_from_ems(cdg_slots[CDG_BG_PLAYCHAR_BOMB].seg_colors(),
        EMS_PLAYCHAR_BOMB_BG_OFFSET, size);
}

typedef char th05_tail_side_is_2[(sizeof(dialog_side_t) == 2) ? 1 : -1];
typedef char th05_tail_sequence_is_1[(sizeof(dialog_sequence_id) == 1) ? 1 : -1];
typedef char th05_tail_page_is_1[(sizeof(page_front) == 1) ? 1 : -1];
typedef char th05_tail_playchar_is_1[(sizeof(playchar_t) == 1) ? 1 : -1];
typedef char th05_tail_replay_chunk_is_40000[(DEMO_N_EXTRA * sizeof(REC<1>) == 40000U) ? 1 : -1];
#endif

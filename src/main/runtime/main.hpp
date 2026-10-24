// Complete MAIN entry interfaces. TH05 operands are reviewed independently;
// maintained TH04 core sources supply semantic provenance, not exact evidence.
#ifndef TH05_RUNTIME_MAIN_HPP
#define TH05_RUNTIME_MAIN_HPP
#include "src/main/hud/resident.hpp"

#if GAME != 5 || BINARY != 'M'
#error This producer implements the TH05 MAIN runtime prefix
#endif

// Identical complete enum to the accepted generic boss interface.
enum quit_t { Q_KEEP_RUNNING = 0, Q_QUIT_TO_OP = 1, Q_NEXT_STAGE = 2 };
extern quit_t quit;
extern unsigned int mem_assign_paras;
extern long random_seed;

// Foreign filenames are actual existing objects; no payload is supplied here.
extern const unsigned char main_pf_fn[];
extern const char se_fn[];
extern const char op_fn[];

#pragma codeseg RUNTIME_MAIN01_TEXT main_01
resident_t __seg *near cfg_load_resident_ptr(void);
void near ems_allocate_and_preload_eyecatch(void);
void near stage_session_init(void);
extern "C" void near stage_session_free(void);
int pascal far GameExecl(const char far *binary_fn);

#pragma codeseg SHARED
int pascal far game_init_main(const unsigned char far *pf_fn);
enum snd_load_func_t { SND_LOAD_SONG = 0x0600, SND_LOAD_SE = 0x0B00 };
extern "C" {
    int pascal far snd_determine_modes(int req_bgm_mode, int req_se_mode);
    void pascal far snd_load(const char far *filename, snd_load_func_t operation);
}
#pragma codeseg _TEXT
extern "C" void pascal far text_clear(void);

#pragma codeseg DEMO_TEXT main_01
void near gameplay_loop(void);
#pragma codeseg

typedef char runtime_quit_is_1[(sizeof(quit_t) == 1) ? 1 : -1];
typedef char runtime_resident_is_128[(sizeof(resident_t) == 128) ? 1 : -1];
typedef char runtime_resident_rand_at_40[(offsetof(resident_t, rand) == 40) ? 1 : -1];
typedef char runtime_resident_bgm_at_18[(offsetof(resident_t, bgm_mode) == 18) ? 1 : -1];
typedef char runtime_resident_se_at_21[(offsetof(resident_t, se_mode) == 21) ? 1 : -1];
typedef char runtime_resident_pointer_is_4[(sizeof(resident) == 4) ? 1 : -1];
typedef char runtime_memory_paragraphs_is_2[(sizeof(mem_assign_paras) == 2) ? 1 : -1];
#endif

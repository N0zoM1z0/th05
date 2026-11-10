// Complete natural MAINE score codec / registration compiler context.
// All 14 real function bodies remain in original order; no artificial CODE prefix.
// Includes only the genuine one-byte local ROR required by the score file format.
#pragma option -zCREG_FULL_TEXT
#include "src/main/hud/resident.hpp"
// Both genuine codec function definitions now precede the score lifecycle.
#pragma codeseg REG_FULL_TEXT GROUP_01
unsigned char pascal near scoredat_decode(void);
void pascal near scoredat_encode(void);
// Score lifecycle function signatures must precede their general header.
#pragma codeseg REG_FULL_TEXT GROUP_01
void near scoredat_recreate(void);
bool pascal near hiscore_scoredat_load_for(int pc);
void near hiscore_scoredat_save(void);
#pragma codeseg _TEXT
// The two complete type headers do not declare the nine owned functions.
#include "src/op/hiscore/view.hpp"
#include "src/maine/score/end.hpp"
#include "src/maine/registration/glyphball.hpp"
// Exact real declarations; registration and sound headers separately declare
// two incompatible original game-specific sound enum names in this combined TU.
#pragma codeseg SHARED
extern "C" void far snd_se_update(void);
void pascal far frame_delay(int frames);
extern unsigned char registration_page;
#pragma codeseg REG_FULL_TEXT GROUP_01
void near scoredat_recreate(void);
bool pascal near hiscore_scoredat_load_for(int pc);
void near hiscore_scoredat_save(void);
void near score_insert(void);
void pascal near registration_score_put(int place, int pc);
void pascal near registration_stage_put(int place, int pc, int glyph);
void pascal near reg_name_put(int place, playchar_t pc, uint8_t cursor);
void pascal near registration_place_put(int place, int pc);
void pascal near places_put(int pc);
void pascal near alphabet_cursor_put(int col, int row, int attr);
void near registration_frame(void);
void pascal near glyphball_spawn(int x, int y, int place, playchar_t pc, uint8_t cursor);
void near glyphballs_update(void);
void near glyphballs_commit_and_wait(void);
void near regist_menu(void);
#include "src/maine/registration/values.hpp"
#include "src/maine/registration/insert.hpp"
#include "src/maine/registration/display.hpp"
#include "src/maine/registration/places.hpp"
#include "src/maine/registration/alphabet.hpp"
#include "src/maine/registration/motion.hpp"
#include "src/maine/registration/menu.hpp"
#pragma codeseg REG_FULL_TEXT GROUP_01
// First eight-byte score key and original near-Pascal cipher interface.
// The one-byte local rotate is genuinely required by the original codec.
unsigned char pascal near scoredat_decode(void)
{
    int index;
    int checksum;
    for(index = offsetof(scoredat_section_t, score);
        index < (sizeof(scoredat_section_t) - 1); index++) {
        unsigned char value = reinterpret_cast<unsigned char *>(&hi)[index + 1];
        _AL = hi.key2;
        asm { ror value, 3; }
        value ^= _AL;
        reinterpret_cast<unsigned char *>(&hi)[index] =
            (hi.key1 + value + reinterpret_cast<unsigned char *>(&hi)[index]);
    }
    reinterpret_cast<unsigned char *>(&hi)[index] += hi.key1;
    checksum = 0;
    for(index = offsetof(scoredat_section_t, score);
        index < sizeof(scoredat_section_t); index++) {
        checksum += reinterpret_cast<unsigned char *>(&hi)[index];
    }
    return (hi.score_sum - checksum);
}
void pascal near scoredat_encode(void)
{
    int index;
    hi.score_sum = 0;
    for(index = offsetof(scoredat_section_t, score);
        index < sizeof(scoredat_section_t); index++) {
        hi.score_sum += reinterpret_cast<unsigned char *>(&hi)[index];
    }
    hi.key1 = irand();
    hi.key2 = irand();
    unsigned char feedback = 0;
    index = sizeof(scoredat_section_t) - 1;
    while(index >= offsetof(scoredat_section_t, score)) {
        reinterpret_cast<unsigned char *>(&hi)[index] -= (hi.key1 + feedback);
        feedback = reinterpret_cast<unsigned char *>(&hi)[index];
        _AL = hi.key2;
        asm { ror feedback, 3; }
        feedback ^= _AL;
        index--;
    }
}


#include "src/maine/score/end_body.inl"

#pragma option -a
#include "src/maine/registration/insert.inl"
#include "src/maine/registration/score.inl"
#include "src/maine/registration/stage.inl"
#include "src/maine/registration/name.inl"
#include "src/maine/registration/place.inl"
#include "src/maine/registration/places.inl"
#include "src/maine/registration/alphabet_body.inl"

#include "src/maine/registration/frame_body.inl"

#pragma option -a
#include "src/maine/registration/spawn.inl"
#include "src/maine/registration/update.inl"
#include "src/maine/registration/commit_body.inl"

#include "src/maine/registration/menu.inl"

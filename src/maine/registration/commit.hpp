// True far integer/sound APIs and the foreign no-result registration frame.
#ifndef TH05_MREG_COMMIT_HPP
#define TH05_MREG_COMMIT_HPP
#pragma codeseg SHARED
#include "src/shared/sound/se.hpp"
#pragma codeseg _TEXT
extern "C" int pascal far iatan2(int y, int x);
#pragma codeseg REG_FRAME_TEXT GROUP_01
void near registration_frame(void);
#pragma codeseg REG_COMMIT_TEXT GROUP_01
void near glyphballs_commit_and_wait(void);
#pragma codeseg
#include "src/maine/registration/glyphball.hpp"
#endif

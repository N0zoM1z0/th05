// Real three-word near-Pascal cursor API; Master glyph output is far Pascal.
#ifndef TH05_MREG_ALPHA_HPP
#define TH05_MREG_ALPHA_HPP
#pragma codeseg _TEXT
extern "C" void pascal far gaiji_putca(int x, int y, int glyph, int attr);
#pragma codeseg REG_ALPHA_TEXT GROUP_01
void pascal near alphabet_cursor_put(int col, int row, int attr);
#pragma codeseg
#include "src/maine/registration/glyphball.hpp"
#endif

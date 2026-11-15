// The Music Room, compiled as one translation unit. The UTF-8 sources are
// converted to Shift-JIS before compilation. See NOTES.md for why
// nopoly_B_put() in here does not match.
#pragma option -zCOP_MUSIC_TEXT -zPop_01
#include <dos.h>
#include <mem.h>
#include "src/op/music/music.hpp"
#include "src/op/main/strings.hpp"
#include "src/op/music/titles.hpp"
#pragma codeseg OP_MUSIC_TEXT op_01
#include "src/op/music/music_body.inl"

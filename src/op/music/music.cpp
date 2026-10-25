// Natural TH05 Music Room frontend, adapted from ReC98
// b6ba5b0a529edbb31efdf8c0e939263804f8ee47: th02/op/m_music.cpp, GAME=5.
// UTF-8 source is consumed as CP932. The DS-copy helper is context only and
// remains unaccepted; all credited complete function scopes are separate.
#pragma option -zCOP_MUSIC_TEXT -zPop_01
#include <dos.h>
#include <mem.h>
#include "src/op/music/music.hpp"
#include "src/op/main/strings.hpp"
#include "src/op/music/titles.hpp"
#pragma codeseg OP_MUSIC_TEXT op_01
#include "src/op/music/music_body.inl"

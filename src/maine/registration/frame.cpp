// Complete TH05 registration frame, original [BD1E,BD46).
// Natural semantics reviewed against ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47
// th05_maine.asm sub_BD1E and the original decoded MAINE instructions.
#pragma option -zCREG_FRAME_TEXT -zPGROUP_01
#include "src/maine/registration/frame.hpp"
#pragma codeseg REG_FRAME_TEXT GROUP_01

#include "src/maine/registration/frame_body.inl"

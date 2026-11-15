// The ZUN Soft logo animation shown on OP.EXE's first start: fireworks
// ("pyros") over ZUN00.PI, timed to the LOGO song. Based on ReC98
// th04/op/zunsoft.cpp, with TH05's differences.
#pragma option -zCOP_ZUNSOFT_TEXT -zPop_01
#include "src/op/zunsoft/zunsoft.hpp"
#pragma codeseg OP_ZUNSOFT_TEXT op_01
#include "src/op/zunsoft/zunsoft_pyro_new.inl"
#include "src/op/zunsoft/zunsoft_update_and_render.inl"
#include "src/op/zunsoft/zunsoft_palette_update_and_show.inl"
#include "src/op/zunsoft/zunsoft_animate.inl"

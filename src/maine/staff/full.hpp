// Declarations for the 17 staff scene functions compiled by full.cpp and
// staff_complete_context.cpp.
#ifndef TH05_MAINE_STAFF_FULL_HPP
#define TH05_MAINE_STAFF_FULL_HPP
#ifndef TH05_STAFF_FULL_FAMILY
#error Define TH05_STAFF_FULL_FAMILY to put every staff function into STAFF_FULL_TEXT
#endif
// lifecycle.hpp must come first: it declares grc_setclip() and
// space_window_set() before staff.hpp redeclares them.
#include "src/maine/staff/lifecycle.hpp"
#include "src/maine/staff/orb_opening.hpp"
#include "src/maine/staff/rain.hpp"
#include "src/maine/staff/wipe.hpp"
#include "src/maine/staff/image_phase.hpp"
#include "src/maine/staff/reveal_b.hpp"
#include "src/maine/staff/render.hpp"
#include "src/maine/staff/frame.hpp"
#endif

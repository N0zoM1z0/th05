// Per-difficulty bullet template tuning wrappers, all of which first adjust
// the stack size of stacked groups by play performance. Same as ReC98's
// th05/main/bullet/tune.cpp.
#pragma option -zCBULLET_A_TEXT -zPmain_03

#include <dos.h>
#include "src/main/bullet/tune.hpp"

#pragma option -k-

// Each `codestring "\x90"` reproduces a word-alignment NOP that the original
// has between these functions.

extern "C" {

static inline uint8_t not_aimed() {
	return ~BGC0_AIMED;
}

// Stacked groups get one more bullet at high play performance and one less
// (but never fewer than one) at low play performance.
void pascal near tune_for_playperf(void)
{
	if((bullet_template.group & not_aimed()) != BG_STACK) {
		return;
	}
	_AL = playperf;
	if(_AL >= 38) {
		bullet_template.stack++;
	} else if(_AL <= 24 && bullet_template.stack >= 2) {
		bullet_template.stack--;
	}
}

#pragma codestring "\x90"

void pascal near bullet_template_tune_easy(void)
{
	tune_for_playperf();
	tune_for_easy();
}

#pragma codestring "\x90"

void pascal near bullet_template_tune_normal(void)
{
	tune_for_playperf();
}

void pascal near bullet_template_tune_hard(void)
{
	tune_for_playperf();
	tune_for_hard();
}

#pragma codestring "\x90"

void pascal near bullet_template_tune_lunatic(void)
{
	tune_for_playperf();
	tune_for_lunatic();
}

#pragma codestring "\x90"

#pragma option -k.

}

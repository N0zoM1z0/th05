// Candidate adapted from nmlgc/ReC98@b6ba5b0a; exactness requires local replay.
#pragma option -zCBULLET_A_TEXT -zPmain_03

#include <dos.h>
#include "src/main/bullet/tune.hpp"

#pragma option -k-

extern "C" {

static inline uint8_t not_aimed() {
	return ~BGC0_AIMED;
}

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

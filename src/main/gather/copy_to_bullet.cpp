// gather.bullet_template = bullet_template, copied as 7 words with REP MOVSW
// (ReC98 th04/main/gather.cpp: copy_near_struct_member(..., prepare_si_di)).
// A plain structure assignment would call Borland's F_SCOPY@ helper instead.
#pragma option -zCGATHER_COPY_TO_TEXT -zPmain_03
#include <stddef.h>
#include "src/main/gather/gather.hpp"
#pragma codeseg GATHER_COPY_TO_TEXT main_03

void pascal near set_gather_template_to_bullet_template(gather_t near &gather)
{
    _CX = (sizeof(BulletTemplate) / sizeof(uint16_t));
    asm { push ds; pop es; }
    _SI = FP_OFF(&bullet_template);
    _DI = FP_OFF(&gather);
    _DI += offsetof(gather_t, bullet_template);
    asm { rep movsw; }
}

// enemy_bullet_template_push(): copies an enemy's bullet template into the
// global bullet_template, as one REP MOVSW.
//
// A plain structure assignment calls Borland's F_SCOPY@ helper instead, and
// the __memcpy__ intrinsic loads SI, DI and CX in a different order; setting
// the registers in this order reproduces the original.
#pragma option -zCENEMY_TEMPLATE_COPY_TEXT -zPmain_03
#include <dos.h>
#include "src/main/bullet/template.hpp"
extern BulletTemplate bullet_template;
#pragma codeseg ENEMY_TEMPLATE_COPY_TEXT main_03
extern "C" void pascal near enemy_bullet_template_push(const BulletTemplate near &source)
{
    _CX = sizeof(BulletTemplate) / sizeof(unsigned int);
    _SI = reinterpret_cast<unsigned int>(&source);
    _DI = reinterpret_cast<unsigned int>(&bullet_template);
    asm { push ds; pop es }
    asm { rep movsw }
}

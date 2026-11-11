// Copy one full native bullet template into the live spawner.
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

// Complete background-particle motion, animation, clipping and drawing.
#pragma option -zCSHINKI_PARTICLE_TEXT -zPmain_01
#include <dos.h>
#include "src/main/boss/background.hpp"
#pragma codeseg SHINKI_PARTICLE_TEXT main_01

typedef char shinki_render_record_is_16[(sizeof(boss_particle_t) == 16) ? 1 : -1];

void near shinki_bg_particles_render(void)
{
    boss_particle_t near *particle;
    int patnum;
    int left;
    int top;
    int i;
    _ES = SEG_PLANE_B;
    particle = boss_particles;
    for(i = 0; i < BOSS_PARTICLE_COUNT; i++, particle++) {
        if(particle->pos.x.v != -999 * 16) {
            particle->pos.x.v += particle->velocity.x.v;
            particle->pos.y.v += particle->velocity.y.v;
            if(particle->patnum == 0) {
                patnum = particle->age / 8;
                if(patnum >= PARTICLE_CELS) {
                    patnum = PARTICLE_CELS - 1;
                }
                patnum += PAT_PARTICLE;
            } else {
                patnum = particle->patnum;
            }
            left = PLAYFIELD_LEFT + (particle->pos.x.v >> 4) - PARTICLE_W / 2;
            top = PLAYFIELD_TOP + (particle->pos.y.v >> 4) - PARTICLE_H / 2;
            if(!(left > PLAYFIELD_LEFT - PARTICLE_W &&
                 left < PLAYFIELD_RIGHT && top > 0 && top < PLAYFIELD_BOTTOM)) {
                particle->pos = particle->origin;
                particle->age = 0;
            } else {
                z_super_roll_put_16x16_mono(left, top, patnum);
                particle->age++;
            }
        }
    }
}

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
            // Prepare the real graphics arguments before clipping. No call
            // intervenes before the draw; comparisons preserve AX and CX.
            _AX = PLAYFIELD_TOP + (particle->pos.y.v >> 4) - PARTICLE_H / 2;
            _CX = left;
            if(!(static_cast<int>(_CX) > PLAYFIELD_LEFT - PARTICLE_W &&
                 static_cast<int>(_CX) < PLAYFIELD_RIGHT &&
                 static_cast<int>(_AX) > 0 &&
                 static_cast<int>(_AX) < PLAYFIELD_BOTTOM)) {
                particle->pos = particle->origin;
                particle->age = 0;
            } else {
                z_super_roll_put_16x16_mono_raw(patnum);
                particle->age++;
            }
        }
    }
}

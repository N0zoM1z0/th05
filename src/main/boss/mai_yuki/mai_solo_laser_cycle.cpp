// Natural radial fixed-laser lifecycle and cycling bullet attacks, TH05.
// Original disassembly corroborated by ReC98 b6ba5b0a; no ASM body copied.
#pragma option -zCMAIN_035_TEXT -zPmain_03
#include "src/main/boss/mai_yuki/mai_solo_laser_cycle.hpp"
#pragma codeseg MAIN_035_TEXT main_03

#define mai_laser_direction boss_statebyte[15]
#define mai_laser_patterns_seen boss_statebyte[10]

bool near mai_solo_laser_cycle(void)
{
    // A phase word serves as initial angular offset, cycle tick, then step.
    int phase;
    int i;
    if(boss.phase_frame == 32) {
        laser_template.col = 8;
        laser_template.coords.width.nonshrink = 8;
        phase = randring2_next16();
        mai_solo_laser_count = rank + 5;
        for(i = 0; i < mai_solo_laser_count; i++) {
            laser_template.coords.angle = ((i << 8) / mai_solo_laser_count) +
                static_cast<unsigned char>(phase);
            laser_manual_fixed_spawn(i);
        }
        mai_solo_laser_fraction = 0;
        mai_solo_laser_speed = 1;
        mai_solo_laser_pattern = mai_solo_rotating_fans;
        mai_laser_direction = 1;
        mai_laser_patterns_seen = 0;
    } else if(boss.phase_frame > 32) {
        phase = (boss.phase_frame - 32) % 256;
        for(i = 0; i < mai_solo_laser_count; i++) {
            lasers[i].coords.origin = boss.pos.cur;
        }
        if(phase == 160) {
            for(i = 0; i < mai_solo_laser_count; i++) {
                laser_manual_grow(i);
            }
        } else if(phase == 212) {
            for(i = 0; i < mai_solo_laser_count; i++) {
                lasers[i].flag = LF_FIXED_SHRINK_AND_WAIT_TO_GROW;
            }
        } else if(phase == 180) {
            mai_laser_direction = -mai_laser_direction;
        }

        if(phase <= 112) {
            mai_solo_laser_speed += stage_frame_mod2;
            if(mai_solo_laser_speed > 0x80) {
                mai_solo_laser_speed = 0x80;
            }
        } else if(phase <= 192) {
            mai_solo_laser_speed -= 2;
            if(mai_solo_laser_speed < 0) {
                mai_solo_laser_speed = 0;
            }
        } else {
            mai_solo_laser_speed += stage_frame_mod2;
            if((phase > 212) && (randring2_next16_and(0x1F) == 0)) {
                boss.phase_frame += 255 - phase;
            }
        }

        if(phase == 0) {
            mai_solo_laser_pattern = mai_solo_laser_patterns[mai_laser_patterns_seen % 3];
            mai_laser_patterns_seen++;
        }
        if(boss.phase_frame >= 288) {
            mai_solo_laser_pattern();
            if((boss.phase_frame >= 544) && (phase <= 96)) {
                boss_flystep_random(phase - 32);
            }
        }
        mai_solo_laser_fraction += mai_solo_laser_speed;
        if(mai_solo_laser_fraction >= 16) {
            // The original unsigned byte direction wraps1/-1 modulo256.
            phase = (mai_solo_laser_fraction / 16) * mai_laser_direction;
            mai_solo_laser_fraction %= 16;
            for(i = 0; i < mai_solo_laser_count; i++) {
                lasers[i].coords.angle = lasers[i].coords.angle + phase;
            }
        }
    }
    return false;
}

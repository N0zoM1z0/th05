// Complete stage-two update, with a read-only bridge for the real packed point return.
#ifndef TH05_STAGE2_BG_COMBINED
#pragma option -zCSTAGE2_TEXT -zPmain_01
#endif
#include "src/main/stage/background2.hpp"
#pragma codeseg STAGE2_TEXT main_01

void pascal near stage2_update(void)
{
    int i;
    int left;
    int right;
    s2particle_t near *particle;

    if(boss.phase > PHASE_BOSS_ENTRANCE_BB && boss.phase < PHASE_BOSS_EXPLODE_BIG) {
        return;
    }
    if(boss.phase == PHASE_BOSS_ENTRANCE_BB && boss.phase_frame >= 32) {
        return;
    }
    if(stage_frame < 304) {
        scroll_active = false;
        if(stage_frame >= 256) {
            i = 303 - stage_frame;
            Palettes.colors[0].c.r = i;
            Palettes.colors[0].c.g = i;
            Palettes.colors[0].c.b = i * 5;
            PaletteTone = stage2_tone_offset + 100;
            palette_changed = true;
            stage2_tone_offset += 2;
            if(stage_frame_mod4 == 0) {
                i = (stage_frame - 256) >> 2;
                left = 11 - i;
                right = i + 12;
                for(i = 0; i < 25; i++) {
                    tile_ring[i][left] = STAGE2_TILE_AREA_VRAM_LEFT + (256 * STAGE2_ROW_SIZE);
                    tile_ring[i][right] = STAGE2_TILE_AREA_VRAM_LEFT + (256 * STAGE2_ROW_SIZE);
                }
            }
        }
        tiles_invalidate_all();
        return;
    }
    if(stage_frame < 306) {
        graph_scrollup(scroll_line);
        for(left = 0; left < 24; left++) {
            for(i = 0; i < 25; i++) {
                tile_ring[i][left] = STAGE2_TILE_AREA_VRAM_LEFT;
            }
        }
        tiles_invalidate_all();
        scroll_active = true;
        stage2_particles_spawned = 0;
        stage2_palette_level = 0;
        stage2_palette_falling = 0;
        return;
    }
    if(stage2_tone_offset != 0) {
        if(stage2_tone_offset > 4) {
            stage2_tone_offset -= 4;
        } else {
            stage2_tone_offset = 0;
        }
        PaletteTone = stage2_tone_offset + 100;
        palette_changed = true;
        return;
    }
    if(stage2_particles_spawned < S2PARTICLE_COUNT && stage_frame_mod2 == 0) {
        particle = &s2particles[stage2_particles_spawned];
        particle->flag = 1;
        particle->angle = randring1_next16_mod(0x20) + 0x30;
        particle->pos.cur.x.v = TO_SP((0x50 - particle->angle) * 8) + TO_SP(64);
        particle->pos.cur.y.v = 0;
        vector2(particle->pos.velocity.x.v, particle->pos.velocity.y.v,
            particle->angle, TO_SP(8));
        stage2_particles_spawned++;
    }
    grcg_setcolor(GC_RMW, 0);
    particle = s2particles;
    for(i = 0; i < S2PARTICLE_COUNT; i++, particle++) {
        if(particle->flag != 0) {
            // Read the actual packed-point return immediately at this ABI boundary.
            // The full PlayfieldPoint return type and Motion object stay unchanged.
            particle->pos.update_seg1();
            if(static_cast<subpixel_t>(_AX) <= -TO_SP(8) ||
                static_cast<subpixel_t>(_AX) >= TO_SP(PLAYFIELD_W + 8) ||
                static_cast<subpixel_t>(_DX) <= -TO_SP(8) ||
                static_cast<subpixel_t>(_DX) >= TO_SP(PLAYFIELD_H + 8)) {
                stage2_particle_init(*particle);
            } else {
                // Real PC-98 VRAM segment consumed by the existing raw renderer.
                _ES = SEG_PLANE_B;
                if((i & 3) != 0) {
                    particle->zoom++;
                }
                left = particle->zoom >> 4;
                if(left >= PARTICLE_CELS - 1) {
                    left = PARTICLE_CELS - 1;
                }
                left += PAT_PARTICLE;
                right = (particle->pos.cur.x.v >> 4) + PLAYFIELD_LEFT - (PARTICLE_W / 2);
                // Existing real AX/CX/ES hardware API, without register hints.
                z_super_roll_put_16x16_mono(right,
                    scroll_subpixel_y_to_vram_seg1(
                        particle->pos.cur.y.v + TO_SP(PLAYFIELD_TOP - (PARTICLE_H / 2))),
                    left);
            }
        }
    }
    grcg_off();
    if(stage_frame_mod4 == 0) {
        if(stage2_palette_falling == 0) {
            stage2_palette_level++;
            if(stage2_palette_level >= 0x3F) {
                stage2_palette_falling++;
            }
        } else {
            stage2_palette_level--;
            if(stage2_palette_level <= 0x20) {
                stage2_palette_falling--;
            }
        }
        Palettes.colors[0].c.r = stage2_palette_level * 2;
        Palettes.colors[0].c.g = stage2_palette_level * 2;
        Palettes.colors[0].c.b = stage2_palette_level * 4;
        palette_changed = true;
    }
}

// Complete stage-two update, with a read-only bridge for the real packed point return.
#ifndef TH05_STAGE2_BG_COMBINED
#pragma option -zCSTAGE2_TEXT -zPmain_01
#endif
#include "src/main/stage/stage2_transition_counters.h"
#include "src/main/stage/stage2_transition_rules.hpp"
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
    if(boss.phase == PHASE_BOSS_ENTRANCE_BB && boss.phase_frame >= S2T_BOSS_ENTRANCE_MAX_FRAME) {
        return;
    }
    if(stage_frame < S2T_FADE_END_FRAME) {
        scroll_active = false;
        if(stage_frame >= S2T_FADE_START_FRAME) {
            i = S2T_FADE_REMAINING_BASE - stage_frame;
            Palettes.colors[0].c.r = i;
            Palettes.colors[0].c.g = i;
            Palettes.colors[0].c.b = i * S2T_BLUE_FADE_SCALE;
            PaletteTone = stage2_tone_offset + S2T_BRIGHTNESS_BASE;
            palette_changed = true;
            stage2_tone_offset += S2T_BRIGHTNESS_INCREMENT;
            if(stage_frame_mod4 == 0) {
                i = (stage_frame - S2T_FADE_START_FRAME) >> S2T_RING_WIPE_SHIFT;
                left = S2T_TILE_WIPE_LEFT_ANCHOR - i;
                right = i + S2T_TILE_WIPE_RIGHT_ANCHOR;
                for(i = 0; i < S2T_SCREEN_WIPE_ROWS; i++) {
                    tile_ring[i][left] = STAGE2_TILE_AREA_VRAM_LEFT + (S2T_RING_WIPE_SOURCE_Y * STAGE2_ROW_SIZE);
                    tile_ring[i][right] = STAGE2_TILE_AREA_VRAM_LEFT + (S2T_RING_WIPE_SOURCE_Y * STAGE2_ROW_SIZE);
                }
            }
        }
        tiles_invalidate_all();
        return;
    }
    if(stage_frame < S2T_SCROLL_END_FRAME) {
        graph_scrollup(scroll_line);
        for(left = 0; left < S2T_SCREEN_WIPE_COLUMNS; left++) {
            for(i = 0; i < S2T_SCREEN_WIPE_ROWS; i++) {
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
        if(stage2_tone_offset > S2T_BRIGHTNESS_DECREMENT) {
            stage2_tone_offset -= S2T_BRIGHTNESS_DECREMENT;
        } else {
            stage2_tone_offset = 0;
        }
        PaletteTone = stage2_tone_offset + S2T_BRIGHTNESS_BASE;
        palette_changed = true;
        return;
    }
    if(stage2_particles_spawned < S2PARTICLE_COUNT && stage_frame_mod2 == S2T_PARTICLE_SPAWN_EVERY_OTHER) {
        particle = &s2particles[stage2_particles_spawned];
        particle->flag = S2T_PARTICLE_INITIAL_FLAG;
        particle->angle = randring1_next16_mod(S2T_PARTICLE_INITIAL_ANGLE_MASK) + S2T_PARTICLE_INITIAL_ANGLE_BIAS;
        particle->pos.cur.x.v = TO_SP((S2T_PARTICLE_X_REF_ANGLE - particle->angle) * S2T_PARTICLE_X_SLOPE) + TO_SP(S2T_PARTICLE_SPAWN_X_BIAS_PX);
        particle->pos.cur.y.v = 0;
        vector2(particle->pos.velocity.x.v, particle->pos.velocity.y.v,
            particle->angle, TO_SP(S2T_PARTICLE_SPAWN_SPEED_PX));
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
            if(stage2_palette_level >= S2T_PALETTE_PULSE_CEILING) {
                stage2_palette_falling++;
            }
        } else {
            stage2_palette_level--;
            if(stage2_palette_level <= S2T_PALETTE_PULSE_FLOOR) {
                stage2_palette_falling--;
            }
        }
        Palettes.colors[0].c.r = stage2_palette_level * S2T_PALETTE_RED_GREEN_SCALE;
        Palettes.colors[0].c.g = stage2_palette_level * S2T_PALETTE_RED_GREEN_SCALE;
        Palettes.colors[0].c.b = stage2_palette_level * S2T_PALETTE_BLUE_SCALE;
        palette_changed = true;
    }
}

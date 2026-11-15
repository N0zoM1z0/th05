// Stage 2 background, run every frame in place of the regular stage render
// function: the fade from the tile map to the particle backdrop, then the
// falling particles and the pulse of palette color 0.
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

    // Nothing happens during the boss fight itself.
    if(boss.phase > PHASE_BOSS_ENTRANCE_BB && boss.phase < PHASE_BOSS_EXPLODE_BIG) {
        return;
    }
    if(boss.phase == PHASE_BOSS_ENTRANCE_BB && boss.phase_frame >= S2T_BOSS_ENTRANCE_MAX_FRAME) {
        return;
    }
    // The stage starts without scrolling. From frame 256, color 0 fades from
    // (47, 47, 235) to black while the screen brightens and the tile map is
    // wiped out.
    if(stage_frame < S2T_FADE_END_FRAME) {
        scroll_active = false;
        if(stage_frame >= S2T_FADE_START_FRAME) {
            i = (S2T_FADE_END_FRAME - 1) - stage_frame;
            Palettes.colors[0].c.r = i;
            Palettes.colors[0].c.g = i;
            Palettes.colors[0].c.b = i * 5;
            PaletteTone = stage2_tone_offset + S2T_BRIGHTNESS_BASE;
            palette_changed = true;
            stage2_tone_offset += S2T_BRIGHTNESS_INCREMENT;
            // One more column on each side every 4 frames
            if(stage_frame_mod4 == 0) {
                i = (stage_frame - S2T_FADE_START_FRAME) >> 2;
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
    // For two frames, reset the whole tile ring to the first source tile,
    // then resume scrolling over the particle backdrop.
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
    // Let the brightness flash decay before the particles start.
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
    // Spawn one new particle every second frame until all are active.
    // ZUN bloat: this repeats the first stream direction of
    // stage2_particle_init() instead of calling it, and leaves the zoom alone.
    if(stage2_particles_spawned < S2PARTICLE_COUNT && stage_frame_mod2 == 0) {
        particle = &s2particles[stage2_particles_spawned];
        particle->flag = 1;
        particle->angle = randring1_next16_mod(S2T_PARTICLE_ANGLE_RANGE) + S2T_PARTICLE_ANGLE_DOWN;
        particle->pos.cur.x.v = TO_SP((S2T_PARTICLE_ANGLE_DOWN + S2T_PARTICLE_ANGLE_RANGE - particle->angle) * S2T_PARTICLE_X_PER_ANGLE) + TO_SP(S2T_PARTICLE_X_DOWN_PX);
        particle->pos.cur.y.v = 0;
        vector2(particle->pos.velocity.x.v, particle->pos.velocity.y.v,
            particle->angle, TO_SP(S2T_PARTICLE_SPAWN_SPEED_PX));
        stage2_particles_spawned++;
    }
    grcg_setcolor(GC_RMW, 0);
    particle = s2particles;
    for(i = 0; i < S2PARTICLE_COUNT; i++, particle++) {
        if(particle->flag != 0) {
            // update_seg1() returns the new position as X in AX and Y in DX.
            // The original compares those registers directly; storing the
            // returned PlayfieldPoint in a local first would add stores.
            particle->pos.update_seg1();
            if(static_cast<subpixel_t>(_AX) <= -TO_SP(S2T_PARTICLE_CLIP_MARGIN_PX) ||
                static_cast<subpixel_t>(_AX) >= TO_SP(PLAYFIELD_W + S2T_PARTICLE_CLIP_MARGIN_PX) ||
                static_cast<subpixel_t>(_DX) <= -TO_SP(S2T_PARTICLE_CLIP_MARGIN_PX) ||
                static_cast<subpixel_t>(_DX) >= TO_SP(PLAYFIELD_H + S2T_PARTICLE_CLIP_MARGIN_PX)) {
                stage2_particle_init(*particle);
            } else {
                // z_super_roll_put_16x16_mono() draws into the VRAM plane
                // in ES.
                _ES = SEG_PLANE_B;

                // All particles except every fourth one grow, and the zoom
                // selects one of the four particle cels. [left] and [right]
                // are reused for the sprite number and the screen X.
                if((i & 3) != 0) {
                    particle->zoom++;
                }
                left = particle->zoom >> 4;
                if(left >= PARTICLE_CELS - 1) {
                    left = PARTICLE_CELS - 1;
                }
                left += PAT_PARTICLE;
                right = (particle->pos.cur.x.v >> 4) + PLAYFIELD_LEFT - (PARTICLE_W / 2);
                z_super_roll_put_16x16_mono(right,
                    scroll_subpixel_y_to_vram_seg1(
                        particle->pos.cur.y.v + TO_SP(PLAYFIELD_TOP - (PARTICLE_H / 2))),
                    left);
            }
        }
    }
    grcg_off();

    // Pulse color 0 between a darker and a brighter blue.
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

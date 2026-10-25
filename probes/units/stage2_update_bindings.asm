; Outside-only real context for the complete653-byte stage2_update.
; The initializer at11700 is genuinely foreign, with no body or credited gap.
; No original parent contribution, source padding, fake functions or values.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 118ech
UNIT_END equ 11b79h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_SETCOLOR, GRAPH_SCROLLUP, IRAND
org 01a88h
GRCG_SETCOLOR label far
org 01ee2h
GRAPH_SCROLLUP label far
org 023c6h
IRAND label far
org MAIN01_BASE
_TEXT ends

STAGE2_TEXT segment byte public 'CODE' use16
assume cs:STAGE2_TEXT
public @tiles_invalidate_all$qv, @PlayfieldMotion@update_seg1$qv
public Z_SUPER_ROLL_PUT_16X16_MONO_RAW, @RANDRING1_NEXT16_MOD$QUI
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0bd38h - MAIN01_BASE)
@tiles_invalidate_all$qv label near
org (0be1ah - MAIN01_BASE)
@PlayfieldMotion@update_seg1$qv label near
org (0c21eh - MAIN01_BASE)
Z_SUPER_ROLL_PUT_16X16_MONO_RAW label near
org (0c724h - MAIN01_BASE)
@RANDRING1_NEXT16_MOD$QUI label near
org (0df28h - MAIN01_BASE)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
public @STAGE2_PARTICLE_INIT$QR12S2PARTICLE_T
org (11700h - MAIN01_BASE)
@STAGE2_PARTICLE_INIT$QR12S2PARTICLE_T label near
org (UNIT_START - MAIN01_BASE)
STAGE2_TEXT ends

; The distinct byte-aligned tail begins after the sole complete owned function.
STAGE2_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
STAGE2_AFTER_TEXT ends
main_01 group STAGE2_TEXT, STAGE2_AFTER_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2
org 0008h
VECTOR2 label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends

; Address declarations only: no initialized objects are supplied by context.
_DATA segment word public 'DATA' use16
public _PaletteTone, _stage2_particles_spawned, _stage2_palette_level
public _stage2_tone_offset, _Palettes, _scroll_line, _scroll_active
public _stage2_palette_falling, _tile_ring, _stage_frame
public _stage_frame_mod2, _stage_frame_mod4, _palette_changed
public _boss, _custom_entities
org 03dah
_PaletteTone label word
org 1994h
_stage2_particles_spawned label word
org 1996h
_stage2_palette_level label byte
org 1997h
_stage2_tone_offset label byte
org 264ah
_Palettes label byte
org 3516h
_scroll_line label word
org 351ah
_scroll_active label byte
org 4a84h
_stage2_palette_falling label byte
org 511ah
_tile_ring label word
org 5764h
_stage_frame label word
org 5766h
_stage_frame_mod2 label byte
org 5767h
_stage_frame_mod4 label byte
org 576dh
_palette_changed label byte
org 5abah
_boss label byte
org 0b3f4h
_custom_entities label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

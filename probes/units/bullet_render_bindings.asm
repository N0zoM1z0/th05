; True near graphics/DS labels and gaps outside the complete334-byte renderer.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 13185h
UNIT_END equ 132d3h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
BULLET_RENDER_TEXT segment byte public 'CODE' use16
assume cs:BULLET_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW, Z_SUPER_ROLL_PUT_TINY_16X16_RAW
public @grcg_setcolor_direct_raw$qv, _pellets_render_top, _pellets_render_bottom
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0bf62h - MAIN01_BASE)
Z_SUPER_ROLL_PUT_TINY_32X32_RAW label near
org (0c07ch - MAIN01_BASE)
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
org (0c204h - MAIN01_BASE)
@grcg_setcolor_direct_raw$qv label near
org (0c322h - MAIN01_BASE)
_pellets_render_top label near
org (0c3b4h - MAIN01_BASE)
_pellets_render_bottom label near
org (0df28h - MAIN01_BASE)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (UNIT_START - MAIN01_BASE)
BULLET_RENDER_TEXT ends
BULLET_RENDER_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
BULLET_RENDER_AFTER_TEXT ends
main_01 group HUD_OVRL_TEXT, BULLET_RENDER_TEXT, BULLET_RENDER_AFTER_TEXT
BULLET_RENDER_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
BULLET_RENDER_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _bullet_zap, _bullet_clear_time, _bullets, _pellet_bottom_col
public _pellet_clouds_render, _pellet_clouds_render_count
org 3f96h
_bullet_zap label byte
org 3f97h
_bullet_clear_time label byte
org 5f2ah
_bullets label byte
org 0c33eh
_pellet_bottom_col label word
org 0c340h
_pellet_clouds_render label word
org 0c4a8h
_pellet_clouds_render_count label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

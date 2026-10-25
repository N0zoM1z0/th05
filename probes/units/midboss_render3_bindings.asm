; Real outside context for the complete127-byte stage3 midboss renderer.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 13106h
UNIT_END equ 13185h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE, SUPER_ROLL_PUT
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 02fe0h
SUPER_ROLL_PUT label far
org MAIN01_BASE
_TEXT ends
M3_RENDER_TEXT segment byte public 'CODE' use16
assume cs:M3_RENDER_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - MAIN01_BASE)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (UNIT_START - MAIN01_BASE)
M3_RENDER_TEXT ends
M3_RENDER_AFTER_TEXT segment byte public 'CODE' use16
assume cs:M3_RENDER_AFTER_TEXT
public @midboss_defeat_render$qv
org (132d3h - UNIT_END)
@midboss_defeat_render$qv label near
org (SHARED_BASE - UNIT_END)
M3_RENDER_AFTER_TEXT ends
main_01 group M3_RENDER_TEXT, M3_RENDER_AFTER_TEXT
M3_RENDER_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
M3_RENDER_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _stage_frame_mod16, _midboss
org 5769h
_stage_frame_mod16 label byte
org 5aa4h
_midboss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

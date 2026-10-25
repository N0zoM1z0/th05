; Extra callback identity comes from originalstage setup, not its stage5 twin.
; All holes are outside the complete101-byte natural source contribution.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0dd2ah
UNIT_END equ 0dd8fh
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
MX_RENDER_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN01_BASE)
MX_RENDER_TEXT ends
MX_RENDER_AFTER_TEXT segment byte public 'CODE' use16
assume cs:MX_RENDER_AFTER_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1, @midboss_defeat_render$qv
org (0df28h - UNIT_END)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (132d3h - UNIT_END)
@midboss_defeat_render$qv label near
org (SHARED_BASE - UNIT_END)
MX_RENDER_AFTER_TEXT ends
main_01 group MX_RENDER_TEXT, MX_RENDER_AFTER_TEXT
MX_RENDER_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
MX_RENDER_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _midboss
org 5aa4h
_midboss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

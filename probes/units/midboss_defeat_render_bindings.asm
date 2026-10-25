; Real foreign declarations and gaps outside the full170-byte defeat renderer.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 132d3h
UNIT_END equ 1337dh
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT
org 02fe0h
SUPER_ROLL_PUT label far
org MAIN01_BASE
_TEXT ends
MID_DEFEAT_TEXT segment byte public 'CODE' use16
assume cs:MID_DEFEAT_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0df28h - MAIN01_BASE)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (UNIT_START - MAIN01_BASE)
MID_DEFEAT_TEXT ends
MID_DEFEAT_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
MID_DEFEAT_AFTER_TEXT ends
main_01 group MID_DEFEAT_TEXT, MID_DEFEAT_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public @POLAR$QIII
org 0394h
@POLAR$QIII label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8, _midboss_defeat_angle, _midboss
org 041ch
_SinTable8 label word
org 049ch
_CosTable8 label word
org 1a60h
_midboss_defeat_angle label byte
org 5aa4h
_midboss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

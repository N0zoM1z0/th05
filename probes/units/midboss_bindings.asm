; Symbol-only context for two complete natural midboss state functions.
; All holes surround the entire 85-byte C++ contribution. No instructions,
; dummy helper bodies, target bytes or state values are supplied.
.386
.model large

MAIN01_BASE equ 0ae10h
MAIN03_BASE equ 15270h
UNIT_START equ 1c4a1h
UNIT_SIZE equ 0055h
UNIT_END equ (UNIT_START + UNIT_SIZE)
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends

MAI_TEXT segment word public 'CODE' use16
assume cs:MAI_TEXT
public NULLFUNC_NEAR, NULLFUNC_FAR, @MIDBOSS_INVALIDATE_FUNC$QV
org 192eh
NULLFUNC_NEAR label near
org 1930h
NULLFUNC_FAR label far
org 5badh
@MIDBOSS_INVALIDATE_FUNC$QV label near
org (MAIN03_BASE - MAIN01_BASE)
MAI_TEXT ends
main_01 group MAI_TEXT

MIDBOSS_TEXT segment word public 'CODE' use16
assume cs:MIDBOSS_TEXT
org (UNIT_START - MAIN03_BASE)
MIDBOSS_TEXT ends
main_03 group MIDBOSS_TEXT

MIDBOSS_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
MIDBOSS_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _stage_frame, _midboss, _midboss_active
public _midboss_invalidate, _midboss_update, _midboss_render
public _midboss_update_func, _midboss_render_func
org 5764h
_stage_frame label word
org 5aa4h
_midboss label byte
org 0c4aah
_midboss_active label byte
org 0c4ach
_midboss_invalidate label word
org 0c4aeh
_midboss_update label dword
org 0c4b2h
_midboss_render label word
org 0c4b4h
_midboss_update_func label dword
org 0c4b8h
_midboss_render_func label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

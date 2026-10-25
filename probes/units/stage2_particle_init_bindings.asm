; Whole original stage-two initializer [11700h,118ECh), no update body/context.
; Symbol-only foreign addresses and outside-owner holes; no values or stack.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 11700h
UNIT_END equ 118ech
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 023c6h
IRAND label far
org MAIN01_BASE
_TEXT ends

STAGE2_TEXT segment byte public 'CODE' use16
assume cs:STAGE2_TEXT
public @RANDRING1_NEXT16_MOD$QUI
org (0c724h - MAIN01_BASE)
@RANDRING1_NEXT16_MOD$QUI label near
org (UNIT_START - MAIN01_BASE)
STAGE2_TEXT ends

; Starts only after the one complete compiler-owned initializer.
STAGE2_INIT_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
STAGE2_INIT_AFTER_TEXT ends
main_01 group STAGE2_TEXT, STAGE2_INIT_AFTER_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2
org 0008h
VECTOR2 label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends

_DATA segment word public 'DATA' use16
public _stage_frame
org 05764h
_stage_frame label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

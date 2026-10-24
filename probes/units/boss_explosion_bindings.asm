; External symbol context for the 452-byte maintained Boss explosion unit.
; No target instructions are supplied. All origin holes are outside the sole
; credited C++ contribution; they only preserve the observed far/near bindings.
.386
.model large
.stack 80h

MASTER_TEXT_END equ 0ae10h
UNIT_START equ 1060eh
UNIT_END equ 107d2h
POLAR_SEGMENT_BASE equ 14ab0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_PUT
org 33f0h
SUPER_PUT label far
org MASTER_TEXT_END
_TEXT ends

BOSS_EXP_TEXT segment word public 'CODE' use16
assume cs:BOSS_EXP_TEXT
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW, @grcg_setmode_rmw$qv
org (0c07ch - MASTER_TEXT_END)
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
org (0c1f8h - MASTER_TEXT_END)
@grcg_setmode_rmw$qv label near
org (UNIT_START - MASTER_TEXT_END)
BOSS_EXP_TEXT ends
main_01 group BOSS_EXP_TEXT

POLAR_BINDING_GAP segment word public 'CODE' use16
org (POLAR_SEGMENT_BASE - UNIT_END)
POLAR_BINDING_GAP ends

SHARED segment word public 'CODE' use16
assume cs:SHARED
public @POLAR$QIII
org 0394h
@POLAR$QIII label far
SHARED ends

_DATA segment word public 'DATA' use16
public _PaletteTone, _SinTable8, _CosTable8
public _explosion_big_frame, _explosions_small, _explosions_big, _palette_changed
org 03dah
_PaletteTone label word
org 041ch
_SinTable8 label word
org 049ch
_CosTable8 label word
org 18e4h
_explosion_big_frame label word
org 43fch
_explosions_small label byte
org 441ch
_explosions_big label byte
org 576dh
_palette_changed label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

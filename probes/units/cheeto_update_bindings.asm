; Symbol-only context for the complete natural 592-byte Cheeto update owner.
; All ORG holes surround the whole compiler contribution. No instructions,
; target bytes, global values or dummy helper bodies are supplied or credited.
.386
.model large
.stack 80h

MAIN03_BASE equ 15270h
UNIT_START equ 1a82eh
UNIT_SIZE equ 0250h
UNIT_END equ (UNIT_START + UNIT_SIZE)
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends

FRAME_PADDING segment word public 'CODE' use16
org 0a460h
FRAME_PADDING ends

CHEETO_U_TEXT segment word public 'CODE' use16
assume cs:CHEETO_U_TEXT
public @PlayfieldMotion@update_seg3$qv, VECTOR2_NEAR
public @BULLET_PATNUM_FOR_ANGLE$QUIUC
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
org (1527ch - MAIN03_BASE)
@PlayfieldMotion@update_seg3$qv label near
org (152dah - MAIN03_BASE)
VECTOR2_NEAR label near
org (16f52h - MAIN03_BASE)
@BULLET_PATNUM_FOR_ANGLE$QUIUC label near
org (171cch - MAIN03_BASE)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (UNIT_START - MAIN03_BASE)
CHEETO_U_TEXT ends
main_03 group CHEETO_U_TEXT

; This independent byte-aligned CODE segment starts after both entire C++
; functions. Its uncredited extent preserves the observed DS group frame.
CHEETO_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
CHEETO_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _player_pos, _player_is_hit, _stage_frame_mod2
public _custom_entities, _cheeto_trails
org 36d2h
_player_pos label byte
org 36f3h
_player_is_hit label byte
org 5766h
_stage_frame_mod2 label byte
org 0b3f4h
_custom_entities label byte
org 0c0aah
_cheeto_trails label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

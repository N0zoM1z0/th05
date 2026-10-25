; Address declarations only; all gaps outside the complete308-byte C++ owner.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 11b79h
UNIT_END equ 11cadh
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BYTEBOXFILL_X
org 0f76h
GRCG_BYTEBOXFILL_X label far
org MAIN01_BASE
_TEXT ends
EX_CUSTOM_TEXT segment byte public 'CODE' use16
assume cs:EX_CUSTOM_TEXT
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW
org (0c07ch - MAIN01_BASE)
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
org (UNIT_START - MAIN01_BASE)
EX_CUSTOM_TEXT ends
EX_CUSTOM_AFTER_TEXT segment byte public 'CODE' use16
assume cs:EX_CUSTOM_AFTER_TEXT
public @CHEETOS_RENDER$QV
org (12f2bh - UNIT_END)
@CHEETOS_RENDER$QV label near
org (SHARED_BASE - UNIT_END)
EX_CUSTOM_AFTER_TEXT ends
main_01 group EX_CUSTOM_TEXT, EX_CUSTOM_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public @POLAR$QIII
org 0394h
@POLAR$QIII label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends
_DATA segment word public 'DATA' use16
public _SinTable8, _player_pos, _player_is_hit, _firewaves
org 041ch
_SinTable8 label word
org 36d2h
_player_pos label byte
org 36f3h
_player_is_hit label byte
org 4a90h
_firewaves label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

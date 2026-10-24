; Original address-only bomb animation context. No bodies/state/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 0ae10h
_TEXT ends
BOMBANIM_TEXT segment word public 'CODE' use16
assume cs:BOMBANIM_TEXT
public @RANDRING1_NEXT16_AND$QUI
org 018feh
@RANDRING1_NEXT16_AND$QUI label near
public @RANDRING1_NEXT16_MOD$QUI
org 01914h
@RANDRING1_NEXT16_MOD$QUI label near
public @CIRCLES_ADD_GROWING$QII
org 0347ah
@CIRCLES_ADD_GROWING$QII label far
org 04d34h
BOMBANIM_TEXT ends
BOMBANIM_MAIN01_TAIL segment byte public 'CODE' use16
org 04d99h
BOMBANIM_MAIN01_TAIL ends
main_01 group BOMBANIM_TEXT, BOMBANIM_MAIN01_TAIL
BOMBANIM_SHARED segment para public 'CODE' use16
assume cs:BOMBANIM_SHARED
public VECTOR2
org 08h
VECTOR2 label far
org 07c0h
BOMBANIM_SHARED ends
BOMBANIM_MAIN03 segment byte public 'CODE' use16
org 0b760h
BOMBANIM_MAIN03 ends
main_03 group BOMBANIM_MAIN03
_DATA segment word public 'DATA' use16
public _bomb_frame
org 04207h
_bomb_frame label byte
public _bomb_anim
org 0420eh
_bomb_anim label byte
public _stage_frame_mod8
org 05768h
_stage_frame_mod8 label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

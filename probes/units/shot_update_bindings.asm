; Foreign symbol context around the complete408-byte shot update/table extent.
.386
.model large
UNIT_START equ 133dbh
UNIT_END equ 13573h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01f3ah
IATAN2 label far
org 0ae10h
_TEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
SHOT_HIT_TEXT ends
SHOT_RUNTIME_MAIN01_CONTEXT segment byte public 'CODE' use16
assume cs:SHOT_RUNTIME_MAIN01_CONTEXT
public @PlayfieldMotion@update_seg1$qv
org (0be1ah - 0ae10h)
@PlayfieldMotion@update_seg1$qv label near
public @SHOT_VELOCITY_SET$QP7SPPOINTUC
org (0e3c4h - 0ae10h)
@SHOT_VELOCITY_SET$QP7SPPOINTUC label near
org (UNIT_START - 0ae10h)
SHOT_RUNTIME_MAIN01_CONTEXT ends
SHOT_UPDATE_TEXT segment byte public 'CODE' use16
SHOT_UPDATE_TEXT ends
SHOT_UPDATE_TAIL segment byte public 'CODE' use16
org (14ab0h - UNIT_END)
SHOT_UPDATE_TAIL ends
main_01 group SHOT_HIT_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_UPDATE_TEXT, SHOT_UPDATE_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
SHOT_RUNTIME_MAIN03_CONTEXT ends
main_03 group SHOT_RUNTIME_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _homing_target
org 03f8ah
_homing_target label byte
public _shots
org 0ba8eh
_shots label byte
public _hitshots
org 0bf56h
_hitshots label byte
public _shots_alive
org 0c4c8h
_shots_alive label byte
public _shots_alive_count
org 0c648h
_shots_alive_count label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

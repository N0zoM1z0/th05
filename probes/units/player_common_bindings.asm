; True TH05 common-shot symbol context. No helper instructions, initializer
; bytes, stack, or inside-unit padding. All holes remain outside the183-byte TU.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0e644h
UNIT_END equ 0e6fbh
SHARED_BASE equ 14ab0h
SHARED_END equ (SHARED_BASE + 0232h)
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
assume cs:MAIN_01_TEXT
public @RANDRING1_NEXT16_AND$QUI, @shots_add$qv, @SHOT_VELOCITY_SET$QP7SPPOINTUC
org (0c70eh - MAIN01_BASE)
@RANDRING1_NEXT16_AND$QUI label near
org (0e38ch - MAIN01_BASE)
@shots_add$qv label near
org (0e3c4h - MAIN01_BASE)
@SHOT_VELOCITY_SET$QP7SPPOINTUC label near
org (UNIT_START - MAIN01_BASE)
MAIN_01_TEXT ends
main_01 group MAIN_01_TEXT
PLAYER_COMMON_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
PLAYER_COMMON_SHARED_GAP ends
PLAYER_COMMON_SHARED segment para public 'CODE' use16
assume cs:PLAYER_COMMON_SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
PLAYER_COMMON_SHARED ends
PLAYER_COMMON_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
PLAYER_COMMON_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _shot_time, _shot_ptr, _shot_last_id, _shots
org 036f2h
_shot_time label byte
org 04200h
_shot_ptr label word
org 04202h
_shot_last_id label byte
org 0ba8eh
_shots label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

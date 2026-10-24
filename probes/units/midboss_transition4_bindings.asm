; Actual foreign context only; no owned instructions, values or stack.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 15f74h
UNIT_END equ 16044h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
M4TRANS_MAIN01_CONTEXT segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
M4TRANS_MAIN01_CONTEXT ends
main_01 group M4TRANS_MAIN01_CONTEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @RANDRING2_NEXT16_MOD$QUI
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends
M4TRANS_AFTER_TEXT segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
M4TRANS_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, M4TRANS_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _midboss4_transition_center_x, _stage_frame_mod2, _midboss, _boss_statebyte
org 372ah
_midboss4_transition_center_x label word
org 5766h
_stage_frame_mod2 label byte
org 5aa4h
_midboss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

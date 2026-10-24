; Foreign symbols and holes outside the complete556-byte five-callback owner.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1e209h
AFTER_BASE equ 1e440h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
MAIN_01_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:CIRCLE_TEXT
public @CIRCLES_ADD_SHRINKING$QII
org 034c6h
@CIRCLES_ADD_SHRINKING$QII label far
org (SHARED_BASE - MAIN01_BASE)
CIRCLE_TEXT ends
main_01 group MAIN_01_TEXT, CIRCLE_TEXT
SHARED segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @randring2_next16$qv, _bullets_add_regular
org (1529ch - MAIN03_BASE)
@randring2_next16$qv label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends
ALICE_PUP_TEXT segment byte public 'CODE' use16
ALICE_PUP_TEXT ends
ALICE_PUP_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
ALICE_PUP_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_PUP_TEXT, ALICE_PUP_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _bullet_template_tune, _stage_frame, _stage_frame_mod2, _bullet_template
org 41deh
_bullet_template_tune label word
org 5764h
_stage_frame label word
org 5766h
_stage_frame_mod2 label byte
org 577eh
_bullet_template label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

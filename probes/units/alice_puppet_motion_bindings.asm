; Real foreign contexts, with no supplied instructions or initialized values.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1df86h
AFTER_BASE equ 1e210h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
assume cs:MAIN_01_TEXT
public @shots_hittest$qv
org 08873h
@shots_hittest$qv label far
org (SHARED_BASE - MAIN01_BASE)
MAIN_01_TEXT ends
main_01 group MAIN_01_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY, @POLAR$QIII
org 0232h
SND_SE_PLAY label far
org 0394h
@POLAR$QIII label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI
org (152aah - MAIN03_BASE)
@RANDRING2_NEXT16_AND$QUI label near
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends
ALICE_PMV_TEXT segment byte public 'CODE' use16
ALICE_PMV_TEXT ends
ALICE_PMV_AFTER_TEXT segment para public 'CODE' use16
assume cs:ALICE_PMV_AFTER_TEXT
public @ALICE_PUPPET_RECOVER$QR11ALICEPUPPET
org (1e435h - AFTER_BASE)
@ALICE_PUPPET_RECOVER$QR11ALICEPUPPET label near
org (DGROUP_BASE - AFTER_BASE)
ALICE_PMV_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_PMV_TEXT, ALICE_PMV_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _SinTable8, _CosTable8, _alice_puppet_pattern_table
public _player_pos, _player_is_hit, _score_delta, _boss, _custom_entities
public _shot_hitbox_center, _shot_hitbox_radius
public _alice_puppet_pattern0, _alice_puppet_pattern1, _boss_statebyte
org 041ch
_SinTable8 label word
org 049ch
_CosTable8 label word
org 1f7eh
_alice_puppet_pattern_table label word
org 36d2h
_player_pos label byte
org 36f3h
_player_is_hit label byte
org 3712h
_score_delta label dword
org 5abah
_boss label byte
org 0b3f4h
_custom_entities label byte
org 0c4c0h
_shot_hitbox_center label byte
org 0c4c4h
_shot_hitbox_radius label byte
org 0c666h
_alice_puppet_pattern0 label word
org 0c668h
_alice_puppet_pattern1 label word
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

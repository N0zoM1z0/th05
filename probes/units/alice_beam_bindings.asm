; Symbol-only context for one complete natural Alice puppet-beam algorithm.
; No instructions, initialized state, asset values, stack or inner holes.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1e602h
AFTER_BASE equ 1e770h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
assume cs:MAIN_01_TEXT
public @shots_hittest_laser$qv
org 08a02h
@shots_hittest_laser$qv label far
org (SHARED_BASE - MAIN01_BASE)
MAIN_01_TEXT ends
main_01 group MAIN_01_TEXT

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (MAIN03_BASE - SHARED_BASE)
SHARED ends

B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public _bullets_add_regular
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends

ALICE_BEAM_AFTER_TEXT segment para public 'CODE' use16
org (DGROUP_BASE - AFTER_BASE)
ALICE_BEAM_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_BEAM_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _player_is_hit, _bullet_template_tune
public _bullet_template, _boss, _custom_entities
public _shot_hitbox_center, _shot_hitbox_radius
public _alice_beam_frame, _alice_beam_burst_window, _boss_statebyte
org 36d2h
_player_pos label byte
org 36f3h
_player_is_hit label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 0b3f4h
_custom_entities label byte
org 0c4c0h
_shot_hitbox_center label byte
org 0c4c4h
_shot_hitbox_radius label byte
org 0c66ah
_alice_beam_frame label word
org 0c66ch
_alice_beam_burst_window label word
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

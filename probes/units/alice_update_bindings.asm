; Real outside-contribution context for final spread and Alice's full callback.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1e957h
AFTER_BASE equ 1ed50h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
MAIN_01_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
assume cs:BOSS_BG_TEXT
public @ALICE_BG_RENDER$QV
org 05cfbh
@ALICE_BG_RENDER$QV label near
org (SHARED_BASE - MAIN01_BASE)
BOSS_BG_TEXT ends
main_01 group MAIN_01_TEXT, BOSS_BG_TEXT

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
public @BOSS_FLYSTEP_RANDOM$QI, @BOSS_FLYSTEP_TOWARDS$QII
public _bullets_add_regular
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
public @HUD_HP_UPDATE_AND_RENDER$QII, @BOSS_SCORE_BONUS$QUI
public @alice_puppets_entrance$qv, @alice_puppets_update$qv
public @ALICE_PUPPET_INITIAL$QR11ALICEPUPPET
public @ALICE_PUPPET_SPREAD$QR11ALICEPUPPET
public @ALICE_PUPPET_RINGS$QR11ALICEPUPPET
public @ALICE_PUPPET_HOLD$QR11ALICEPUPPET
public @alice_pattern_opening$qv, @alice_puppet_beam_pattern$qv
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (15914h - MAIN03_BASE)
@BOSS_FLYSTEP_RANDOM$QI label near
org (15a07h - MAIN03_BASE)
@BOSS_FLYSTEP_TOWARDS$QII label near
org (17204h - MAIN03_BASE)
_bullets_add_regular label near
org (176ddh - MAIN03_BASE)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (1c4f6h - MAIN03_BASE)
@HUD_HP_UPDATE_AND_RENDER$QII label near
org (1c5b8h - MAIN03_BASE)
@BOSS_SCORE_BONUS$QUI label near
org (1df86h - MAIN03_BASE)
@alice_puppets_entrance$qv label near
org (1e025h - MAIN03_BASE)
@alice_puppets_update$qv label near
org (1e209h - MAIN03_BASE)
@ALICE_PUPPET_INITIAL$QR11ALICEPUPPET label near
org (1e27ah - MAIN03_BASE)
@ALICE_PUPPET_SPREAD$QR11ALICEPUPPET label near
org (1e3d6h - MAIN03_BASE)
@ALICE_PUPPET_RINGS$QR11ALICEPUPPET label near
org (1e44dh - MAIN03_BASE)
@ALICE_PUPPET_HOLD$QR11ALICEPUPPET label near
org (1e456h - MAIN03_BASE)
@alice_pattern_opening$qv label near
org (1e602h - MAIN03_BASE)
@alice_puppet_beam_pattern$qv label near
org (UNIT_START - MAIN03_BASE)
B4_UPDATE_TEXT ends

ALICE_UPDATE_AFTER_TEXT segment para public 'CODE' use16
assume cs:ALICE_UPDATE_AFTER_TEXT
public @boss_hittest_shots$qv, @boss_hittest_shots_invincible$qv
public @boss_items_drop$qv, @BOSS_DEFEAT_UPDATE$QUI
org (1fad0h - AFTER_BASE)
@boss_hittest_shots$qv label near
org (1fafah - AFTER_BASE)
@boss_hittest_shots_invincible$qv label near
org (1fb0ch - AFTER_BASE)
@boss_items_drop$qv label near
org (1fbb1h - AFTER_BASE)
@BOSS_DEFEAT_UPDATE$QUI label near
org (DGROUP_BASE - AFTER_BASE)
ALICE_UPDATE_AFTER_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_UPDATE_AFTER_TEXT

_DATA segment word public 'DATA' use16
public _alice_pattern_table, _bg_render_bombing_func, _homing_target
public _bullet_clear_time, _bullet_template_tune, _bullet_template
public _boss, _gather_template, _custom_entities
public _alice_puppet_pattern0, _alice_puppet_pattern1
public _alice_beam_frame, _alice_beam_burst_window, _alice_pattern_current
public _boss_statebyte
org 1f86h
_alice_pattern_table label word
org 350ah
_bg_render_bombing_func label word
org 3f8ah
_homing_target label byte
org 3f97h
_bullet_clear_time label byte
org 41deh
_bullet_template_tune label word
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
org 9ea6h
_gather_template label byte
org 0b3f4h
_custom_entities label byte
org 0c666h
_alice_puppet_pattern0 label word
org 0c668h
_alice_puppet_pattern1 label word
org 0c66ah
_alice_beam_frame label word
org 0c66ch
_alice_beam_burst_window label word
org 0c66eh
_alice_pattern_current label word
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

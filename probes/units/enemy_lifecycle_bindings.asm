; Address-only foreign context; no code/data payload, no stack allocation.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
ENEMY_MAIN01_CONTEXT segment byte public 'CODE' use16
assume cs:ENEMY_MAIN01_CONTEXT
public NULLFUNC_FAR
org 01930h
NULLFUNC_FAR label far
public HUD_DREAM_PUT
org 023bdh
HUD_DREAM_PUT label far
public @shots_hittest$qv
org 08873h
@shots_hittest$qv label far
org 09ca0h
ENEMY_MAIN01_CONTEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
HUD_OVRL_TEXT ends
main_01 group ENEMY_MAIN01_CONTEXT, HUD_OVRL_TEXT
ENEMY_SHARED_CONTEXT segment para public 'CODE' use16
assume cs:ENEMY_SHARED_CONTEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
ENEMY_SHARED_CONTEXT ends
ENEMY_SHARED_TAIL segment byte public 'CODE' use16
assume cs:ENEMY_SHARED_TAIL
org 0058eh
ENEMY_SHARED_TAIL ends
MIDBOSS_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSS_TEXT
MIDBOSS_TEXT ends
ENEMY_SPAWN_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_SPAWN_TEXT
public @PlayfieldMotion@update_seg3$qv
org 0ch
@PlayfieldMotion@update_seg3$qv label near
public @randring2_next16$qv
org 02ch
@randring2_next16$qv label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public _enemy_script_update
org 0184h
_enemy_script_update label near
org 0180ah
ENEMY_SPAWN_TEXT ends
ENEMY_TEMPLATE_FOREIGN segment byte public 'CODE' use16
assume cs:ENEMY_TEMPLATE_FOREIGN
public ENEMY_BULLET_TEMPLATE_PUSH
org 00h
ENEMY_BULLET_TEMPLATE_PUSH label near
org 018h
ENEMY_TEMPLATE_FOREIGN ends
ENEMY_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_UPDATE_TEXT
ENEMY_UPDATE_TEXT ends
ENEMY_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ENEMY_MAIN03_TAIL
public @SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II
org 05fh
@SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II label far
public _bullets_add_regular
org 03ddh
_bullets_add_regular label near
public @midboss_activate_if_stage_frame_$qv
org 0569dh
@midboss_activate_if_stage_frame_$qv label far
public @ITEMS_ADD$QII11ITEM_TYPE_T
org 05e04h
@ITEMS_ADD$QII11ITEM_TYPE_T label near
org 09ba9h
ENEMY_MAIN03_TAIL ends
main_03 group MIDBOSS_TEXT, ENEMY_SPAWN_TEXT, ENEMY_TEMPLATE_FOREIGN, ENEMY_UPDATE_TEXT, ENEMY_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _enemies_gone
org 014a4h
_enemies_gone label byte
public _enemies_killed
org 014a6h
_enemies_killed label byte
public _std_enemy_scripts
org 0362ah
_std_enemy_scripts label byte
public _std_ip
org 0366ah
_std_ip label byte
public _player_pos
org 036d2h
_player_pos label byte
public _player_is_hit
org 036f3h
_player_is_hit label byte
public _dream
org 036f6h
_dream label byte
public _score_delta
org 03712h
_score_delta label byte
public _homing_target
org 03f8ah
_homing_target label byte
public _stage_vm
org 03f8eh
_stage_vm label byte
public _enemy_cur
org 03f92h
_enemy_cur label byte
public _bullet_template_tune
org 041deh
_bullet_template_tune label byte
public _stage_frame
org 05764h
_stage_frame label byte
public _stage_id
org 0576eh
_stage_id label byte
public _rank
org 0576fh
_rank label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _enemies
org 093fah
_enemies label byte
public _midboss_active
org 0c4aah
_midboss_active label byte
public _shot_hitbox_center
org 0c4c0h
_shot_hitbox_center label byte
public _shot_hitbox_radius
org 0c4c4h
_shot_hitbox_radius label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

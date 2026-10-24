; Genuine external code/data context for the complete609-byte collision pair.
; No helper implementations, owned bytes, DATA values or stack allocation.
.386
.model large
UNIT_START equ 13683h
UNIT_END equ 138e4h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_UPDATE_TEXT segment byte public 'CODE' use16
SHOT_UPDATE_TEXT ends
SHOT_RUNTIME_MAIN01_CONTEXT segment byte public 'CODE' use16
assume cs:SHOT_RUNTIME_MAIN01_CONTEXT
public @randring1_next16$qv
org (0c700h - 0ae10h)
@randring1_next16$qv label near
public @SELECT_FOR_PLAYCHAR$QIIII
org (0cfach - 0ae10h)
@SELECT_FOR_PLAYCHAR$QIIII label far
public HITSHOT_FROM
org (13617h - 0ae10h)
HITSHOT_FROM label near
org (UNIT_START - 0ae10h)
SHOT_RUNTIME_MAIN01_CONTEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
SHOT_HIT_TEXT ends
SHOT_COLLISION_TAIL segment byte public 'CODE' use16
org (14ab0h - UNIT_END)
SHOT_COLLISION_TAIL ends
main_01 group SHOT_UPDATE_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_HIT_TEXT, SHOT_COLLISION_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:SHOT_RUNTIME_MAIN03_CONTEXT
public @SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II
org (16e86h - 15270h)
@SPARKS_ADD_RANDOM$Q20%SUBPIXELBASE$TI$TI%T1II label far
public _bullets_add_regular_far
org (1758ah - 15270h)
_bullets_add_regular_far label far
org (209d0h - 15270h)
SHOT_RUNTIME_MAIN03_CONTEXT ends
main_03 group SHOT_RUNTIME_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _shots_hittest_against_boss
org 01dc0h
_shots_hittest_against_boss label byte
public _player_pos
org 036d2h
_player_pos label byte
public _score_delta
org 03712h
_score_delta label dword
public _bombing, _bomb_frame
org 04206h
_bombing label byte
org 04207h
_bomb_frame label byte
public _stage_frame_mod4
org 05767h
_stage_frame_mod4 label byte
public _stage_id, _rank, _playchar
org 0576eh
_stage_id label byte
org 0576fh
_rank label byte
org 05773h
_playchar label byte
public _bullet_template
org 0577eh
_bullet_template label byte
public _shot_hitbox_center, _shot_hitbox_radius, _shots_alive
org 0c4c0h
_shot_hitbox_center label byte
org 0c4c4h
_shot_hitbox_radius label byte
org 0c4c8h
_shots_alive label byte
public _shots_alive_count, _shot_hit_spark_cycle
org 0c648h
_shots_alive_count label word
org 0c64eh
_shot_hit_spark_cycle label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

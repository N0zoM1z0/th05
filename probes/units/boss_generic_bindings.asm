; Symbol-only original TH05 generic boss context. No .stack or helper bodies.
; Source owns three natural CODE contributions and DATA10; ORG holes lie outside them.
.386
.model large

MAIN01_BASE equ 0AE10h
SHARED_BASE equ 14AB0h
MAIN03_BASE equ 15270h
UNIT_START equ 1FA51h
IFNDEF GENERIC_BOSS_CODE_SIZE
GENERIC_BOSS_CODE_SIZE equ 0160h
ENDIF
UNIT_END equ (UNIT_START + GENERIC_BOSS_CODE_SIZE)
DGROUP_BASE equ 209D0h
OWNED_DATA_START equ 01FBEh
IFNDEF GENERIC_BOSS_DATA_SIZE
GENERIC_BOSS_DATA_SIZE equ 0Ah
ENDIF
OWNED_DATA_END equ (OWNED_DATA_START + GENERIC_BOSS_DATA_SIZE)

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends

GENERIC_BOSS_MAIN01_TEXT segment word public 'CODE' use16
assume cs:GENERIC_BOSS_MAIN01_TEXT
public @TILES_RENDER_ALL$QV
org 0DDCh
@TILES_RENDER_ALL$QV label near
public NULLFUNC_NEAR
org 0192Eh
NULLFUNC_NEAR label near
public @end_game$qv
org 0290Eh
@end_game$qv label far
public @end_extra$qv
org 02946h
@end_extra$qv label far
public @OVERLAY_STAGE_LEAVE_UPDATE_AND_R$QV
org 07020h
@OVERLAY_STAGE_LEAVE_UPDATE_AND_R$QV label near
public @shots_hittest$qv
org 08873h
@shots_hittest$qv label far
public @dialog_animate$qv
org 09048h
@dialog_animate$qv label far
GENERIC_BOSS_MAIN01_TEXT ends
main_01 group GENERIC_BOSS_MAIN01_TEXT

GENERIC_BOSS_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - (MAIN01_BASE + 09048h))
GENERIC_BOSS_SHARED_GAP ends

GENERIC_BOSS_SHARED_TEXT segment word public 'CODE' use16
assume cs:GENERIC_BOSS_SHARED_TEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
public SND_KAJA_INTERRUPT
org 04ACh
SND_KAJA_INTERRUPT label far
public @FRAME_DELAY$QI
org 0652h
@FRAME_DELAY$QI label far
GENERIC_BOSS_SHARED_TEXT ends

GENERIC_BOSS_MAIN03_GAP segment byte public 'CODE' use16
org (MAIN03_BASE - (SHARED_BASE + 0652h))
GENERIC_BOSS_MAIN03_GAP ends

BOSS_TEXT segment word public 'CODE' use16
assume cs:BOSS_TEXT
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org 0246Dh
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
public @boss_explode_big_circle$qv
org 0251Bh
@boss_explode_big_circle$qv label near
public @BOSS_SCORE_BONUS$QUI
org 07348h
@BOSS_SCORE_BONUS$QUI label near
public @stage_clear_bonus$qv
org 0752Ah
@stage_clear_bonus$qv label near
public @stage_allclear_bonus$qv
org 0775Bh
@stage_allclear_bonus$qv label near
public @ITEMS_ADD$QII11ITEM_TYPE_T
org 079BBh
@ITEMS_ADD$QII11ITEM_TYPE_T label near
org (UNIT_START - MAIN03_BASE)
BOSS_TEXT ends

; The real natural defeat function occupies its own complete contribution.
BOSS_DEFEAT_TEXT segment byte public 'CODE' use16
BOSS_DEFEAT_TEXT ends

; Six uncredited bytes follow the actual 408-byte defeat contribution and
; precede the whole 46-byte natural collision function. Both remain unaccepted.
; The first six accepted functions end before either function or this hole.
BOSS_COLLISION_TEXT segment byte public 'CODE' use16
org 6
BOSS_COLLISION_TEXT ends
main_03 group BOSS_TEXT, BOSS_DEFEAT_TEXT, BOSS_COLLISION_TEXT

; Paragraph alignment is outside the entire actual compiler contribution.
; The split actual end1FD7D and original end1FD7A both round to1FD80.
; A diagnostic must reject a compiler end beyond1FD80; no function is padded.
GENERIC_BOSS_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 1FD80h)
GENERIC_BOSS_DGROUP_GAP ends

; Source compiler DATA is the real ten-byte local item-drop table.
_DATA segment word public 'DATA' use16
public _PaletteTone
org 03DAh
_PaletteTone label word
public _shots_hittest_against_boss
org 01DC0h
_shots_hittest_against_boss label byte
org OWNED_DATA_START
_DATA ends

; These genuine foreign runtime objects follow the complete source DATA.
; No source BSS belongs to this TU. The stage-owned timed-out flag is a label.
_BSS segment word public 'BSS' use16
public _boss_phase_timed_out
org (01FC8h - OWNED_DATA_END)
_boss_phase_timed_out label byte
public _bg_render_bombing_func
org (0350Ah - OWNED_DATA_END)
_bg_render_bombing_func label word
public _playfield_shake_x
org (0351Ch - OWNED_DATA_END)
_playfield_shake_x label word
public _playfield_shake_y
org (0351Eh - OWNED_DATA_END)
_playfield_shake_y label word
public _player_pos
org (036D2h - OWNED_DATA_END)
_player_pos label byte
public _player_invincibility_time
org (036EEh - OWNED_DATA_END)
_player_invincibility_time label byte
public _power
org (036F0h - OWNED_DATA_END)
_power label byte
public _player_is_hit
org (036F3h - OWNED_DATA_END)
_player_is_hit label byte
public _score
org (03702h - OWNED_DATA_END)
_score label byte
public _homing_target
org (03F8Ah - OWNED_DATA_END)
_homing_target label dword
public _bullet_zap
org (03F96h - OWNED_DATA_END)
_bullet_zap label byte
public _bullet_clear_time
org (03F97h - OWNED_DATA_END)
_bullet_clear_time label byte
public _stage_graze
org (03F98h - OWNED_DATA_END)
_stage_graze label word
public _resident
org (041FCh - OWNED_DATA_END)
_resident label dword
public _overlay1
org (04ABEh - OWNED_DATA_END)
_overlay1 label word
public _stage_frame_mod2
org (05766h - OWNED_DATA_END)
_stage_frame_mod2 label byte
public _stage_frame_mod4
org (05767h - OWNED_DATA_END)
_stage_frame_mod4 label byte
public _slowdown_factor
org (0576Ah - OWNED_DATA_END)
_slowdown_factor label word
public _quit
org (0576Ch - OWNED_DATA_END)
_quit label byte
public _palette_changed
org (0576Dh - OWNED_DATA_END)
_palette_changed label byte
public _stage_id
org (0576Eh - OWNED_DATA_END)
_stage_id label byte
public _midboss
org (05AA4h - OWNED_DATA_END)
_midboss label byte
public _boss
org (05ABAh - OWNED_DATA_END)
_boss label byte
public _bombing_disabled
org (0C4BAh - OWNED_DATA_END)
_bombing_disabled label byte
public _shot_hitbox_center
org (0C4C0h - OWNED_DATA_END)
_shot_hitbox_center label dword
public _shot_hitbox_radius
org (0C4C4h - OWNED_DATA_END)
_shot_hitbox_radius label dword
public _boss_fg_render
org (0C676h - OWNED_DATA_END)
_boss_fg_render label word
public _boss_hitbox_radius
org (0C694h - OWNED_DATA_END)
_boss_hitbox_radius label dword
_BSS ends
DGROUP group _DATA, _BSS
end

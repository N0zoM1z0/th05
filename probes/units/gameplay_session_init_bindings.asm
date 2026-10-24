; Outside-only original context for the complete natural new-game initializer.
; No helper body, callback/asset value, stack or inside-owner alignment filler.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SESSION_INIT_TEXT segment byte public 'CODE' use16
assume cs:SESSION_INIT_TEXT
org (0b063h - 0ae10h)
SESSION_INIT_TEXT ends
SESSION_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:SESSION_MAIN01_TEXT
public @hiscore_load$qv
org 0176dh
@hiscore_load$qv label near
public @score_reset$qv
org 01d8fh
@score_reset$qv label near
public BB_TXT_LOAD
org 0327fh
BB_TXT_LOAD label near
public @BOMB_REIMU$QV
org 04b34h
@BOMB_REIMU$QV label near
public @BOMB_MARISA$QV
org 04d80h
@BOMB_MARISA$QV label near
public @BOMB_MIMA$QV
org 04fa3h
@BOMB_MIMA$QV label near
public @BOMB_YUUKA$QV
org 0513ah
@BOMB_YUUKA$QV label near
org (14ab0h - 0b237h)
SESSION_MAIN01_TEXT ends
main_01 group SESSION_INIT_TEXT, SESSION_MAIN01_TEXT
SESSION_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SESSION_SHARED_SPACE ends
BULLET_A_TEXT segment byte public 'CODE' use16
assume cs:BULLET_A_TEXT
public BULLET_TEMPLATE_TUNE_EASY
org 0242ch
BULLET_TEMPLATE_TUNE_EASY label near
public BULLET_TEMPLATE_TUNE_NORMAL
org 02434h
BULLET_TEMPLATE_TUNE_NORMAL label near
public BULLET_TEMPLATE_TUNE_HARD
org 02438h
BULLET_TEMPLATE_TUNE_HARD label near
public BULLET_TEMPLATE_TUNE_LUNATIC
org 02440h
BULLET_TEMPLATE_TUNE_LUNATIC label near
org (209d0h - 15270h)
BULLET_A_TEXT ends
main_03 group BULLET_A_TEXT
_DATA segment word public 'DATA' use16
public _SHOT_FUNCS
org 01d70h
_SHOT_FUNCS label byte
public _playchar_speed_aligned
org 036deh
_playchar_speed_aligned label word
public _playchar_speed_diagonal
org 036e2h
_playchar_speed_diagonal label word
public _power
org 036f0h
_power label byte
public _dream
org 036f6h
_dream label byte
public _score
org 03702h
_score label byte
public _graze_score
org 03f9ah
_graze_score label word
public _bullet_template_tune
org 041deh
_bullet_template_tune label word
public _resident
org 041fch
_resident label dword
public _playchar_bomb_func
org 04208h
_playchar_bomb_func label word
public _lives
org 04ad4h
_lives label byte
public _bombs
org 04ad5h
_bombs label byte
public _stage_id
org 0576eh
_stage_id label byte
public _rank
org 0576fh
_rank label byte
public _playperf
org 05770h
_playperf label byte
public _playperf_max
org 05771h
_playperf_max label byte
public _playperf_min
org 05772h
_playperf_min label byte
public _playchar
org 05773h
_playchar label byte
public _turbo_mode
org 05776h
_turbo_mode label byte
public _playchar_shot_funcs
org 0c4beh
_playchar_shot_funcs label word
public _item_point_score_at_full_dream
org 0c652h
_item_point_score_at_full_dream label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

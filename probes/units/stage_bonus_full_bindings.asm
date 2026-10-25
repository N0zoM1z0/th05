; Real outside context for the complete1445-byte natural four-function family.
; No omitted function/padding/data bytes are provided by this binder.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1c669h
UNIT_END equ 1cc0eh
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA, PALETTE_SHOW, TEXT_PUTSA
org 01dbeh
GAIJI_PUTSA label far
org 02158h
PALETTE_SHOW label far
org 02598h
TEXT_PUTSA label far
org MAIN01_BASE
_TEXT ends
BONUS_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:BONUS_MAIN01_TEXT
public PLAYPERF_RAISE, PLAYPERF_LOWER
org 216ah
PLAYPERF_RAISE label far
org 2184h
PLAYPERF_LOWER label far
org (SHARED_BASE - MAIN01_BASE)
BONUS_MAIN01_TEXT ends
main_01 group BONUS_MAIN01_TEXT
BONUS_FULL_SHARED_GAP segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
BONUS_FULL_SHARED_GAP ends
BONUS_HELP_TEXT segment byte public 'CODE' use16
assume cs:BONUS_HELP_TEXT
public @HUD_5_DIGIT_PUT$QUIUIUIUI, @HUD_POINTS_PUT$QUIUIUL
org (158aah - MAIN03_BASE)
@HUD_5_DIGIT_PUT$QUIUIUIUI label far
org (158c4h - MAIN03_BASE)
@HUD_POINTS_PUT$QUIUIUL label far
org (UNIT_START - MAIN03_BASE)
BONUS_HELP_TEXT ends
BONUS_FULL_AFTER_TEXT segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
BONUS_FULL_AFTER_TEXT ends
main_03 group BONUS_HELP_TEXT, BONUS_FULL_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _PaletteTone, _extends_gained, _bonus_previous_miss_count
public _bonus_previous_bomb_count, _STAGE_CLEAR_BONUS_DESC
public _BONUS_STAGE, _BONUS_DREAM, _GRAZEX50, _POINT_ITEMS
public _BONUS_NOMISS, _BONUS_NOBOMB, _BONUS_TOTAL, _ALL_CLEAR
public _PLAYER_REM, _POINT_TOTAL, _gpCLEAR_BONUS, _gpCONGRATULATION
public _extend_point_items_collected, _stage_point_items_collected, _dream
public _continues_used, _score_delta, _stage_graze, _resident, _lives
public _stage_id, _rank, _boss
org 03dah
_PaletteTone label word
org 1372h
_extends_gained label byte
org 1a62h
_bonus_previous_miss_count label byte
org 1a63h
_bonus_previous_bomb_count label byte
org 1a64h
_STAGE_CLEAR_BONUS_DESC label word
org 1a7ah
_BONUS_STAGE label word
org 1a7ch
_BONUS_DREAM label word
org 1a7eh
_GRAZEX50 label word
org 1a80h
_POINT_ITEMS label word
org 1a82h
_BONUS_NOMISS label word
org 1a84h
_BONUS_NOBOMB label word
org 1a86h
_BONUS_TOTAL label word
org 1a88h
_ALL_CLEAR label word
org 1a8ah
_PLAYER_REM label word
org 1a8ch
_POINT_TOTAL label word
org 1a8eh
_gpCLEAR_BONUS label byte
org 1a97h
_gpCONGRATULATION label byte
org 1e7eh
_extend_point_items_collected label word
org 36f5h
_stage_point_items_collected label byte
org 36f6h
_dream label byte
org 3702h
_continues_used label byte
org 3712h
_score_delta label dword
org 3f98h
_stage_graze label word
org 41fch
_resident label dword
org 4ad4h
_lives label byte
org 576eh
_stage_id label byte
org 576fh
_rank label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

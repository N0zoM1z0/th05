; Symbol-only linker context for bounded C++ unit replay. No instructions or
; copied target payloads are supplied. ORG holes are outside every credited
; source contribution and are never counted as authored or exact game bytes.
;
; Target evidence: MAIN load offsets 171CC/17676, iatan2 0000:1F3A,
; player_pos DGROUP:36D2, playperf:5770, bullet_template:577E.
; Near difficulty helpers are 00E8/00A4/004C before tune_for_playperf.
.386
.model large
.stack 80h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 1f3ah
public IATAN2
IATAN2 label far
_TEXT ends

MAIN_032_TEXT segment word public 'CODE' use16
assume cs:MAIN_032_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI
public @RANDRING2_NEXT16_MOD$QUI, VECTOR2_NEAR
org 2ch
@randring2_next16$qv label near
org 3ah
@RANDRING2_NEXT16_AND$QUI label near
org 50h
@RANDRING2_NEXT16_MOD$QUI label near
org 6ah
VECTOR2_NEAR label near
org 6a4h
MAIN_032_TEXT ends

PLAYER_A_TEXT segment word public 'CODE' use16
PLAYER_A_TEXT ends

BULLET_A_TEXT segment word public 'CODE' use16
assume cs:BULLET_A_TEXT
public TUNE_FOR_EASY, TUNE_FOR_HARD, TUNE_FOR_LUNATIC
TUNE_FOR_EASY label near
org 44h
TUNE_FOR_HARD label near
org 9ch
TUNE_FOR_LUNATIC label near
org 0e8h
BULLET_A_TEXT ends

main_03 group MAIN_032_TEXT, PLAYER_A_TEXT, BULLET_A_TEXT

CFG_LRES_TEXT segment word public 'CODE' use16
CFG_LRES_TEXT ends
main_01 group CFG_LRES_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _playperf, _bullet_template, _boss
public _CFG_FN, _cfg, _resident
public _boss_sprite_left, _boss_sprite_right, _boss_sprite_stay
public _boss_flystep_random_clamp, _boss_flystep_random_next_y_direc
org 1436h
_boss_flystep_random_clamp label byte
org 18d2h
_CFG_FN label byte
org 36d2h
_player_pos label byte
org 371ah
_boss_sprite_left label word
org 371ch
_boss_sprite_right label word
org 371eh
_boss_sprite_stay label word
org 3720h
_boss_flystep_random_next_y_direc label byte
org 41f2h
_cfg label byte
org 41fch
_resident label dword
org 5770h
_playperf label byte
org 577eh
_bullet_template label byte
org 5abah
_boss label byte
_DATA ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

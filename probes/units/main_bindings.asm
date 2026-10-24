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

main_03 group PLAYER_A_TEXT, BULLET_A_TEXT

_DATA segment word public 'DATA' use16
public _player_pos, _playperf, _bullet_template
org 36d2h
_player_pos label byte
org 5770h
_playperf label byte
org 577eh
_bullet_template label byte
_DATA ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

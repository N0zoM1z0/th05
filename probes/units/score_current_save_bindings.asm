; Actual external codec frames, score-file literal and score state; no payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCORE_CODE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_CODE_TEXT
public @SCOREDAT_DECODE$QV, @SCOREDAT_ENCODE$QV
org (0c812h - 0ae10h)
@SCOREDAT_DECODE$QV label near
org (0c849h - 0ae10h)
@SCOREDAT_ENCODE$QV label near
org (0c8b9h - 0ae10h)
SCORE_CODE_TEXT ends
SCORE_IO_TEXT segment byte public 'CODE' use16
SCORE_IO_TEXT ends
SCORE_IO_TAIL segment byte public 'CODE' use16
org (14ab0h - 0c8f0h)
SCORE_IO_TAIL ends
main_01 group SCORE_CODE_TEXT, SCORE_IO_TEXT, SCORE_IO_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _main_score_filename, _hi, _rank, _playchar
org 00f5eh
_main_score_filename label byte
org 0366eh
_hi label byte
org 0576fh
_rank label byte
org 05773h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

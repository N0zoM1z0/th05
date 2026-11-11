; Foreign score I/O, score/record state and near continuation name only.
; No owned instructions, initialized data, or target bytes are supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCORE_IO_TEXT segment byte public 'CODE' use16
assume cs:SCORE_IO_TEXT
public @scoredat_save_cur$qv
org (0c8b9h - 0ae10h)
@scoredat_save_cur$qv label near
org (0c8f0h - 0ae10h)
SCORE_IO_TEXT ends
SCORE_RAW_TEXT segment byte public 'CODE' use16
SCORE_RAW_TEXT ends
SCORE_RAW_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c998h)
SCORE_RAW_TAIL ends
main_01 group SCORE_IO_TEXT, SCORE_RAW_TEXT, SCORE_RAW_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi, _score, _stage_id, _unnecessary_shift_place_copy, _gCONTINUE
org 00f69h
_gCONTINUE label byte
org 0366eh
_hi label byte
org 036ceh
_unnecessary_shift_place_copy label byte
org 03702h
_score label byte
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

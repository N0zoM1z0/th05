; Only the preceding foreign load function and actual score objects.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCORE_IO_TEXT segment byte public 'CODE' use16
assume cs:SCORE_IO_TEXT
public @scoredat_load_for_cur$qv
org (0c882h - 0ae10h)
@scoredat_load_for_cur$qv label near
org (0c9a4h - 0ae10h)
SCORE_IO_TEXT ends
HISCORE_LOAD_TEXT segment byte public 'CODE' use16
HISCORE_LOAD_TEXT ends
HISCORE_LOAD_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c9bah)
HISCORE_LOAD_TAIL ends
main_01 group SCORE_IO_TEXT, HISCORE_LOAD_TEXT, HISCORE_LOAD_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi, _hiscore
org 0366eh
_hi label byte
org 0370ah
_hiscore label byte
org 03712h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

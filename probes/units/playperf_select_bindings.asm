; True MAIN01/DGROUP frames and five external runtime selector bytes only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
PLAYPERF_PREFIX segment byte public 'CODE' use16
org (0cf7ah - 0ae10h)
PLAYPERF_PREFIX ends
PLAYPERF_TEXT segment byte public 'CODE' use16
PLAYPERF_TEXT ends
PLAYPERF_TAIL segment byte public 'CODE' use16
org (014ab0h - 0cfc6h)
PLAYPERF_TAIL ends
main_01 group PLAYPERF_PREFIX, PLAYPERF_TEXT, PLAYPERF_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _rank, _playperf, _playperf_max, _playperf_min, _playchar
org 0576fh
_rank label byte
org 05770h
_playperf label byte
org 05771h
_playperf_max label byte
org 05772h
_playperf_min label byte
org 05773h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

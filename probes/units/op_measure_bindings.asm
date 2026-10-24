; Actual decoded OP driver frame and mode field only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org 00dceh
SHARED ends
MEASURE_DATA_GAP segment byte public 'CODE' use16
org 00eefh
MEASURE_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 00a62h
_snd_bgm_mode label byte
org 02817h ; Known real foreign music DATA, no supplied values.
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

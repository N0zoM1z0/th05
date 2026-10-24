; Actual decoded MAINE driver frame and mode field only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
org 00a42h
SHARED ends
MEASURE_DATA_GAP segment byte public 'CODE' use16
org 00eabh
MEASURE_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 006dch
_snd_bgm_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

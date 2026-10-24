; Symbol-only context. No implementation or payload bytes.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
org 0061eh
SHARED ends
KAJA_DS_GAP segment byte public 'CODE' use16
org 012d5h
KAJA_DS_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 006dch
_snd_bgm_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

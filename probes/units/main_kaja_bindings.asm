; Symbol-only context. No implementation or payload bytes.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
KAJA_FRAME_GAP segment byte public 'CODE' use16
org 09ca0h
KAJA_FRAME_GAP ends
SHARED segment para public 'CODE' use16
org 004ach
SHARED ends
KAJA_DS_GAP segment byte public 'CODE' use16
org 0ba57h
KAJA_DS_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 00836h
_snd_bgm_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

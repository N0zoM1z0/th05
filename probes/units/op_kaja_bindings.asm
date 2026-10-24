; Symbol-only context. No instructions, implementations or payload values.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org 00976h
SHARED ends
; The full compiled function ends at DC93, before an uncredited original NOP.
OP_KAJA_DS_GAP segment byte public 'CODE' use16
org 0134dh
OP_KAJA_DS_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 00a62h
_snd_bgm_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

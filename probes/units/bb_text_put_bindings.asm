; Original MAIN01 and DGROUP anchor for a complete near raw text painter.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BB_TEXT_PUT_PREFIX segment byte public 'CODE' use16
org (0e51ah - 0ae10h)
BB_TEXT_PUT_PREFIX ends
BB_TEXT_PUT_TEXT segment byte public 'CODE' use16
BB_TEXT_PUT_TEXT ends
BB_TEXT_PUT_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e57ch)
BB_TEXT_PUT_TAIL ends
main_01 group BB_TEXT_PUT_PREFIX, BB_TEXT_PUT_TEXT, BB_TEXT_PUT_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _bb_txt_seg
org 019b0h
_bb_txt_seg label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

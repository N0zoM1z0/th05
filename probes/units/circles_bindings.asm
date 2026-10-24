; Symbol-only foreign context: no instructions or state values.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLE
org 010aeh
GRCG_CIRCLE label far
org 0ae10h
_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:CIRCLE_TEXT
public @grcg_setcolor_direct_raw$qv
org 013f4h
@grcg_setcolor_direct_raw$qv label near
org 0347ah
CIRCLE_TEXT ends
main_01 group CIRCLE_TEXT
CIRCLES_DS_GAP_1 segment byte public 'CODE' use16
org 0f000h
CIRCLES_DS_GAP_1 ends
CIRCLES_DS_GAP_2 segment byte public 'CODE' use16
org 03645h
CIRCLES_DS_GAP_2 ends
_DATA segment word public 'DATA' use16
public _circles_color, _circles
org 041dah
_circles_color label byte
org 09eb4h
_circles label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

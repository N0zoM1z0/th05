; Only real external frames and state, outside both complete device procedures.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_SETCOLOR
org 00F28h
GRCG_SETCOLOR label far
org 0A540h
_TEXT ends
STAFF_BITMAP_TEXT segment byte public 'CODE' use16
org (0E3A4h - 0A540h)
STAFF_BITMAP_TEXT ends
STAFF_BITMAP_TAIL segment byte public 'CODE' use16
org (0E800h - 0E422h)
STAFF_BITMAP_TAIL ends
group_01 group STAFF_BITMAP_TEXT, STAFF_BITMAP_TAIL
SHARED segment para public 'CODE' use16
org (10110h - 0E800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _verdict_bitmap
org 056D8h
_verdict_bitmap label byte
org 0C4D8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

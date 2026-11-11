; Natural stage-2 callback at MAIN 14AAA, before the original SHARED frame.
; Only external CODE labels and segment extents are supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
LOUISE_BACKDROP_PREFIX segment byte public 'CODE' use16
assume cs:LOUISE_BACKDROP_PREFIX
public grcg_fill_playfield_rows
org (010600h - 0AE10h)
grcg_fill_playfield_rows label near
org (014AAAh - 0AE10h)
LOUISE_BACKDROP_PREFIX ends
LOUISE_BACKDROP_TEXT segment byte public 'CODE' use16
LOUISE_BACKDROP_TEXT ends
main_01 group LOUISE_BACKDROP_PREFIX, LOUISE_BACKDROP_TEXT
SHARED segment byte public 'CODE' use16
org (0209D0h - 014AB8h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

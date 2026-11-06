; Only foreign frame reservations and the complete existing two-screen BSS.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
STAFF_BITMAP_PREFIX segment byte public 'CODE' use16
org (0e3a4h - 0a540h)
STAFF_BITMAP_PREFIX ends
STAFF_BITMAP_TEXT segment byte public 'CODE' use16
STAFF_BITMAP_TEXT ends
STAFF_BITMAP_TAIL segment byte public 'CODE' use16
org (0e802h - 0e3cfh)
STAFF_BITMAP_TAIL ends
group_01 group STAFF_BITMAP_PREFIX, STAFF_BITMAP_TEXT, STAFF_BITMAP_TAIL
SHARED segment word public 'CODE' use16
org (010110h - 0e802h)
SHARED ends
_DATA segment word public 'DATA' use16
public _verdict_bitmap
org 056d8h
_verdict_bitmap label byte
org 0c4d8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

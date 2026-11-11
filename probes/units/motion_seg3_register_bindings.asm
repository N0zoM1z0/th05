; Real MAIN03 near-Pascal motion location with foreign-only CODE context.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
MOTION_PRE_MAIN01 segment para public 'CODE' use16
org (014AB0h - 0AE10h)
MOTION_PRE_MAIN01 ends
MOTION_PRE_SHARED segment para public 'CODE' use16
org (015270h - 014AB0h)
MOTION_PRE_SHARED ends
MOTION_SEG3_PREFIX segment byte public 'CODE' use16
org (01527Ch - 015270h)
MOTION_SEG3_PREFIX ends
MOTION_SEG3_TEXT segment byte public 'CODE' use16
MOTION_SEG3_TEXT ends
MOTION_SEG3_TAIL segment byte public 'CODE' use16
org (0209D0h - 01529Ch)
MOTION_SEG3_TAIL ends
main_03 group MOTION_SEG3_PREFIX, MOTION_SEG3_TEXT, MOTION_SEG3_TAIL
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

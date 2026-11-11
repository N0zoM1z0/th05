; Original MAIN01 and DGROUP frames with only the actual laser mask bank label.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
SHOT_LASER_PREFIX segment byte public 'CODE' use16
org (0DDF4h - 0AE10h)
SHOT_LASER_PREFIX ends
SHOT_LASER_PUT_TEXT segment byte public 'CODE' use16
SHOT_LASER_PUT_TEXT ends
SHOT_LASER_TAIL segment byte public 'CODE' use16
org (014AB0h - 0DE58h)
SHOT_LASER_TAIL ends
main_01 group SHOT_LASER_PREFIX, SHOT_LASER_PUT_TEXT, SHOT_LASER_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _SHOT_LASER_DOTS
org 01496h
_SHOT_LASER_DOTS label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

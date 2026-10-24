; Address-only foreign context around the complete Yuuka heart callback.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 0ae10h
_TEXT ends
YUUKA_HEART_TEXT segment byte public 'CODE' use16
org (1027bh - 0ae10h)
YUUKA_HEART_TEXT ends
YUUKA_HEART_TAIL segment byte public 'CODE' use16
org (14ab0h - 102f9h)
YUUKA_HEART_TAIL ends
main_01 group YUUKA_HEART_TEXT, YUUKA_HEART_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _bomb_frame, _bomb_anim
org 04207h
_bomb_frame label byte
org 0420eh
_bomb_anim label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real foreign graphics/math/name providers and complete game-state addresses.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2, SUPER_PUT_RECT
org 01a8ch
IATAN2 label far
org 02974h
SUPER_PUT_RECT label far
org 0a540h
_TEXT ends
REG_NAME_TEXT segment byte public 'CODE' use16
assume cs:REG_NAME_TEXT
public @REG_NAME_PUT$QI10PLAYCHAR_TUC
org (0ba84h - 0a540h)
@REG_NAME_PUT$QI10PLAYCHAR_TUC label near
org (0be76h - 0a540h)
REG_NAME_TEXT ends
REG_UPDATE_TEXT segment byte public 'CODE' use16
REG_UPDATE_TEXT ends
REG_UPDATE_TAIL segment byte public 'CODE' use16
org (0e800h - 0c16ch)
REG_UPDATE_TAIL ends
GROUP_01 group REG_NAME_TEXT, REG_UPDATE_TEXT, REG_UPDATE_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT, BGIMAGE_PUT_RECT_16
org 04a0h
VECTOR2_AT label far
org 04e4h
BGIMAGE_PUT_RECT_16 label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _entered_name_cursor, _hi, _entered_place, _playchar, _glyphballs
org 01522h
_entered_name_cursor label word
org 04f1ah
_hi label byte
org 04f7ah
_glyphballs label byte
org 05076h
_entered_place label byte
org 05078h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

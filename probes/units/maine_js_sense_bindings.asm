; Complete original MAINE near joystick reader is at 2E70.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SOUND_JOY
org 02e70h
SOUND_JOY label near
org 02e82h
_TEXT ends
FOREIGN_MAINE_CODE segment byte public 'CODE' use16
org (010110h - 02e97h)
FOREIGN_MAINE_CODE ends
_DATA segment word public 'DATA' use16
org 01d4ah
_DATA ends
_BSS segment word public 'BSS' use16
org 0a800h
_BSS ends
DGROUP group _DATA, _BSS
end

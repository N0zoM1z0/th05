; Complete original OP near joystick reader is at 2CA8, before the far sensor.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SOUND_JOY
org 02ca8h
SOUND_JOY label near
org 02cbah
_TEXT ends
FOREIGN_OP_CODE segment byte public 'CODE' use16
org (0efe0h - 02ccfh)
FOREIGN_OP_CODE ends
_DATA segment word public 'DATA' use16
org 02dech
_DATA ends
_BSS segment word public 'BSS' use16
org 01128h
_BSS ends
DGROUP group _DATA, _BSS
end

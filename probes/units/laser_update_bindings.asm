; Symbol-only actual frames and foreign APIs. All ORG holes are uncredited.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
LASER_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:LASER_UPDATE_TEXT
public @LASER_HITTEST$QR5LASER
org 028b6h
@LASER_HITTEST$QR5LASER label near
org 07d9dh
LASER_UPDATE_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
LASER_MAIN01_TAIL segment byte public 'CODE' use16
org 01dcbh
LASER_MAIN01_TAIL ends
main_01 group LASER_UPDATE_TEXT, HUD_OVRL_TEXT, LASER_MAIN01_TAIL
LASER_SHARED_CONTEXT segment para public 'CODE' use16
assume cs:LASER_SHARED_CONTEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
LASER_SHARED_CONTEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
main_03 group LASER_SC_TEXT
LASER_MAIN03_CONTEXT segment byte public 'CODE' use16
org 0b760h
LASER_MAIN03_CONTEXT ends
_DATA segment word public 'DATA' use16
public _bullet_zap
org 03f96h
_bullet_zap label byte
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _lasers
org 0578ch
_lasers label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

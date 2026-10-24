; Original external addresses only; no implementations or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
LASER_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
LASER_MAIN01_CONTEXT ends
main_01 group LASER_MAIN01_CONTEXT
LASER_SHARED_CONTEXT segment para public 'CODE' use16
assume cs:LASER_SHARED_CONTEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
LASER_SHARED_CONTEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @playperf_speedtune
org 01f7ah
@playperf_speedtune label near
org 053feh
LASER_SC_TEXT ends
main_03 group LASER_SC_TEXT
LASER_MAIN03_TAIL segment byte public 'CODE' use16
org 061a2h
LASER_MAIN03_TAIL ends
_DATA segment word public 'DATA' use16
public _lasers
org 0578ch
_lasers label byte
public _laser_template
org 05a8ch
_laser_template label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Outside-only MASTER, MAIN frames and real foreign HUD state. No bodies/data.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTCA
org 01d7ah
GAIJI_PUTCA label far
public TEXT_PUTSA
org 02598h
TEXT_PUTSA label far
org 0ae10h
_TEXT ends
HUD_RESOURCES_PREFIX segment byte public 'CODE' use16
org (0d035h - 0ae10h)
HUD_RESOURCES_PREFIX ends
HUD_RESOURCES_TEXT segment byte public 'CODE' use16
HUD_RESOURCES_TEXT ends
HUD_RESOURCES_TAIL segment byte public 'CODE' use16
org (014ab0h - 0d1a2h)
HUD_RESOURCES_TAIL ends
main_01 group HUD_RESOURCES_PREFIX, HUD_RESOURCES_TEXT, HUD_RESOURCES_TAIL
HUD_RESOURCES_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
HUD_RESOURCES_SHARED_SPACE ends
HUD_RESOURCES_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
HUD_RESOURCES_MAIN03_SPACE ends
main_03 group HUD_RESOURCES_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _hud_lives_extra
org 013f0h
_hud_lives_extra label byte
public _hud_bombs_extra
org 013fbh
_hud_bombs_extra label byte
public _lives
org 04ad4h
_lives label byte
public _bombs
org 04ad5h
_bombs label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

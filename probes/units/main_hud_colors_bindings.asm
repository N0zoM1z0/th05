; Original MAIN near-DATA prefix; no resource bytes are furnished by binder.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_COLORS_TEXT segment byte public 'CODE' use16
org 09ca0h
HUD_COLORS_TEXT ends
main_01 group HUD_COLORS_TEXT
HUD_COLORS_OUTSIDE segment byte public 'CODE' use16
org 07c0h
HUD_COLORS_OUTSIDE ends
HUD_COLORS_MAIN03 segment byte public 'CODE' use16
org 0b760h
HUD_COLORS_MAIN03 ends
main_03 group HUD_COLORS_MAIN03
_DATA segment word public 'DATA' use16
org 013ceh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

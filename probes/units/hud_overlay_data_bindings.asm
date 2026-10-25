; Outside-only true MAIN frames; source owns all164 semantic DATA bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
HUD_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
HUD_DATA_TEXT ends
main_01 group HUD_DATA_TEXT
HUD_DATA_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
HUD_DATA_SHARED_SPACE ends
HUD_DATA_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
HUD_DATA_MAIN03_SPACE ends
main_03 group HUD_DATA_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 019ach
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Original MAIN frames and near-DATA prefix, with no glyph bytes in binder.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
GAMEOVER_GAIJI_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
GAMEOVER_GAIJI_DATA_TEXT ends
main_01 group GAMEOVER_GAIJI_DATA_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
GAMEOVER_GAIJI_MAIN03 segment byte public 'CODE' use16
org 0b760h
GAMEOVER_GAIJI_MAIN03 ends
main_03 group GAMEOVER_GAIJI_MAIN03
_DATA segment word public 'DATA' use16
org 0144ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

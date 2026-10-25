; Outside-only real MAIN frame context; source owns all19 selector-text bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BONUS_GLYPH_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
BONUS_GLYPH_MAIN01_SPACE ends
main_01 group BONUS_GLYPH_MAIN01_SPACE
BONUS_GLYPH_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
BONUS_GLYPH_SHARED_SPACE ends
BONUS_GLYPH_DATA_TEXT segment byte public 'CODE' use16
org 0b760h
BONUS_GLYPH_DATA_TEXT ends
main_03 group BONUS_GLYPH_DATA_TEXT
_DATA segment word public 'DATA' use16
org 01a8eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

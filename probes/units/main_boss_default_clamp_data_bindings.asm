; Authentic MAIN CODE frame and preceding DATA prefix only.
; Subpixel coordinate words are produced by the native C++ initializer.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BOSS_DEFAULT_CLAMP_TEXT segment byte public 'CODE' use16
org 09ca0h
BOSS_DEFAULT_CLAMP_TEXT ends
main_01 group BOSS_DEFAULT_CLAMP_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_DEFAULT_CLAMP_MAIN03 segment byte public 'CODE' use16
org 0b760h
BOSS_DEFAULT_CLAMP_MAIN03 ends
main_03 group BOSS_DEFAULT_CLAMP_MAIN03
_DATA segment word public 'DATA' use16
org 01436h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

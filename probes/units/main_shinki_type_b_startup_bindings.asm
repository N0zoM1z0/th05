; Actual MAIN CODE group frames, never the target candidate initializer.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHINKI_BG_TYPE_B_START_TEXT segment byte public 'CODE' use16
org 09ca0h
SHINKI_BG_TYPE_B_START_TEXT ends
main_01 group SHINKI_BG_TYPE_B_START_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHINKI_BG_TYPE_B_START_TEXT_MAIN03 segment byte public 'CODE' use16
org 0b760h
SHINKI_BG_TYPE_B_START_TEXT_MAIN03 ends
main_03 group SHINKI_BG_TYPE_B_START_TEXT_MAIN03
_DATA segment word public 'DATA' use16
org 198ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

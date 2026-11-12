; Only original MAIN CODE frames and the previous original DATA prefix.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHINKI_DEVIL_DELAY_TEXT segment byte public 'CODE' use16
org 09ca0h
SHINKI_DEVIL_DELAY_TEXT ends
main_01 group SHINKI_DEVIL_DELAY_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHINKI_DEVIL_DELAY_TEXT_MAIN03 segment byte public 'CODE' use16
org 0b760h
SHINKI_DEVIL_DELAY_TEXT_MAIN03 ends
main_03 group SHINKI_DEVIL_DELAY_TEXT_MAIN03
_DATA segment word public 'DATA' use16
org 1a58h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

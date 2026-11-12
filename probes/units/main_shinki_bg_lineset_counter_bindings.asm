; The authentic MAIN CODE frames and only the original outside DATA prefix.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHINKI_LINESET_COUNTER_TEXT segment byte public 'CODE' use16
org 09ca0h
SHINKI_LINESET_COUNTER_TEXT ends
main_01 group SHINKI_LINESET_COUNTER_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHINKI_LINESET_COUNTER_MAIN03 segment byte public 'CODE' use16
org 0b760h
SHINKI_LINESET_COUNTER_MAIN03 ends
main_03 group SHINKI_LINESET_COUNTER_MAIN03
_DATA segment word public 'DATA' use16
org 01988h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

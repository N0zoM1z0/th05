; Foreign row-rendering entry and real code/data frames; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
REG_PLACE_ENTRY_TEXT segment byte public 'CODE' use16
assume cs:REG_PLACE_ENTRY_TEXT
public @REGISTRATION_PLACE_PUT$QII
org (0bbefh - 0a540h)
@REGISTRATION_PLACE_PUT$QII label near
org (0bcd3h - 0a540h)
REG_PLACE_ENTRY_TEXT ends
REG_PLACES_TEXT segment byte public 'CODE' use16
REG_PLACES_TEXT ends
REG_PLACES_TAIL segment byte public 'CODE' use16
org (0e800h - 0bcedh)
REG_PLACES_TAIL ends
GROUP_01 group REG_PLACE_ENTRY_TEXT, REG_PLACES_TEXT, REG_PLACES_TAIL
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

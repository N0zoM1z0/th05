; Real MAIN CODE group frames and only the previous DATA prefix.
; The candidate state and surrounding alignment are NOT injected here.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MIDBOSS_DEFEAT_ANGLE_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
MIDBOSS_DEFEAT_ANGLE_DATA_TEXT ends
main_01 group MIDBOSS_DEFEAT_ANGLE_DATA_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
MIDBOSS_DEFEAT_ANGLE_DATA_TEXT_MAIN03 segment byte public 'CODE' use16
org 0b760h
MIDBOSS_DEFEAT_ANGLE_DATA_TEXT_MAIN03 ends
main_03 group MIDBOSS_DEFEAT_ANGLE_DATA_TEXT_MAIN03
_DATA segment word public 'DATA' use16
org 1a60h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

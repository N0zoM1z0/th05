; Authentic MAIN code group frames and outside-only near DATA prefix.
; No raster coverage bytes or foreign CODE instructions are injected.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_LASER_COVERAGE_TEXT segment byte public 'CODE' use16
org 09ca0h
SHOT_LASER_COVERAGE_TEXT ends
main_01 group SHOT_LASER_COVERAGE_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHOT_LASER_COVERAGE_MAIN03 segment byte public 'CODE' use16
org 0b760h
SHOT_LASER_COVERAGE_MAIN03 ends
main_03 group SHOT_LASER_COVERAGE_MAIN03
_DATA segment word public 'DATA' use16
org 01496h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

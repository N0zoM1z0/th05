; Outside-only real MAIN frames; source owns all1024 mathematical velocity bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_VEL_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
SHOT_VEL_DATA_TEXT ends
main_01 group SHOT_VEL_DATA_TEXT
SHOT_VEL_DATA_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SHOT_VEL_DATA_SHARED_SPACE ends
SHOT_VEL_DATA_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
SHOT_VEL_DATA_MAIN03_SPACE ends
main_03 group SHOT_VEL_DATA_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 0f72h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

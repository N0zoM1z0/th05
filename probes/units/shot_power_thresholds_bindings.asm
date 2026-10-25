; Outside-only context; source owns all18 threshold bytes atDS18AC.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_LEVEL_DATA_TEXT segment byte public 'CODE' use16
org 09ca0h
SHOT_LEVEL_DATA_TEXT ends
main_01 group SHOT_LEVEL_DATA_TEXT
SHOT_LEVEL_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SHOT_LEVEL_SHARED_SPACE ends
SHOT_LEVEL_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
SHOT_LEVEL_MAIN03_SPACE ends
main_03 group SHOT_LEVEL_MAIN03_SPACE
_DATA segment word public 'DATA' use16
org 018ach
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

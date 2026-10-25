; Complete motion candidate: placement only, with no supplied instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MOTION_SEG1_TEXT segment byte public 'CODE' use16
org (0be1ah - 0ae10h)
MOTION_SEG1_TEXT ends
main_01 group MOTION_SEG1_TEXT
MOTION_SEG1_TAIL segment byte public 'CODE' use16
org (14ab0h - 0be3ah)
MOTION_SEG1_TAIL ends
MOTION_SEG1_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
MOTION_SEG1_SHARED_SPACE ends
MOTION_SEG1_MAIN03_SPACE segment byte public 'CODE' use16
org (209d0h - 15270h)
MOTION_SEG1_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

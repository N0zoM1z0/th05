; Native foreign frames and the complete bullet template, with no payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
GATHER_COPY_MAIN01 segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
GATHER_COPY_MAIN01 ends
main_01 group GATHER_COPY_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
GATHER_COPY_TO_TEXT segment word public 'CODE' use16
org (016f70h - 015270h)
GATHER_COPY_TO_TEXT ends
GATHER_COPY_TO_TAIL segment byte public 'CODE' use16
org (0209d0h - 016f8bh)
GATHER_COPY_TO_TAIL ends
main_03 group GATHER_COPY_TO_TEXT, GATHER_COPY_TO_TAIL
_DATA segment word public 'DATA' use16
public _bullet_template
org 0577eh
_bullet_template label byte
org 0578ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

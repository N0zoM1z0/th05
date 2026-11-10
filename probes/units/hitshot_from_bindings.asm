; Genuine source-free MAIN01/DS HitShot context; no CODE or DATA payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_RENDER_TEXT segment byte public 'CODE' use16
org (13617h - 0ae10h)
SHOT_RENDER_TEXT ends
HITSHOT_FROM_TEXT segment byte public 'CODE' use16
HITSHOT_FROM_TEXT ends
HITSHOT_FROM_TAIL segment byte public 'CODE' use16
org (14ab0h - 13683h)
HITSHOT_FROM_TAIL ends
main_01 group SHOT_RENDER_TEXT, HITSHOT_FROM_TEXT, HITSHOT_FROM_TAIL
SHARED segment word public 'CODE' use16
org (15270h - 14ab0h)
SHARED ends
MAIN03_CONTEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
MAIN03_CONTEXT ends
main_03 group MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _hitshots, _hitshot_next_free_id
org 0bf56h
_hitshots label byte
org 0c64ah
_hitshot_next_free_id label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

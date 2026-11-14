; Genuine source-free MAIN01/DS HitShot context; no CODE or DATA payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_UPDATE_TEXT segment byte public 'CODE' use16
SHOT_UPDATE_TEXT ends
SHOT_RUNTIME_MAIN01_CONTEXT segment byte public 'CODE' use16
org (13617h - 0ae10h)
SHOT_RUNTIME_MAIN01_CONTEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
SHOT_HIT_TEXT ends
HITSHOT_FROM_TAIL segment byte public 'CODE' use16
org (14ab0h - 13683h)
HITSHOT_FROM_TAIL ends
main_01 group SHOT_UPDATE_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_HIT_TEXT, HITSHOT_FROM_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
SHOT_RUNTIME_MAIN03_CONTEXT ends
main_03 group SHOT_RUNTIME_MAIN03_CONTEXT
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

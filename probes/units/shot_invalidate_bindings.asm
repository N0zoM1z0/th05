; Complete natural shot invalidation; only outside foreign addresses/extents.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_UPDATE_TEXT segment byte public 'CODE' use16
SHOT_UPDATE_TEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
SHOT_HIT_TEXT ends
SHOT_RUNTIME_MAIN01_CONTEXT segment byte public 'CODE' use16
SHOT_RUNTIME_MAIN01_CONTEXT ends
SHOT_INVALIDATE_TEXT segment byte public 'CODE' use16
assume cs:SHOT_INVALIDATE_TEXT
public TILES_INVALIDATE_AROUND
org (0bad2h - 0ae10h)
TILES_INVALIDATE_AROUND label near
org (1337dh - 0ae10h)
SHOT_INVALIDATE_TEXT ends
SHOT_INVALIDATE_TAIL segment byte public 'CODE' use16
org (14ab0h - 133dbh)
SHOT_INVALIDATE_TAIL ends
main_01 group SHOT_UPDATE_TEXT, SHOT_HIT_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_INVALIDATE_TEXT, SHOT_INVALIDATE_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
SHOT_RUNTIME_MAIN03_CONTEXT ends
main_03 group SHOT_RUNTIME_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _tile_invalidate_box
org 03502h
_tile_invalidate_box label dword
public _shots
org 0ba8eh
_shots label byte
public _hitshots
org 0bf56h
_hitshots label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Native symbols and section origins only; no fake helpers or data values.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BULLET_GATHER_PREFIX segment byte public 'CODE' use16
assume cs:BULLET_GATHER_PREFIX
public tiles_invalidate_around
org (0bad2h - 0ae10h)
tiles_invalidate_around label near
org (0e40eh - 0ae10h)
BULLET_GATHER_PREFIX ends
BULLET_GATHER_INV_TEXT segment byte public 'CODE' use16
BULLET_GATHER_INV_TEXT ends
BULLET_GATHER_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e4b6h)
BULLET_GATHER_TAIL ends
main_01 group BULLET_GATHER_PREFIX, BULLET_GATHER_INV_TEXT, BULLET_GATHER_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _bullet_zap_active, _bullet_clear_time
public _bullets, _gather_circles
org 03502h
_tile_invalidate_box label dword
org 03f96h
_bullet_zap_active label byte
org 03f97h
_bullet_clear_time label byte
org 05f2ah
_bullets label byte
org 09bfah
_gather_circles label byte
org 09e5ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

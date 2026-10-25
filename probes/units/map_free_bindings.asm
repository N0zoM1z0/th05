; Outside-only context for genuine MAP release; no owned body or90 supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 0291eh
HMEM_FREE label far
org 0ae10h
_TEXT ends
MAP_FREE_PREFIX segment byte public 'CODE' use16
org (0e606h - 0ae10h)
MAP_FREE_PREFIX ends
MAP_FREE_TEXT segment byte public 'CODE' use16
MAP_FREE_TEXT ends
MAP_FREE_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e61dh)
MAP_FREE_TAIL ends
main_01 group MAP_FREE_PREFIX, MAP_FREE_TEXT, MAP_FREE_TAIL
MAP_FREE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
MAP_FREE_SHARED_SPACE ends
MAP_FREE_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
MAP_FREE_MAIN03_SPACE ends
main_03 group MAP_FREE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _map_seg
org 04ad8h
_map_seg label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

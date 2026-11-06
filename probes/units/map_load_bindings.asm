; Outside-only native frames and foreign symbols, without payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 0281ah
HMEM_ALLOCBYTE label far
org 0ae10h
_TEXT ends
MAP_LOAD_PREFIX segment byte public 'CODE' use16
org (0e5c2h - 0ae10h)
MAP_LOAD_PREFIX ends
MAP_LOAD_TEXT segment byte public 'CODE' use16
MAP_LOAD_TEXT ends
MAP_FREE_TEXT segment byte public 'CODE' use16
assume cs:main_01
public @map_free$qv
@map_free$qv label near
org (014ab0h - 0e606h)
MAP_FREE_TEXT ends
main_01 group MAP_LOAD_PREFIX, MAP_LOAD_TEXT, MAP_FREE_TEXT
SHARED segment para public 'CODE' use16
org 07c0h
SHARED ends
MAP_LOAD_MAIN03 segment word public 'CODE' use16
org 0b760h
MAP_LOAD_MAIN03 ends
main_03 group MAP_LOAD_MAIN03
_DATA segment word public 'DATA' use16
public _map_fn, _map_header, _map_seg, _stage_id
org 018c8h
_map_fn label byte
org 018d1h
org 041eah
_map_header label byte
org 041f2h
org 04ad8h
_map_seg label word
org 04adah
org 0576eh
_stage_id label byte
org 0576fh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

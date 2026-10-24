; Real symbol-only context for complete27+105-byte B4Ball reset/allocation.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
YUKI_SOLO_RENDER_TEXT ends
B4_SPAWN_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
B4_SPAWN_MAIN01_SPACE ends
main_01 group YUKI_SOLO_RENDER_TEXT, B4_SPAWN_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public VECTOR2_NEAR, @playperf_speedtune
org 006ah
VECTOR2_NEAR label near
org (171eah - 15270h)
@playperf_speedtune label near
org (183d5h - 15270h)
MAIN_035_TEXT ends
B4_SPAWN_AFTER_TEXT segment byte public 'CODE' use16
org (209d0h - 18459h)
B4_SPAWN_AFTER_TEXT ends
main_03 group MAIN_035_TEXT, B4_SPAWN_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _custom_entities
org 0b3f4h
_custom_entities label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

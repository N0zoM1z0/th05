; Real sprite and scalar scroll providers; complete full foreign Sword pool.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
BULLET_RENDER_TEXT segment byte public 'CODE' use16
assume cs:BULLET_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW, SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0BF62h - 0AE10h)
Z_SUPER_ROLL_PUT_TINY_32X32_RAW label near
org (0DF28h - 0AE10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
BULLET_RENDER_TEXT ends
YUMEKO_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
org (143E0h - 0DF28h)
YUMEKO_UPDATE_MAIN01_TEXT ends
main_01 group GENERIC_BOSS_MAIN01_TEXT, BULLET_RENDER_TEXT, YUMEKO_UPDATE_MAIN01_TEXT
SWORD_RENDER_MAIN03_GAP segment byte public 'CODE' use16
org (15270h - 14422h)
SWORD_RENDER_MAIN03_GAP ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
B5_UPDATE_TEXT ends
main_03 group BOSS_TEXT, B5_UPDATE_TEXT
SWORD_RENDER_DGROUP_GAP segment byte public 'CODE' use16
org (209D0h - 15270h)
SWORD_RENDER_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _custom_entities
org 0B3F4h
_custom_entities label byte
org 0BA74h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

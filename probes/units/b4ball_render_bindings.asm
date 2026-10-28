; Real near sprite/scroll providers and foreign full custom pool only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
BULLET_RENDER_TEXT segment byte public 'CODE' use16
assume cs:BULLET_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW, SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0BF62h - 0AE10h)
Z_SUPER_ROLL_PUT_TINY_32X32_RAW label near
org (0DF28h - 0AE10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
BULLET_RENDER_TEXT ends
YUKI_SOLO_RENDER_TEXT segment byte public 'CODE' use16
org (108DFh - 0DF28h)
YUKI_SOLO_RENDER_TEXT ends
main_01 group HUD_OVRL_TEXT, BULLET_RENDER_TEXT, YUKI_SOLO_RENDER_TEXT
B4_RENDER_MAIN03_GAP segment byte public 'CODE' use16
org (15270h - 1093Fh)
B4_RENDER_MAIN03_GAP ends
MAIN_035_TEXT segment word public 'CODE' use16
MAIN_035_TEXT ends
main_03 group MAIN_035_TEXT
B4_RENDER_DGROUP_GAP segment byte public 'CODE' use16
org (209D0h - 15270h)
B4_RENDER_DGROUP_GAP ends
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

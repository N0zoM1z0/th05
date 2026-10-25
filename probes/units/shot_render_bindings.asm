; Real outside-only context for complete natural shot renderer164.
; No helper bodies, instruction values, stack or in-owner gaps.
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
SHOT_RENDER_TEXT segment byte public 'CODE' use16
assume cs:SHOT_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_16X16_RAW
org 0126ch
Z_SUPER_ROLL_PUT_TINY_16X16_RAW label near
public @grcg_setmode_rmw$qv
org 013e8h
@grcg_setmode_rmw$qv label near
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org 03118h
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (13573h - 0ae10h)
SHOT_RENDER_TEXT ends
SHOT_RENDER_TAIL segment byte public 'CODE' use16
org (14ab0h - 13617h)
SHOT_RENDER_TAIL ends
main_01 group SHOT_UPDATE_TEXT, SHOT_HIT_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_RENDER_TEXT, SHOT_RENDER_TAIL
SHOT_RENDER_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SHOT_RENDER_SHARED_SPACE ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
SHOT_RUNTIME_MAIN03_CONTEXT ends
main_03 group SHOT_RUNTIME_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _hitshots
org 0bf56h
_hitshots label byte
public _shots_alive
org 0c4c8h
_shots_alive label byte
public _shots_alive_count
org 0c648h
_shots_alive_count label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

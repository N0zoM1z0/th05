; Original external symbol positions; no function bodies or owned state.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLEFILL
org 100eh
GRCG_CIRCLEFILL label far
org 0ae10h
_TEXT ends

BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
MAIN_0_TEXT segment byte public 'CODE' use16
assume cs:MAIN_0_TEXT
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW, @grcg_setcolor_direct_raw$qv, CHEETOS_RENDER
org (0bf62h - 0ae10h)
Z_SUPER_ROLL_PUT_TINY_32X32_RAW label near
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (12f2bh - 0ae10h)
CHEETOS_RENDER label near
org (12ff5h - 0ae10h)
MAIN_0_TEXT ends
main_01 group BOSS_BG_TEXT, MAIN_0_TEXT

B6_RENDER_SHARED_GAP segment para public 'CODE' use16
org (15270h - 13070h)
B6_RENDER_SHARED_GAP ends

B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
B6_UPDATE_TEXT ends
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
B6_PATTERN_A_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
B6_RENDER_MAIN03_GAP segment byte public 'CODE' use16
org (209d0h - 15270h)
B6_RENDER_MAIN03_GAP ends
main_03 group B6_BALLS_TEXT, B6_UPDATE_TEXT, B6_PATTERN_A_TEXT, LASER_SC_TEXT, BULLET_A_TEXT, B6_RENDER_MAIN03_GAP

_DATA segment word public 'DATA' use16
public _custom_entities
org 0b3f4h
_custom_entities label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

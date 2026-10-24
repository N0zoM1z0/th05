; Real external sprite/explosion context for complete Sara159 +Louise116.
; All origin holes are outside the source-owned275-byte contribution.
.386
.model large
UNIT_START equ 140c4h
UNIT_END equ 141d7h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_LARGE_PUT, SUPER_PUT_1PLANE, SUPER_PUT
org 02048h
SUPER_LARGE_PUT label far
org 02adah
SUPER_PUT_1PLANE label far
org 033f0h
SUPER_PUT label far
org 0ae10h
_TEXT ends
BOSS_FG_TEXT segment byte public 'CODE' use16
assume cs:BOSS_FG_TEXT
public @explosions_small_update_and_rend$qv
org (1060eh - 0ae10h)
@explosions_small_update_and_rend$qv label near
public @explosions_big_update_and_render$qv
org (106d8h - 0ae10h)
@explosions_big_update_and_render$qv label near
org (UNIT_START - 0ae10h)
BOSS_FG_TEXT ends
BOSS_FG_TAIL segment byte public 'CODE' use16
org (14ab0h - UNIT_END)
BOSS_FG_TAIL ends
main_01 group BOSS_FG_TEXT, BOSS_FG_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_FG_MAIN03_SPACE segment byte public 'CODE' use16
org (209d0h - 15270h)
BOSS_FG_MAIN03_SPACE ends
main_03 group BOSS_FG_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _stage_frame_mod8, _stage_frame_mod16, _boss
org 05768h
_stage_frame_mod8 label byte
org 05769h
_stage_frame_mod16 label byte
org 05abah
_boss label byte
org 05ad2h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

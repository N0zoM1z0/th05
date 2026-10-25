; Symbol-only outside layout for the complete126-byte survivor foreground.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 1093fh
UNIT_END equ 109bdh
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_LARGE_PUT, SUPER_PUT_1PLANE, SUPER_PUT
org 02048h
SUPER_LARGE_PUT label far
org 02adah
SUPER_PUT_1PLANE label far
org 033f0h
SUPER_PUT label far
org MAIN01_BASE
_TEXT ends
BOSS_FG_TEXT segment byte public 'CODE' use16
assume cs:BOSS_FG_TEXT
public @explosions_small_update_and_rend$qv, @explosions_big_update_and_render$qv
org (1060eh - MAIN01_BASE)
@explosions_small_update_and_rend$qv label near
org (106d8h - MAIN01_BASE)
@explosions_big_update_and_render$qv label near
org (UNIT_START - MAIN01_BASE)
BOSS_FG_TEXT ends
SURVIVOR_FG_TEXT segment byte public 'CODE' use16
SURVIVOR_FG_TEXT ends
SURVIVOR_FG_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
SURVIVOR_FG_AFTER_TEXT ends
main_01 group BOSS_FG_TEXT, SURVIVOR_FG_TEXT, SURVIVOR_FG_AFTER_TEXT
SURVIVOR_FG_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
SURVIVOR_FG_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _stage_frame_mod8, _boss
org 5768h
_stage_frame_mod8 label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real symbols and outside-only holes around the full163-byte callback.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 11cadh
UNIT_END equ 11d50h
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
EXALICE_FG_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_FG_TEXT
public @explosions_small_update_and_rend$qv, @explosions_big_update_and_render$qv
org (1060eh - MAIN01_BASE)
@explosions_small_update_and_rend$qv label near
org (106d8h - MAIN01_BASE)
@explosions_big_update_and_render$qv label near
org (UNIT_START - MAIN01_BASE)
EXALICE_FG_TEXT ends
EX_FG_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
EX_FG_AFTER_TEXT ends
main_01 group EXALICE_FG_TEXT, EX_FG_AFTER_TEXT
EX_FG_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
EX_FG_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _exalice_bomb_invincibility, _exalice_backdrop_patnum
public _stage_frame_mod16, _boss
org 4a8eh
_exalice_bomb_invincibility label byte
org 4a9ch
_exalice_backdrop_patnum label word
org 5769h
_stage_frame_mod16 label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

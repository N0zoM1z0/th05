; Address-only context around the full531-byte compiler contribution.
; Only the complete381-byte puppet renderer is an exact candidate.
; No instructions, initialized data, stack or gaps inside either function.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 141d7h
UNIT_END equ 143eah
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLEFILL, GRCG_CIRCLE, GRCG_HLINE, GRCG_SETCOLOR
public SUPER_LARGE_PUT, SUPER_PUT_1PLANE, SUPER_ROLL_PUT, SUPER_PUT
org 0100eh
GRCG_CIRCLEFILL label far
org 010aeh
GRCG_CIRCLE label far
org 01690h
GRCG_HLINE label far
org 01a88h
GRCG_SETCOLOR label far
org 02048h
SUPER_LARGE_PUT label far
org 02adah
SUPER_PUT_1PLANE label far
org 02fe0h
SUPER_ROLL_PUT label far
org 033f0h
SUPER_PUT label far
org MAIN01_BASE
_TEXT ends

MAIN_01_TEXT segment byte public 'CODE' use16
MAIN_01_TEXT ends
ALICE_FG_TEXT segment byte public 'CODE' use16
assume cs:ALICE_FG_TEXT
public @explosions_small_update_and_rend$qv, @explosions_big_update_and_render$qv
org (1060eh - MAIN01_BASE)
@explosions_small_update_and_rend$qv label near
org (106d8h - MAIN01_BASE)
@explosions_big_update_and_render$qv label near
org (UNIT_START - MAIN01_BASE)
ALICE_FG_TEXT ends
ALICE_FG_AFTER_TEXT segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
ALICE_FG_AFTER_TEXT ends
main_01 group MAIN_01_TEXT, ALICE_FG_TEXT, ALICE_FG_AFTER_TEXT

SHARED segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SHARED ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
B4_UPDATE_TEXT ends
ALICE_FG_MAIN03_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
ALICE_FG_MAIN03_GAP ends
main_03 group B4_UPDATE_TEXT, ALICE_FG_MAIN03_GAP

_DATA segment word public 'DATA' use16
public _stage_frame, _stage_frame_mod2, _stage_frame_mod8, _stage_frame_mod16
public _boss, _custom_entities, _boss_statebyte
org 5764h
_stage_frame label word
org 5766h
_stage_frame_mod2 label byte
org 5768h
_stage_frame_mod8 label byte
org 5769h
_stage_frame_mod16 label byte
org 5abah
_boss label byte
org 0b3f4h
_custom_entities label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

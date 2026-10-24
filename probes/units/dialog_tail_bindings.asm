; True TH05 dialog-tail foreign context only. No code bodies, resource values,
; stack, or inserted compiler padding. GameExecl remains a real far routine.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 13e58h
UNIT_END equ 140c4h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT, FILE_CLOSE, FILE_READ, FILE_ROPEN, PALETTE_SHOW
public HMEM_ALLOCBYTE, HMEM_FREE, SUPER_ENTRY_BFNT, SUPER_CLEAN, SUPER_CONVERT_TINY, EMS_READ
org 00644h
PALETTE_BLACK_OUT label far
org 00d2eh
FILE_CLOSE label far
org 00d3eh
FILE_READ label far
org 00df2h
FILE_ROPEN label far
org 02158h
PALETTE_SHOW label far
org 0281ah
HMEM_ALLOCBYTE label far
org 0291eh
HMEM_FREE label far
org 02d16h
SUPER_ENTRY_BFNT label far
org 02df0h
SUPER_CLEAN label far
org 035a2h
SUPER_CONVERT_TINY label far
org 03f6ah
EMS_READ label far
org MAIN01_BASE
_TEXT ends
; Match the genuine empty code contexts declared by reused demo.hpp.
DEMO_GAMEEXECL_CONTEXT segment byte public 'CODE' use16
DEMO_GAMEEXECL_CONTEXT ends
DEMO_TEXT segment byte public 'CODE' use16
DEMO_TEXT ends
DIALOG_TAIL_TEXT segment byte public 'CODE' use16
assume cs:DIALOG_TAIL_TEXT
public @GAMEEXECL$QNXC, @overlay_wipe$qv
public @playfield_copy_front_to_back$qv, @DIALOG_FACE_UNPUT_8$QUIUI
public @dialog_box_fade_in_animate$qv, @dialog_run$qv
; This is the original real far routine at CEC2, with RETF4 at CF5E.
; Its address shares this true CODE context; no near prototype or ASM call.
org (0cec2h - MAIN01_BASE)
@GAMEEXECL$QNXC label far
org (11d50h - MAIN01_BASE)
@overlay_wipe$qv label near
org (13a96h - MAIN01_BASE)
@playfield_copy_front_to_back$qv label near
org (13aceh - MAIN01_BASE)
@DIALOG_FACE_UNPUT_8$QUIUI label near
org (13b50h - MAIN01_BASE)
@dialog_box_fade_in_animate$qv label near
org (13d4ah - MAIN01_BASE)
@dialog_run$qv label near
org (UNIT_START - MAIN01_BASE)
DIALOG_TAIL_TEXT ends
main_01 group DEMO_GAMEEXECL_CONTEXT, DEMO_TEXT, DIALOG_TAIL_TEXT
DIALOG_TAIL_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
DIALOG_TAIL_SHARED_GAP ends
SHARED segment word public 'CODE' use16
assume cs:SHARED
public CDG_PUT_8, SND_LOAD, SND_KAJA_INTERRUPT, @FRAME_DELAY$QI
public CDG_LOAD_SINGLE_NOALPHA, CDG_LOAD_SINGLE, CDG_FREE
org 002b8h
CDG_PUT_8 label far
org 003f4h
SND_LOAD label far
org 004ach
SND_KAJA_INTERRUPT label far
org 00652h
@FRAME_DELAY$QI label far
org 00668h
CDG_LOAD_SINGLE_NOALPHA label far
org 0066eh
CDG_LOAD_SINGLE label far
org 00788h
CDG_FREE label far
SHARED ends
DIALOG_TAIL_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 15240h)
DIALOG_TAIL_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _dialog_sequence_id, _st06_bb1, _st06_bb2
public _BGM_EXTRA_BOSS_FN, _DEMO_EXTRA_PART_2_FN, _DIALOG_BINARY_OP
public _faceset_boss_format, _faceset_playchar_format
public _BOMB_BG_REIMU_FN, _BOMB_BG_MARISA_FN, _BOMB_BG_MIMA_FN, _BOMB_BG_YUUKA_FN
public _MIKO16_EXALICE_FN, _BOMB_SHAPE_YUUKA_FN_2, _BOMB_SHAPE_FN_2
public _cdg_slots, _resident, _page_back, _page_front
public _stage_frame, _stage_id, _playchar, _Ems, _DemoBuf, _dialog_side
org 003dah
_PaletteTone label word
org 01ee8h
_dialog_sequence_id label byte
org 01ef6h
_st06_bb1 label byte
org 01effh
_st06_bb2 label byte
org 01f08h
_BGM_EXTRA_BOSS_FN label byte
org 01f0eh
_DEMO_EXTRA_PART_2_FN label byte
org 01f18h
_DIALOG_BINARY_OP label byte
org 01f1bh
_faceset_boss_format label byte
org 01f24h
_faceset_playchar_format label byte
org 01f2dh
_BOMB_BG_REIMU_FN label byte
org 01f35h
_BOMB_BG_MARISA_FN label byte
org 01f3dh
_BOMB_BG_MIMA_FN label byte
org 01f45h
_BOMB_BG_YUUKA_FN label byte
org 01f4dh
_MIKO16_EXALICE_FN label byte
org 01f59h
_BOMB_SHAPE_YUUKA_FN_2 label byte
org 01f63h
_BOMB_SHAPE_FN_2 label byte
org 0306ch
_cdg_slots label byte
org 041fch
_resident label dword
org 04ad6h
_page_back label byte
org 04ad7h
_page_front label byte
org 05764h
_stage_frame label word
org 0576eh
_stage_id label byte
org 05773h
_playchar label byte
org 05774h
_Ems label word
org 05778h
_DemoBuf label dword
org 0c660h
_dialog_side label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

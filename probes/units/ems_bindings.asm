; Real TH05 EMS/CDG/master symbol context only. No helper implementations,
; instructions, resource values, stack or inside-unit alignment bytes.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0b826h
UNIT_END equ 0bad2h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN, PALETTE_SHOW, HMEM_ALLOCBYTE
public EMS_READ, EMS_ALLOCATE, EMS_EXIST, EMS_SETNAME, EMS_WRITE, EMS_SPACE
org 00600h
PALETTE_BLACK_IN label far
org 02158h
PALETTE_SHOW label far
org 0281ah
HMEM_ALLOCBYTE label far
org 03f6ah
EMS_READ label far
org 03fcch
EMS_ALLOCATE label far
org 04000h
EMS_EXIST label far
org 04052h
EMS_SETNAME label far
org 0406ch
EMS_WRITE label far
org 040ceh
EMS_SPACE label far
org MAIN01_BASE
_TEXT ends
EMS_TEXT segment byte public 'CODE' use16
assume cs:EMS_TEXT
org (UNIT_START - MAIN01_BASE)
EMS_TEXT ends
main_01 group EMS_TEXT
EMS_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
EMS_SHARED_GAP ends
SHARED segment word public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8, CDG_LOAD_SINGLE_NOALPHA
public CDG_LOAD_ALL_NOALPHA, CDG_LOAD_ALL, CDG_FREE
org 001c0h
CDG_PUT_NOALPHA_8 label far
org 00668h
CDG_LOAD_SINGLE_NOALPHA label far
org 00726h
CDG_LOAD_ALL_NOALPHA label far
org 0072ch
CDG_LOAD_ALL label far
org 00788h
CDG_FREE label far
SHARED ends
; The next foreign paragraph begins beyond the last address-only label.
EMS_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 15240h)
EMS_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _eyename, _bbname, _EMS_NAME
public _FACESET_REIMU_FN_0, _FACESET_MARISA_FN_0, _FACESET_MIMA_FN, _FACESET_YUUKA_FN
public _PaletteTone, _cdg_slots, _resident, _stage_id, _rank, _playchar, _Ems
org 0009ch
_eyename label dword
org 000a6h
_bbname label dword
org 00229h
_EMS_NAME label byte
org 0023ah
_FACESET_REIMU_FN_0 label byte
org 00243h
_FACESET_MARISA_FN_0 label byte
org 0024ch
_FACESET_MIMA_FN label byte
org 00255h
_FACESET_YUUKA_FN label byte
org 003dah
_PaletteTone label word
org 0306ch
_cdg_slots label byte
org 041fch
_resident label dword
org 0576eh
_stage_id label byte
org 0576fh
_rank label byte
org 05773h
_playchar label byte
org 05774h
_Ems label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

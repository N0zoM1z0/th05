; Original TH05 demo foreign-symbol context. No instructions or initializers.
; GameExecl remains a genuine far function; its external call's linker
; relaxation must be observed, never replaced by authored ASM or a false ABI.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0b756h
UNIT_END equ 0b826h
GAMEEXECL_START equ 0cec2h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT, FILE_CLOSE, FILE_READ, FILE_ROPEN, HMEM_ALLOCBYTE, HMEM_FREE
org 0644h
PALETTE_BLACK_OUT label far
org 0d2eh
FILE_CLOSE label far
org 0d3eh
FILE_READ label far
org 0df2h
FILE_ROPEN label far
org 0281ah
HMEM_ALLOCBYTE label far
org 0291eh
HMEM_FREE label far
org MAIN01_BASE
_TEXT ends
DEMO_TEXT segment byte public 'CODE' use16
assume cs:DEMO_TEXT
org (UNIT_START - MAIN01_BASE)
DEMO_TEXT ends
DEMO_GAMEEXECL_CONTEXT segment byte public 'CODE' use16
assume cs:DEMO_GAMEEXECL_CONTEXT
public @GAMEEXECL$QNXC
org (GAMEEXECL_START - UNIT_END)
@GAMEEXECL$QNXC label far
DEMO_GAMEEXECL_CONTEXT ends
main_01 group DEMO_TEXT, DEMO_GAMEEXECL_CONTEXT
DEMO_DGROUP_GAP segment byte public 'CODE' use16
org (014ab0h - GAMEEXECL_START)
DEMO_DGROUP_GAP ends
DEMO_DGROUP_GAP2 segment byte public 'CODE' use16
org (DGROUP_BASE - 014ab0h)
DEMO_DGROUP_GAP2 ends
_DATA segment word public 'DATA' use16
public _demo_fn, _DEMOPLAY_BINARY_OP, _key_det, _shiftkey, _resident, _stage_frame, _DemoBuf
org 021ch
_demo_fn label byte
org 0226h
_DEMOPLAY_BINARY_OP label byte
org 03064h
_key_det label word
org 03066h
_shiftkey label byte
org 041fch
_resident label dword
org 05764h
_stage_frame label word
org 05778h
_DemoBuf label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

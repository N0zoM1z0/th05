; One immutable symbol-only source, assembled before and after real C++.
; GameExecl retains its genuine far Pascal ABI and original native address.
.386
ifdef BINDINGS_AFTER
; Native post-demo extent and genuine FAR provider in the common public CODE.
DEMO_TEXT segment byte public 'CODE' use16
assume cs:DEMO_TEXT
public @GAMEEXECL$QNXC
org (0cec2h - 0b826h)
@GAMEEXECL$QNXC label far
DEMO_TEXT ends
DEMO_GAMEEXECL_CONTEXT segment byte public 'CODE' use16
DEMO_GAMEEXECL_CONTEXT ends
main_01 group DEMO_TEXT, DEMO_GAMEEXECL_CONTEXT
DEMO_DGROUP_GAP segment byte public 'CODE' use16
org (014ab0h - 0cec2h)
DEMO_DGROUP_GAP ends
DEMO_DGROUP_GAP2 segment byte public 'CODE' use16
org (209d0h - 014ab0h)
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
org 0577ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
else
; Native foreign endpoints and pre-demo extent only. No instructions or data.
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
org 0ae10h
_TEXT ends
DEMO_TEXT segment byte public 'CODE' use16
org (0b756h - 0ae10h)
DEMO_TEXT ends
DEMO_GAMEEXECL_CONTEXT segment byte public 'CODE' use16
DEMO_GAMEEXECL_CONTEXT ends
main_01 group DEMO_TEXT, DEMO_GAMEEXECL_CONTEXT
endif
end

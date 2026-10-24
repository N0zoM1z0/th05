; OP setup symbol-only context, original decoded payload offsets.
; No instructions, string/array values, or source-owned state are supplied.
.386
.model large
; Deliberately no .stack: source-owned BSS must retain its real placement.
OP01_BASE equ 0a390h
UNIT_START equ 0b077h
UNIT_SIZE equ 059fh
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0d300h
SHARED_END equ 0e2d8h
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 0ab6h
OWNED_DATA_SIZE equ 0433h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 03f20h
OWNED_BSS_SIZE equ 0034h
OWNED_BSS_END equ (OWNED_BSS_START + OWNED_BSS_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019F0h
PALETTE_SHOW label far
public SUPER_FREE
org 024F2h
SUPER_FREE label far
public SUPER_ENTRY_BFNT
org 02656h
SUPER_ENTRY_BFNT label far
public SUPER_PUT
org 0292Ah
SUPER_PUT label far
org OP01_BASE
_TEXT ends

; The compiler's byte-aligned CODE contribution begins at OP01:0CE7.
OP_SETUP_TEXT segment byte public 'CODE' use16
assume cs:OP_SETUP_TEXT
org (UNIT_START - OP01_BASE)
OP_SETUP_TEXT ends

OP_SETUP_CODE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
OP_SETUP_CODE_TAIL ends
op_01 group OP_SETUP_TEXT, OP_SETUP_CODE_TAIL

OP_SETUP_SHARED_TEXT segment para public 'CODE' use16
assume cs:OP_SETUP_SHARED_TEXT
public GRAPH_PUTSA_FX
org 0136h
GRAPH_PUTSA_FX label far
public @PI_LOAD$QINXC
org 0AD8h
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org 0B0Ah
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org 0BBAh
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0BE0h
@PI_FREE$QI label far
public @INPUT_WAIT_FOR_CHANGE$QI
org 0DA4h
@INPUT_WAIT_FOR_CHANGE$QI label far
public @FRAME_DELAY$QI
org 0E5Eh
@FRAME_DELAY$QI label far
public @EGC_COPY_RECT_1_TO_0_16$QIIII
org 0FD8h
@EGC_COPY_RECT_1_TO_0_16$QIIII label far
OP_SETUP_SHARED_TEXT ends
OP_SETUP_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_SETUP_DGROUP_GAP ends

; Only a foreign prefix: the compiler supplies both 9-pointer help tables
; and all readable CP932-staged help/choice/caption/filename strings.
_DATA segment word public 'DATA' use16
public _PaletteTone
org 054eh
_PaletteTone label word
org OWNED_DATA_START
_DATA ends

; Foreign DATA/BSS context ends before the complete compiler-owned BSS.
OP_SETUP_DATA_TAIL segment byte public 'DATA' use16
public _resident
org (02dech - OWNED_DATA_END)
_resident label dword
public _key_det
org (03a92h - OWNED_DATA_END)
_key_det label word
org (OWNED_BSS_START - OWNED_DATA_END)
OP_SETUP_DATA_TAIL ends

; palette_unused and the real two-word window remain compiler-owned.
_BSS segment byte public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_SETUP_DATA_TAIL, _BSS
end

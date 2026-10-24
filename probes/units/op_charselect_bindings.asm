; OP character selection symbol-only context, original decoded destinations.
; No instruction bodies, VRAM pointer values, image data or owner state.
.386
.model large
; No .stack: the compiler owns all 15 bytes of this BSS contribution.
OP01_BASE equ 0a390h
UNIT_START equ 0ce65h
UNIT_SIZE equ 049eh
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_FRAME_BASE equ 0d300h
SHARED_CONTEXT_START equ 0d304h
SHARED_END equ 0e15eh
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 0284eh
OWNED_DATA_SIZE equ 0008h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 05138h
OWNED_BSS_SIZE equ 000fh

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public GRCG_BYTEBOXFILL_X
org 0BACh
GRCG_BYTEBOXFILL_X label far
public GRCG_SETCOLOR
org 0EE2h
GRCG_SETCOLOR label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019F0h
PALETTE_SHOW label far
org OP01_BASE
_TEXT ends

M_CHAR_TEXT segment byte public 'CODE' use16
assume cs:M_CHAR_TEXT
org (UNIT_START - OP01_BASE)
M_CHAR_TEXT ends
op_01 group M_CHAR_TEXT

; The owner really ends at D303. Only the following foreign alignment byte
; precedes the context at D304; never align backward to the D300 far frame.
OP_CHARSELECT_SHARED_ALIGN segment byte public 'CODE' use16
org (SHARED_CONTEXT_START - UNIT_END)
OP_CHARSELECT_SHARED_ALIGN ends

; A real-mode paragraph frame can precede a byte/word-aligned contribution.
; This word-aligned segment starts four bytes into D30, so offsets below
; subtract that bias. The linker must preserve actual original frame:offset.
OP_CHARSELECT_SHARED_TEXT segment word public 'CODE' use16
assume cs:OP_CHARSELECT_SHARED_TEXT
public CDG_PUT_NOALPHA_8
org (SHARED_FRAME_BASE + 0290h - SHARED_CONTEXT_START)
CDG_PUT_NOALPHA_8 label far
public _snd_se_reset
org (SHARED_FRAME_BASE + 02F6h - SHARED_CONTEXT_START)
_snd_se_reset label far
public SND_SE_PLAY
org (SHARED_FRAME_BASE + 0302h - SHARED_CONTEXT_START)
SND_SE_PLAY label far
public _snd_se_update
org (SHARED_FRAME_BASE + 033Ch - SHARED_CONTEXT_START)
_snd_se_update label far
public _bgimage_snap
org (SHARED_FRAME_BASE + 0388h - SHARED_CONTEXT_START)
_bgimage_snap label far
public _bgimage_free
org (SHARED_FRAME_BASE + 0426h - SHARED_CONTEXT_START)
_bgimage_free label far
public CDG_PUT_8
org (SHARED_FRAME_BASE + 0458h - SHARED_CONTEXT_START)
CDG_PUT_8 label far
public BGIMAGE_PUT_RECT_16
org (SHARED_FRAME_BASE + 083Ch - SHARED_CONTEXT_START)
BGIMAGE_PUT_RECT_16 label far
public @PI_LOAD$QINXC
org (SHARED_FRAME_BASE + 0AD8h - SHARED_CONTEXT_START)
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org (SHARED_FRAME_BASE + 0B0Ah - SHARED_CONTEXT_START)
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org (SHARED_FRAME_BASE + 0BBAh - SHARED_CONTEXT_START)
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org (SHARED_FRAME_BASE + 0BE0h - SHARED_CONTEXT_START)
@PI_FREE$QI label far
public @input_reset_sense_held$qv
org (SHARED_FRAME_BASE + 0D94h - SHARED_CONTEXT_START)
@input_reset_sense_held$qv label far
public @FRAME_DELAY$QI
org (SHARED_FRAME_BASE + 0E5Eh - SHARED_CONTEXT_START)
@FRAME_DELAY$QI label far
OP_CHARSELECT_SHARED_TEXT ends
OP_CHARSELECT_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_CHARSELECT_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _PaletteTone
org 054eh
_PaletteTone label word
public _VRAM_PLANE_B
org 0aa4h
_VRAM_PLANE_B label dword
org OWNED_DATA_START
_DATA ends

; The compiler supplies slb1.pi and all genuine selection state.
OP_CHARSELECT_DATA_TAIL segment byte public 'DATA' use16
public _resident
org (02dech - OWNED_DATA_END)
_resident label dword
public _vsync_Count1
org (02e4eh - OWNED_DATA_END)
_vsync_Count1 label word
public _key_det
org (03a92h - OWNED_DATA_END)
_key_det label word
public _cleared_with
org (05122h - OWNED_DATA_END)
_cleared_with label byte
org (OWNED_BSS_START - OWNED_DATA_END)
OP_CHARSELECT_DATA_TAIL ends

_BSS segment byte public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_CHARSELECT_DATA_TAIL, _BSS
end

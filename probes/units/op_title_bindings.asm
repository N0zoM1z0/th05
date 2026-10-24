; TH05 OP title original-address symbol-only context.
; No instruction bodies, filenames, images/music or source-owned state.
.386
.model large
; No .stack. The producer owns no BSS objects.
OP01_BASE equ 0a390h
UNIT_START equ 0bc0fh
UNIT_SIZE equ 026ah
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0d300h
SHARED_END equ 0e2cah
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 00f34h
OWNED_DATA_SIZE equ 009ah
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BYTEBOXFILL_X
org 0bach
GRCG_BYTEBOXFILL_X label far
public GRCG_SETCOLOR
org 0ee2h
GRCG_SETCOLOR label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019f0h
PALETTE_SHOW label far
org OP01_BASE
_TEXT ends

OP_TITLE_TEXT segment byte public 'CODE' use16
assume cs:OP_TITLE_TEXT
org (UNIT_START - OP01_BASE)
OP_TITLE_TEXT ends

OP_TITLE_CODE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
OP_TITLE_CODE_TAIL ends
op_01 group OP_TITLE_TEXT, OP_TITLE_CODE_TAIL

OP_TITLE_SHARED_TEXT segment para public 'CODE' use16
assume cs:OP_TITLE_SHARED_TEXT
public SND_LOAD
org 08beh
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 0976h
SND_KAJA_INTERRUPT label far
public @PI_PUT_MASKED_8$QIIII
org 0994h
@PI_PUT_MASKED_8$QIIII label far
public @PI_LOAD$QINXC
org 0ad8h
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org 0b0ah
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org 0bbah
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0be0h
@PI_FREE$QI label far
public @FRAME_DELAY$QI
org 0e5eh
@FRAME_DELAY$QI label far
public CDG_LOAD_SINGLE_NOALPHA
org 0e74h
CDG_LOAD_SINGLE_NOALPHA label far
public CDG_LOAD_SINGLE
org 0e7ah
CDG_LOAD_SINGLE label far
public CDG_LOAD_ALL
org 0f38h
CDG_LOAD_ALL label far
public CDG_FREE_ALL
org 0fcah
CDG_FREE_ALL label far
OP_TITLE_SHARED_TEXT ends
OP_TITLE_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_TITLE_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _PaletteTone
org 054eh
_PaletteTone label word
org OWNED_DATA_START
_DATA ends

OP_TITLE_DATA_TAIL segment byte public 'DATA' use16
public _resident
org (02dech - OWNED_DATA_END)
_resident label dword
OP_TITLE_DATA_TAIL ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_TITLE_DATA_TAIL, _BSS
end

; TH05 OP Music Room original-address symbol-only context.
; Foreign30-byte DS-copy helper has a label/extent, no imported body.
.386
.model large
; No .stack: the producer owns its full BSS state.
OP01_BASE equ 0a390h
PREFIX_START equ 0be79h
PREFIX_SIZE equ 017dh
FOREIGN_SIZE equ 001eh
SUFFIX_SIZE equ 07c1h
UNIT_END equ 0c7d5h
SHARED_FRAME_BASE equ 0d300h
SHARED_END equ 0e2cah
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 00fceh
OWNED_DATA_SIZE equ 01849h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 04d84h
OWNED_BSS_SIZE equ 002dch

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public FILE_CLOSE
org 0938h
FILE_CLOSE label far
public FILE_READ
org 09a4h
FILE_READ label far
public FILE_ROPEN
org 0a58h
FILE_ROPEN label far
public FILE_SEEK
org 0a94h
FILE_SEEK label far
public GRCG_HLINE
org 0c44h
GRCG_HLINE label far
public GRCG_POLYGON_C
org 0ccah
GRCG_POLYGON_C label far
public GRCG_SETCOLOR
org 0ee2h
GRCG_SETCOLOR label far
public GRCG_VLINE
org 0f12h
GRCG_VLINE label far
public GRAPH_CLEAR
org 01216h
GRAPH_CLEAR label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019f0h
PALETTE_SHOW label far
public IRAND
org 01c5eh
IRAND label far
public TEXT_CLEAR
org 020feh
TEXT_CLEAR label far
public HMEM_ALLOCBYTE
org 02322h
HMEM_ALLOCBYTE label far
public HMEM_FREE
org 02426h
HMEM_FREE label far
public PFSTART
org 037b8h
PFSTART label far
public PFEND
org 03858h
PFEND label far
org OP01_BASE
_TEXT ends

OP_MUSIC_PREFIX_TEXT segment byte public 'CODE' use16
assume cs:OP_MUSIC_PREFIX_TEXT
org (PREFIX_START - OP01_BASE)
OP_MUSIC_PREFIX_TEXT ends

OP_MUSIC_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:OP_MUSIC_FOREIGN_TEXT
public @nopoly_B_put$qv
@nopoly_B_put$qv label near
org FOREIGN_SIZE
OP_MUSIC_FOREIGN_TEXT ends

OP_MUSIC_SUFFIX_TEXT segment byte public 'CODE' use16
OP_MUSIC_SUFFIX_TEXT ends
op_01 group OP_MUSIC_PREFIX_TEXT, OP_MUSIC_FOREIGN_TEXT, OP_MUSIC_SUFFIX_TEXT

OP_MUSIC_SHARED_ALIGN segment byte public 'CODE' use16
org (SHARED_FRAME_BASE - UNIT_END)
OP_MUSIC_SHARED_ALIGN ends

OP_MUSIC_SHARED_TEXT segment word public 'CODE' use16
assume cs:OP_MUSIC_SHARED_TEXT
public GRAPH_PUTSA_FX
org 0136h
GRAPH_PUTSA_FX label far
public _bgimage_snap
org 0388h
_bgimage_snap label far
public _bgimage_free
org 0426h
_bgimage_free label far
public @POLAR$QIII
org 0534h
@POLAR$QIII label far
public @piano_setup_and_put_initial$qv
org 0594h
@piano_setup_and_put_initial$qv label far
public @piano_render$qv
org 066eh
@piano_render$qv label far
public BGIMAGE_PUT_RECT_16
org 083ch
BGIMAGE_PUT_RECT_16 label far
public SND_LOAD
org 08beh
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 0976h
SND_KAJA_INTERRUPT label far
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
public @input_reset_sense_held$qv
org 0d94h
@input_reset_sense_held$qv label far
public @FRAME_DELAY$QI
org 0e5eh
@FRAME_DELAY$QI label far
public CDG_FREE_ALL
org 0fcah
CDG_FREE_ALL label far
OP_MUSIC_SHARED_TEXT ends
OP_MUSIC_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_MUSIC_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _PaletteTone
org 054eh
_PaletteTone label word
public _SinTable8
org 0590h
_SinTable8 label word
public _CosTable8
org 0610h
_CosTable8 label word
public _graph_putsa_fx_func
org 09deh
_graph_putsa_fx_func label word
public _VRAM_PLANE_B
org 0aa4h
_VRAM_PLANE_B label dword
org OWNED_DATA_START
_DATA ends

OP_MUSIC_DATA_TAIL segment byte public 'DATA' use16
public _key_det
org (03a92h - OWNED_DATA_END)
_key_det label word
org (OWNED_BSS_START - OWNED_DATA_END)
OP_MUSIC_DATA_TAIL ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_MUSIC_DATA_TAIL, _BSS
end

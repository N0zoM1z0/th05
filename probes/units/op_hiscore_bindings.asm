; OP High Score view symbol-only context, original decoded load offsets.
; No instructions, filenames, table values, score records or dummy functions.
.386
.model large
; No .stack allocation: the compiler owns the complete BSS contribution.
OP01_BASE equ 0a390h
UNIT_START equ 0c8e2h
UNIT_SIZE equ 0583h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0d300h
SHARED_END equ 0e15eh
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 02818h
OWNED_DATA_SIZE equ 0035h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 05060h
OWNED_BSS_SIZE equ 00d7h
OWNED_BSS_END equ (OWNED_BSS_START + OWNED_BSS_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public FILE_CLOSE
org 0938h
FILE_CLOSE label far
public FILE_CREATE
org 0948h
FILE_CREATE label far
public FILE_EXIST
org 0988h
FILE_EXIST label far
public FILE_READ
org 09A4h
FILE_READ label far
public FILE_ROPEN
org 0A58h
FILE_ROPEN label far
public FILE_SEEK
org 0A94h
FILE_SEEK label far
public FILE_WRITE
org 0AD6h
FILE_WRITE label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019F0h
PALETTE_SHOW label far
public SUPER_ENTRY_BFNT
org 02656h
SUPER_ENTRY_BFNT label far
public SUPER_PUT
org 0292Ah
SUPER_PUT label far
public GRAPH_GAIJI_PUTS
org 03674h
GRAPH_GAIJI_PUTS label far
public GRAPH_GAIJI_PUTC
org 0371Eh
GRAPH_GAIJI_PUTC label far
org OP01_BASE
_TEXT ends

; These true near helpers precede the complete compiler-owned SCORE_TEXT body.
SCORE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_TEXT
public @SCOREDAT_DECODE$QV
org (0c7d5h - OP01_BASE)
@SCOREDAT_DECODE$QV label near
public @SCOREDAT_ENCODE$QV
org (0c87eh - OP01_BASE)
@SCOREDAT_ENCODE$QV label near
org (UNIT_START - OP01_BASE)
SCORE_TEXT ends

OP_HISCORE_CODE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
OP_HISCORE_CODE_TAIL ends
op_01 group SCORE_TEXT, OP_HISCORE_CODE_TAIL

OP_HISCORE_SHARED_TEXT segment para public 'CODE' use16
assume cs:OP_HISCORE_SHARED_TEXT
public SND_LOAD
org 08BEh
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 0976h
SND_KAJA_INTERRUPT label far
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
public @input_reset_sense_held$qv
org 0D94h
@input_reset_sense_held$qv label far
public @FRAME_DELAY$QI
org 0E5Eh
@FRAME_DELAY$QI label far
OP_HISCORE_SHARED_TEXT ends
OP_HISCORE_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_HISCORE_DGROUP_GAP ends

; The compiler supplies all seven natural filename/song strings.
_DATA segment word public 'DATA' use16
public _PaletteTone
org 054eh
_PaletteTone label word
org OWNED_DATA_START
_DATA ends

OP_HISCORE_DATA_TAIL segment byte public 'DATA' use16
public _resident
org (02dech - OWNED_DATA_END)
_resident label dword
public _key_det
org (03a92h - OWNED_DATA_END)
_key_det label word
org (OWNED_BSS_START - OWNED_DATA_END)
OP_HISCORE_DATA_TAIL ends

; Both full score sections, rank, cleared flags and extra_unlocked are owned
; by C++; no object is replaced by an address-only alias in this interval.
_BSS segment byte public 'BSS' use16
_BSS ends
OP_HISCORE_BSS_TAIL segment byte public 'BSS' use16
public _extra_playable_with
org (0513fh - OWNED_BSS_END)
_extra_playable_with label dword
OP_HISCORE_BSS_TAIL ends
DGROUP group _DATA, OP_HISCORE_DATA_TAIL, _BSS, OP_HISCORE_BSS_TAIL
end

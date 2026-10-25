; Whole menu312 atCC5C..CD94, no compiler-owned DATA/BSS or foreign bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN, PALETTE_BLACK_OUT, GRAPH_COPY_PAGE, PALETTE_SHOW
org 00600h
PALETTE_BLACK_IN label far
org 00644h
PALETTE_BLACK_OUT label far
org 01250h
GRAPH_COPY_PAGE label far
org 019f0h
PALETTE_SHOW label far
org 0a390h
_TEXT ends
SCORE_MENU_TEXT segment byte public 'CODE' use16
assume cs:SCORE_MENU_TEXT
public @rank_render$qv
org 0284ch
@rank_render$qv label near
org 028cch
SCORE_MENU_TEXT ends
OP_MENU_CODE_TAIL segment byte public 'CODE' use16
org 0056ch
OP_MENU_CODE_TAIL ends
op_01 group SCORE_MENU_TEXT, OP_MENU_CODE_TAIL
OP_MENU_SHARED_TEXT segment para public 'CODE' use16
assume cs:OP_MENU_SHARED_TEXT
public SND_LOAD, SND_KAJA_INTERRUPT, @PI_LOAD$QINXC, @PI_PUT_8$QIII
public @PI_PALETTE_APPLY$QI, @PI_FREE$QI
public @input_reset_sense_held$qv, @FRAME_DELAY$QI
org 008beh
SND_LOAD label far
org 00976h
SND_KAJA_INTERRUPT label far
org 00ad8h
@PI_LOAD$QINXC label far
org 00b0ah
@PI_PUT_8$QIII label far
org 00bbah
@PI_PALETTE_APPLY$QI label far
org 00be0h
@PI_FREE$QI label far
org 00d94h
@input_reset_sense_held$qv label far
org 00e5eh
@FRAME_DELAY$QI label far
OP_MENU_SHARED_TEXT ends
OP_MENU_DGROUP_GAP segment byte public 'CODE' use16
org 00e82h
OP_MENU_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _hi_filenames, _resident, _key_det
org 0054eh
_PaletteTone label word
org 02818h
_hi_filenames label byte
org 02dech
_resident label dword
org 03a92h
_key_det label word
org 03a94h
_DATA ends
_BSS segment word public 'BSS' use16
public _rank
; Actual rank byte remains foreign BSS, DS5121; no initializer supplied.
org 0168dh
_rank label byte
org 0168eh
_BSS ends
DGROUP group _DATA, _BSS
end

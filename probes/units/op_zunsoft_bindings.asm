; True foreign Master/SHARED frames and semantic state; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT, GRAPH_CLEAR, GRAPH_COPY_PAGE, PALETTE_SHOW
public IRAND, SUPER_FREE, SUPER_ENTRY_BFNT, SUPER_PUT_RECT
org 0644h
PALETTE_BLACK_OUT label far
org 01216h
GRAPH_CLEAR label far
org 01250h
GRAPH_COPY_PAGE label far
org 019f0h
PALETTE_SHOW label far
org 01c5eh
IRAND label far
org 024f2h
SUPER_FREE label far
org 02656h
SUPER_ENTRY_BFNT label far
org 02736h
SUPER_PUT_RECT label far
org 0a390h
_TEXT ends
OP_ZUNSOFT_PREFIX segment byte public 'CODE' use16
org (0b616h - 0a390h)
OP_ZUNSOFT_PREFIX ends
OP_ZUNSOFT_TEXT segment byte public 'CODE' use16
OP_ZUNSOFT_TEXT ends
OP_ZUNSOFT_TAIL segment byte public 'CODE' use16
org (0d300h - 0ba94h)
OP_ZUNSOFT_TAIL ends
op_01 group OP_ZUNSOFT_PREFIX, OP_ZUNSOFT_TEXT, OP_ZUNSOFT_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY, _snd_se_update, _bgimage_snap, _bgimage_put, _bgimage_free
public @POLAR$QIII, SND_LOAD, SND_KAJA_INTERRUPT
public @PI_LOAD$QINXC, @PI_PUT_8$QIII, @PI_PALETTE_APPLY$QI, @PI_FREE$QI
public @input_reset_sense_held$qv, SND_DELAY_UNTIL_MEASURE
org 0302h
SND_SE_PLAY label far
org 033ch
_snd_se_update label far
org 0388h
_bgimage_snap label far
org 03f0h
_bgimage_put label far
org 0426h
_bgimage_free label far
org 0534h
@POLAR$QIII label far
org 08beh
SND_LOAD label far
org 0976h
SND_KAJA_INTERRUPT label far
org 0ad8h
@PI_LOAD$QINXC label far
org 0b0ah
@PI_PUT_8$QIII label far
org 0bbah
@PI_PALETTE_APPLY$QI label far
org 0be0h
@PI_FREE$QI label far
org 0d94h
@input_reset_sense_held$qv label far
org 0df1h
SND_DELAY_UNTIL_MEASURE label far
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _SinTable8, _CosTable8
public _zun00_pi, _logo, _zun02_bft, _zun04_bft, _zun01_bft, _zun03_bft
public _Palettes, _vsync_Count1, _key_det, _zunsoft_palette, _pyros
org 054eh
_PaletteTone label word
org 0590h
_SinTable8 label word
org 0610h
_CosTable8 label word
org 0eeah
_zun00_pi label byte
org 0ef3h
_logo label byte
org 0ef8h
_zun02_bft label byte
org 0f02h
_zun04_bft label byte
org 0f0ch
_zun01_bft label byte
org 0f16h
_zun03_bft label byte
org 02e1eh
_Palettes label byte
org 02e4eh
_vsync_Count1 label word
org 03a92h
_key_det label word
org 03f54h
_zunsoft_palette label byte
org 03f84h
_pyros label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

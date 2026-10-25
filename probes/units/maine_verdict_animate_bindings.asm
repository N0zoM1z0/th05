; Real foreign symbols/extents only; owned compiler contribution remains empty.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public GRAPH_COPY_PAGE
org 0133Ch
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 01B8Ah
PALETTE_SHOW label far
org 0A540h
_TEXT ends
VERDICT_FMT_TEXT segment byte public 'CODE' use16
VERDICT_FMT_TEXT ends
VERDICT_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:VERDICT_FOREIGN_TEXT
public @verdict_main$qv
org 0255Bh
@verdict_main$qv label near
public @verdict_comments_put$qv
org 02C2Fh
@verdict_comments_put$qv label near
org 02C71h
VERDICT_FOREIGN_TEXT ends
VERDICT_ANIMATE_TEXT segment byte public 'CODE' use16
VERDICT_ANIMATE_TEXT ends
VERDICT_ANIMATE_TAIL segment byte public 'CODE' use16
org 015E3h
VERDICT_ANIMATE_TAIL ends
group_01 group VERDICT_FMT_TEXT, VERDICT_FOREIGN_TEXT, VERDICT_ANIMATE_TEXT, VERDICT_ANIMATE_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public @PI_LOAD$QINXC
org 0780h
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org 07B2h
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org 0862h
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0888h
@PI_FREE$QI label far
public @INPUT_WAIT_FOR_CHANGE$QI
org 0A18h
@INPUT_WAIT_FOR_CHANGE$QI label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
org 01910h
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _verdict_picture_filename
org 016F4h
_verdict_picture_filename label byte
org 050C3h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

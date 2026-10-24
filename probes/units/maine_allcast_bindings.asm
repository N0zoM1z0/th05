; Symbol-only original TH05 MAINE all-cast context. No game instructions,
; target bytes, data contents or source-owned BSS definitions. No .stack.
.386
.model large

GROUP01_BASE equ 0A540h
UNIT_START equ 0B273h
IFNDEF ALLCAST_CODE_SIZE
ALLCAST_CODE_SIZE equ 0263h
ENDIF
UNIT_END equ (UNIT_START + ALLCAST_CODE_SIZE)
SHARED_BASE equ 0E800h
SHARED_END equ (SHARED_BASE + 0A88h)
DGROUP_BASE equ 10110h
OWNED_BSS_START equ 04F0Eh

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public GRCG_BYTEBOXFILL_X
org 0C9Eh
GRCG_BYTEBOXFILL_X label far
public GRCG_SETCOLOR
org 0F28h
GRCG_SETCOLOR label far
public PALETTE_SHOW
org 01B8Ah
PALETTE_SHOW label far
org GROUP01_BASE
_TEXT ends

MAINE_01_TEXT segment word public 'CODE' use16
assume cs:MAINE_01_TEXT
public @screen_line_next_animate$qv
org 0C75h
@screen_line_next_animate$qv label near
org (UNIT_START - GROUP01_BASE)
MAINE_01_TEXT ends
group_01 group MAINE_01_TEXT

ALLCAST_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
ALLCAST_SHARED_GAP ends

ALLCAST_SHARED_TEXT segment word public 'CODE' use16
assume cs:ALLCAST_SHARED_TEXT
public SND_LOAD
org 0566h
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 061Eh
SND_KAJA_INTERRUPT label far
public @PI_PUT_QUARTER_MASKED_8$QIIIII
org 066Eh
@PI_PUT_QUARTER_MASKED_8$QIIIII label far
public @PI_LOAD$QINXC
org 0780h
@PI_LOAD$QINXC label far
public @PI_PUT_QUARTER_8$QIIII
org 07E2h
@PI_PUT_QUARTER_8$QIIII label far
public @PI_PALETTE_APPLY$QI
org 0862h
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0888h
@PI_FREE$QI label far
public _snd_bgm_measure
org 0A42h
_snd_bgm_measure label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
ALLCAST_SHARED_TEXT ends

ALLCAST_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
ALLCAST_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _page_shown
org 075Eh
_page_shown label byte
public _BG_FN
org 0760h
_BG_FN label byte
public _BG_QUARTER
org 07E0h
_BG_QUARTER label word
public _EXED
org 014E9h
_EXED label byte
public _resident
org 01D6Eh
_resident label dword
org OWNED_BSS_START
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Symbol-only TH05 MAINE cutscene context. No game/helper instructions,
; data values, target arrays or owner globals are supplied or credited.
; No .stack directive: source BSS must retain its real DGROUP offset.
.386
.model large

GROUP01_BASE equ 0a540h
UNIT_START equ 0a695h
; Actual expected compiler sizes: two complete functions before the boundary,
; then nine complete functions. A diagnostic verifies both real SEGDEF sizes.
IFNDEF CUTSCENE_FIRST_SIZE
CUTSCENE_FIRST_SIZE equ 06fh
ENDIF
IFNDEF CUTSCENE_AFTER_SIZE
CUTSCENE_AFTER_SIZE equ 0ab0h
ENDIF
UNACCEPTED_EGC_TAIL equ 1
CUTSCENE_LAYOUT_SPAN equ (CUTSCENE_FIRST_SIZE + UNACCEPTED_EGC_TAIL + CUTSCENE_AFTER_SIZE)
UNIT_END equ (UNIT_START + CUTSCENE_LAYOUT_SPAN)
SHARED_BASE equ 0e800h
SHARED_END equ (SHARED_BASE + 0C02h)
DGROUP_BASE equ 10110h
OWNED_BSS_START equ 02e88h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public EGC_ON
org 0824h
EGC_ON label far
public EGC_OFF
org 083Ah
EGC_OFF label far
public FILE_CLOSE
org 0946h
FILE_CLOSE label far
public FILE_READ
org 09B2h
FILE_READ label far
public FILE_ROPEN
org 0A66h
FILE_ROPEN label far
public FILE_SIZE
org 0AE4h
FILE_SIZE label far
public GRCG_BYTEBOXFILL_X
org 0C9Eh
GRCG_BYTEBOXFILL_X label far
public GRCG_SETCOLOR
org 0F28h
GRCG_SETCOLOR label far
public GRAPH_CLEAR
org 01302h
GRAPH_CLEAR label far
public GRAPH_COPY_PAGE
org 0133Ch
GRAPH_COPY_PAGE label far
public GRAPH_SCROLLUP
org 01A2Eh
GRAPH_SCROLLUP label far
public PALETTE_SHOW
org 01B8Ah
PALETTE_SHOW label far
public PALETTE_WHITE_IN
org 0243Ch
PALETTE_WHITE_IN label far
public PALETTE_WHITE_OUT
org 0247Ch
PALETTE_WHITE_OUT label far
public GRAPH_GAIJI_PUTC
org 038E6h
GRAPH_GAIJI_PUTC label far
public _tolower
org 045D3h
_tolower label far
org GROUP01_BASE
_TEXT ends

CUTSCENE_TEXT segment word public 'CODE' use16
assume cs:CUTSCENE_TEXT
org (UNIT_START - GROUP01_BASE)
CUTSCENE_TEXT ends

; This separate contribution starts after EGC's real compiler RET. The byte
; lies inside the wholly unaccepted original EGC range; it is never compared
; or credited as part of either complete compiler-owned function.
CUTSCENE_AFTER_TEXT segment byte public 'CODE' use16
org UNACCEPTED_EGC_TAIL
CUTSCENE_AFTER_TEXT ends
group_01 group CUTSCENE_TEXT, CUTSCENE_AFTER_TEXT

CUTSCENE_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
CUTSCENE_SHARED_GAP ends

CUTSCENE_SHARED_TEXT segment para public 'CODE' use16
assume cs:CUTSCENE_SHARED_TEXT
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
public _snd_se_reset
org 02DAh
_snd_se_reset label far
public SND_SE_PLAY
org 02E6h
SND_SE_PLAY label far
public _snd_se_update
org 0320h
_snd_se_update label far
public _bgimage_snap
org 036Ch
_bgimage_snap label far
public _bgimage_free
org 040Ah
_bgimage_free label far
public BGIMAGE_PUT_RECT_16
org 04E4h
BGIMAGE_PUT_RECT_16 label far
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
public @PI_PUT_8$QIII
org 07B2h
@PI_PUT_8$QIII label far
public @PI_PUT_QUARTER_8$QIIII
org 07E2h
@PI_PUT_QUARTER_8$QIIII label far
public @PI_PALETTE_APPLY$QI
org 0862h
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0888h
@PI_FREE$QI label far
public @input_reset_sense_held$qv
org 0A08h
@input_reset_sense_held$qv label far
public SND_DELAY_UNTIL_MEASURE
org 0A65h
SND_DELAY_UNTIL_MEASURE label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
public @EGC_COPY_RECT_1_TO_0_16$QIIII
org 0C02h
@EGC_COPY_RECT_1_TO_0_16$QIIII label far
CUTSCENE_SHARED_TEXT ends

CUTSCENE_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
CUTSCENE_DGROUP_GAP ends

; No initialized DATA belongs to this owner. Foreign labels and the gap stop
; before the entire compiler-owned BSS contribution at DGROUP2E88.
_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _graph_putsa_fx_func
org 06BCh
_graph_putsa_fx_func label word
public _VRAM_PLANE_B
org 071Eh
_VRAM_PLANE_B label dword
public _colmap_count
org 0730h
_colmap_count label byte
public _BOX_MASKS
org 0732h
_BOX_MASKS label byte
public _CUTSCENE_KANJI
org 075Ah
_CUTSCENE_KANJI label dword
public __ctype
org 01A38h
__ctype label byte
public _key_det
org 029FAh
_key_det label word
org OWNED_BSS_START
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

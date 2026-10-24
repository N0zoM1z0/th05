; Symbol-only MAINE entry context. Original decoded addresses, no game code
; or data values are supplied. All holes surround complete source-owned CODE,
; DATA and BSS contributions. No .stack may displace the source BSS.
.386
.model large

GROUP01_BASE equ 0a540h
UNIT_START equ 0a545h
UNIT_SIZE equ 0150h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0e800h
SHARED_END equ 0f3f4h
DGROUP_BASE equ 10110h
OWNED_DATA_START equ 0090h
OWNED_DATA_SIZE equ 002bh
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 01d6eh

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_CLOSE
org 0946h
FILE_CLOSE label far
public FILE_READ
org 09B2h
FILE_READ label far
public FILE_ROPEN
org 0A66h
FILE_ROPEN label far
public GRAPH_HIDE
org 013E8h
GRAPH_HIDE label far
public GRAPH_SHOW
org 01A86h
GRAPH_SHOW label far
public TEXT_CLEAR
org 02298h
TEXT_CLEAR label far
public _execl
org 09DC9h
_execl label far
org GROUP01_BASE
_TEXT ends

MAINE_E_TEXT segment word public 'CODE' use16
assume cs:MAINE_E_TEXT
org (UNIT_START - GROUP01_BASE)
MAINE_E_TEXT ends

; A distinct byte-aligned segment follows the entire 336-byte entry owner.
MAINE_ENTRY_NEAR_TAIL segment byte public 'CODE' use16
assume cs:MAINE_ENTRY_NEAR_TAIL
public @CUTSCENE_SCRIPT_LOAD$QNXC
org (0A695h - UNIT_END)
@CUTSCENE_SCRIPT_LOAD$QNXC label near
public @cutscene_animate$qv
org (0AFD6h - UNIT_END)
@cutscene_animate$qv label near
public @allcast_animate$qv
org (0B3CBh - UNIT_END)
@allcast_animate$qv label near
public @regist_menu$qv
org (0C1DDh - UNIT_END)
@regist_menu$qv label near
public @verdict_animate$qv
org (0D1B1h - UNIT_END)
@verdict_animate$qv label near
public @staffroll_animate$qv
org (0E422h - UNIT_END)
@staffroll_animate$qv label near
org (SHARED_BASE - UNIT_END)
MAINE_ENTRY_NEAR_TAIL ends
group_01 group MAINE_E_TEXT, MAINE_ENTRY_NEAR_TAIL

MAINE_ENTRY_SHARED_TEXT segment para public 'CODE' use16
assume cs:MAINE_ENTRY_SHARED_TEXT
public SND_DETERMINE_MODES
org (0E87Eh - SHARED_BASE)
SND_DETERMINE_MODES label far
public @game_exit$qv
org (0EC3Ch - SHARED_BASE)
@game_exit$qv label far
public SND_LOAD
org (0ED66h - SHARED_BASE)
SND_LOAD label far
public SND_KAJA_INTERRUPT
org (0EE1Eh - SHARED_BASE)
SND_KAJA_INTERRUPT label far
public @GAME_INIT_MAIN$QNXUC
org (0F0BAh - SHARED_BASE)
@GAME_INIT_MAIN$QNXUC label far
public @FRAME_DELAY$QI
org (0F288h - SHARED_BASE)
@FRAME_DELAY$QI label far
public CDG_FREE_ALL
org (0F3F4h - SHARED_BASE)
CDG_FREE_ALL label far
MAINE_ENTRY_SHARED_TEXT ends

MAINE_ENTRY_DS_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
MAINE_ENTRY_DS_GAP ends

; The compiler supplies SCRIPT_FN and every literal, including the natural
; UTF-8 archive filename staged to CP932 and its actual far-pointer fixup.
_DATA segment word public 'DATA' use16
org OWNED_DATA_START
_DATA ends

MAINE_ENTRY_DATA_TAIL segment byte public 'DATA' use16
public _random_seed, _mem_assign_paras
org (0276h - OWNED_DATA_END)
_random_seed label dword
org (06cah - OWNED_DATA_END)
_mem_assign_paras label word
org (OWNED_BSS_START - OWNED_DATA_END)
MAINE_ENTRY_DATA_TAIL ends

; Source-owned resident_t far *resident occupies DGROUP[1D6E,1D72).
; No duplicate _resident symbol or initialized pointer is supplied here.
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, MAINE_ENTRY_DATA_TAIL, _BSS
end

; OP startup/menu symbol-only context. Decoded load-module addresses only.
; No code/data values, target strings, helper instructions or dummy functions.
; The compiler owns the whole CODE, DATA and BSS contributions. All ORG holes
; are in separate contributions before/after those complete extents.
.386
.model large
; No artificial stack allocation: source-owned BSS retains original offsets.

OP01_BASE equ 0a390h
UNIT_START equ 0a39ch
UNIT_SIZE equ 0cdbh
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0d300h
SHARED_END equ 0e2d8h
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 0090h
OWNED_DATA_SIZE equ 0441h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)
OWNED_BSS_START equ 02dech
OWNED_BSS_SIZE equ 000ah
OWNED_BSS_END equ (OWNED_BSS_START + OWNED_BSS_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public DOS_PUTS2
org 0796h
DOS_PUTS2 label far
public GRCG_SETCOLOR
org 0EE2h
GRCG_SETCOLOR label far
public GRAPH_COPY_PAGE
org 01250h
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 019F0h
PALETTE_SHOW label far
public TEXT_CLEAR
org 020FEh
TEXT_CLEAR label far
public RESPAL_CREATE
org 02B18h
RESPAL_CREATE label far
public RESPAL_FREE
org 02B8Eh
RESPAL_FREE label far
public _strlen
org 05D99h
_strlen label far
public _execl
org 09BEDh
_execl label far
public _getch
org 0A002h
_getch label far
org OP01_BASE
_TEXT ends

OP_MAIN_TEXT segment word public 'CODE' use16
assume cs:OP_MAIN_TEXT
org (UNIT_START - OP01_BASE)
OP_MAIN_TEXT ends

; This tail starts after the entire compiler-owned 3291-byte menu body.
OP_MENU_CODE_TAIL segment byte public 'CODE' use16
assume cs:OP_MENU_CODE_TAIL
public @setup_menu$qv
org (0B5A6h - UNIT_END)
@setup_menu$qv label near
public @zunsoft_animate$qv
org (0B806h - UNIT_END)
@zunsoft_animate$qv label near
public @cfg_load$qv
org (0BA94h - UNIT_END)
@cfg_load$qv label near
public @cfg_save$qv
org (0BB0Eh - UNIT_END)
@cfg_save$qv label near
public @cfg_save_exit$qv
org (0BB91h - UNIT_END)
@cfg_save_exit$qv label near
public @main_cdg_load$qv
org (0BC0Fh - UNIT_END)
@main_cdg_load$qv label near
public @main_cdg_free$qv
org (0BC83h - UNIT_END)
@main_cdg_free$qv label near
public @op_animate$qv
org (0BC8Dh - UNIT_END)
@op_animate$qv label near
public @musicroom_menu$qv
org (0C490h - UNIT_END)
@musicroom_menu$qv label near
public @regist_view_menu$qv
org (0CC5Ch - UNIT_END)
@regist_view_menu$qv label near
public @cleardata_and_regist_view_sprite$qv
org (0CD94h - UNIT_END)
@cleardata_and_regist_view_sprite$qv label near
public @playchar_menu$qv
org (0D12Dh - UNIT_END)
@playchar_menu$qv label near
org (SHARED_BASE - UNIT_END)
OP_MENU_CODE_TAIL ends
op_01 group OP_MAIN_TEXT, OP_MENU_CODE_TAIL

OP_MENU_SHARED_TEXT segment para public 'CODE' use16
assume cs:OP_MENU_SHARED_TEXT
public SND_DETERMINE_MODES
org (0D380h - SHARED_BASE)
SND_DETERMINE_MODES label far
public @game_exit_to_dos$qv
org (0D41Ch - SHARED_BASE)
@game_exit_to_dos$qv label far
public GRAPH_PUTSA_FX
org (0D436h - SHARED_BASE)
GRAPH_PUTSA_FX label far
public _snd_se_reset
org (0D5F6h - SHARED_BASE)
_snd_se_reset label far
public SND_SE_PLAY
org (0D602h - SHARED_BASE)
SND_SE_PLAY label far
public _snd_se_update
org (0D63Ch - SHARED_BASE)
_snd_se_update label far
public CDG_PUT_8
org (0D758h - SHARED_BASE)
CDG_PUT_8 label far
public @game_exit$qv
org (0D7ECh - SHARED_BASE)
@game_exit$qv label far
public SND_LOAD
org (0DBBEh - SHARED_BASE)
SND_LOAD label far
public SND_KAJA_INTERRUPT
org (0DC76h - SHARED_BASE)
SND_KAJA_INTERRUPT label far
public @PI_LOAD$QINXC
org (0DDD8h - SHARED_BASE)
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org (0DE0Ah - SHARED_BASE)
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org (0DEBAh - SHARED_BASE)
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org (0DEE0h - SHARED_BASE)
@PI_FREE$QI label far
public @game_init_op$qnxuc
org (0DF12h - SHARED_BASE)
@game_init_op$qnxuc label far
public @input_reset_sense_held$qv
org (0E094h - SHARED_BASE)
@input_reset_sense_held$qv label far
public CDG_PUT_NOCOLORS_8
org (0E114h - SHARED_BASE)
CDG_PUT_NOCOLORS_8 label far
public @FRAME_DELAY$QI
org (0E15Eh - SHARED_BASE)
@FRAME_DELAY$QI label far
public @EGC_COPY_RECT_1_TO_0_16$QIIII
org (0E2D8h - SHARED_BASE)
@EGC_COPY_RECT_1_TO_0_16$QIIII label far
OP_MENU_SHARED_TEXT ends

OP_MENU_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_END)
OP_MENU_DGROUP_GAP ends

; Prefix only: the compiler supplies all 1089 initialized bytes, including
; every real far pointer and readable CP932-staged string. No owner globals
; are declared in this object.
_DATA segment word public 'DATA' use16
org OWNED_DATA_START
_DATA ends

; Low external DATA symbols; then extend only the foreign tail up to the
; real start of compiler-owned BSS. No bytes are placed in source-owned DATA.
OP_MENU_DATA_TAIL segment byte public 'DATA' use16
public _PaletteTone
org (054Eh - OWNED_DATA_END)
_PaletteTone label word
public _graph_putsa_fx_func
org (09DEh - OWNED_DATA_END)
_graph_putsa_fx_func label word
public _mem_assign_paras
org (09ECh - OWNED_DATA_END)
_mem_assign_paras label word
org (OWNED_BSS_START - OWNED_DATA_END)
OP_MENU_DATA_TAIL ends

; Empty prefix: source BSS naturally follows the DATA tails at DGROUP2DEC.
; Resident, in_option, callback and static input flags remain compiler-owned.
_BSS segment word public 'BSS' use16
_BSS ends

OP_MENU_BSS_TAIL segment byte public 'BSS' use16
public _key_det
org (03A92h - OWNED_BSS_END)
_key_det label word
public _extra_unlocked
org (05136h - OWNED_BSS_END)
_extra_unlocked label byte
public _extra_playable_with
org (0513Fh - OWNED_BSS_END)
_extra_playable_with label dword
OP_MENU_BSS_TAIL ends
DGROUP group _DATA, OP_MENU_DATA_TAIL, _BSS, OP_MENU_BSS_TAIL
end

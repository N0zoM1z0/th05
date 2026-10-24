; Stage initialization symbol-only context. No target instructions or data
; values are supplied. Every ORG hole is outside the complete C++ CODE/DATA
; contributions. Source owns all 1510 CODE bytes and 189 DATA bytes separately;
; this scaffold alone grants no ownership/exactness credit. In particular it
; does not define _boss_phase_timed_out or copy any filename literal.
.386
.model large
.stack 80h

MASTER_TEXT_END equ 0ae10h
UNIT_START equ 144c3h
UNIT_SIZE equ 05e6h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 14ab0h
SHARED_END equ (SHARED_BASE + 0726h)
CALLBACK_BASE equ 15270h
CALLBACK_END equ (CALLBACK_BASE + 0a512h)
DS_BASE equ 209d0h
OWNED_DATA_START equ 01fc8h
OWNED_DATA_SIZE equ 0bdh
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE, SUPER_ENTRY_BFNT
org 0291eh
HMEM_FREE label far
org 02d16h
SUPER_ENTRY_BFNT label far
org MASTER_TEXT_END
_TEXT ends

main_01_TEXT segment word public 'CODE' use16
assume cs:main_01_TEXT
public @SARA_BACKDROP_COLORFILL$QV
org (0BEF4h - MASTER_TEXT_END)
@SARA_BACKDROP_COLORFILL$QV label near
public @MAI_YUKI_BACKDROP_COLORFILL$QV
org (0BF24h - MASTER_TEXT_END)
@MAI_YUKI_BACKDROP_COLORFILL$QV label near
public @ALICE_BACKDROP_COLORFILL$QV
org (0C41Eh - MASTER_TEXT_END)
@ALICE_BACKDROP_COLORFILL$QV label near
public @YUMEKO_BACKDROP_COLORFILL$QV
org (0C42Ch - MASTER_TEXT_END)
@YUMEKO_BACKDROP_COLORFILL$QV label near
public @SHINKI_STAGE_BACKDROP_COLORFILL$QV
org (0C68Ah - MASTER_TEXT_END)
@SHINKI_STAGE_BACKDROP_COLORFILL$QV label near
public NULLFUNC_NEAR
org (0C73Eh - MASTER_TEXT_END)
NULLFUNC_NEAR label near
public NULLFUNC_FAR
org (0C740h - MASTER_TEXT_END)
NULLFUNC_FAR label far
public SELECT_FOR_RANK
org (0CFB2h - MASTER_TEXT_END)
SELECT_FOR_RANK label far
public @MIDBOSS1_RENDER$QV
org (0DAE1h - MASTER_TEXT_END)
@MIDBOSS1_RENDER$QV label near
public @MIDBOSS2_RENDER$QV
org (0DBA1h - MASTER_TEXT_END)
@MIDBOSS2_RENDER$QV label near
public @MIDBOSS4_RENDER$QV
org (0DC28h - MASTER_TEXT_END)
@MIDBOSS4_RENDER$QV label near
public @MIDBOSSX_RENDER$QV
org (0DD2Ah - MASTER_TEXT_END)
@MIDBOSSX_RENDER$QV label near
public @MIDBOSS5_RENDER$QV
org (0DD8Fh - MASTER_TEXT_END)
@MIDBOSS5_RENDER$QV label near
public @BB_LOAD$QNXC
org (0F930h - MASTER_TEXT_END)
@BB_LOAD$QNXC label near
public @MAI_YUKI_FG_RENDER$QV
org (01081Dh - MASTER_TEXT_END)
@MAI_YUKI_FG_RENDER$QV label near
public @SARA_BG_RENDER$QV
org (010A17h - MASTER_TEXT_END)
@SARA_BG_RENDER$QV label near
public @LOUISE_BG_RENDER$QV
org (010A7Fh - MASTER_TEXT_END)
@LOUISE_BG_RENDER$QV label near
public @ALICE_BG_RENDER$QV
org (010B0Bh - MASTER_TEXT_END)
@ALICE_BG_RENDER$QV label near
public @MAI_YUKI_BG_RENDER$QV
org (010B97h - MASTER_TEXT_END)
@MAI_YUKI_BG_RENDER$QV label near
public @YUMEKO_BG_RENDER$QV
org (010C29h - MASTER_TEXT_END)
@YUMEKO_BG_RENDER$QV label near
public @SHINKI_BG_RENDER$QV
org (011411h - MASTER_TEXT_END)
@SHINKI_BG_RENDER$QV label near
public @EXALICE_BG_RENDER$QV
org (011666h - MASTER_TEXT_END)
@EXALICE_BG_RENDER$QV label near
public @STAGE2_INVALIDATE$QV
org (0116CDh - MASTER_TEXT_END)
@STAGE2_INVALIDATE$QV label near
public @STAGE2_UPDATE$QV
org (0118ECh - MASTER_TEXT_END)
@STAGE2_UPDATE$QV label near
public @EXALICE_FG_RENDER$QV
org (011CADh - MASTER_TEXT_END)
@EXALICE_FG_RENDER$QV label near
public @SHINKI_FG_RENDER$QV
org (013066h - MASTER_TEXT_END)
@SHINKI_FG_RENDER$QV label near
public @MIDBOSS3_RENDER$QV
org (013106h - MASTER_TEXT_END)
@MIDBOSS3_RENDER$QV label near
public @SARA_FG_RENDER$QV
org (0140C4h - MASTER_TEXT_END)
@SARA_FG_RENDER$QV label near
public @LOUISE_FG_RENDER$QV
org (014163h - MASTER_TEXT_END)
@LOUISE_FG_RENDER$QV label near
public @ALICE_FG_RENDER$QV
org (014354h - MASTER_TEXT_END)
@ALICE_FG_RENDER$QV label near
public @YUMEKO_FG_RENDER$QV
org (014422h - MASTER_TEXT_END)
@YUMEKO_FG_RENDER$QV label near
org (UNIT_START - MASTER_TEXT_END)
main_01_TEXT ends

; Separate byte-aligned segment after the complete 1510-byte compiler body.
STAGE_SETUP_CODE_TAIL segment byte public 'CODE' use16
assume cs:STAGE_SETUP_CODE_TAIL
public @LOUISE_BACKDROP_COLORFILL$QV
org (014AAAh - UNIT_END)
@LOUISE_BACKDROP_COLORFILL$QV label near
org (SHARED_BASE - UNIT_END)
STAGE_SETUP_CODE_TAIL ends
main_01 group main_01_TEXT, STAGE_SETUP_CODE_TAIL

SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_LOAD_ALL_NOALPHA
org 0726h
CDG_LOAD_ALL_NOALPHA label far
SHARED ends

STAGE_SETUP_FAR_GAP segment byte public 'CODE' use16
org (CALLBACK_BASE - SHARED_END)
STAGE_SETUP_FAR_GAP ends

STAGE_SETUP_CALLBACK_TEXT segment para public 'CODE' use16
assume cs:STAGE_SETUP_CALLBACK_TEXT
public @MIDBOSS1_UPDATE$QV
org (015B9Bh - CALLBACK_BASE)
@MIDBOSS1_UPDATE$QV label far
public @MIDBOSS2_UPDATE$QV
org (015DEBh - CALLBACK_BASE)
@MIDBOSS2_UPDATE$QV label far
public @MIDBOSS4_UPDATE$QV
org (01620Fh - CALLBACK_BASE)
@MIDBOSS4_UPDATE$QV label far
public @MIDBOSSX_UPDATE$QV
org (0165B6h - CALLBACK_BASE)
@MIDBOSSX_UPDATE$QV label far
public @MIDBOSS5_UPDATE$QV
org (0168F2h - CALLBACK_BASE)
@MIDBOSS5_UPDATE$QV label far
public @explosions_small_reset$qv
org (0176CEh - CALLBACK_BASE)
@explosions_small_reset$qv label far
public @MAI_YUKI_UPDATE$QV
org (017FDBh - CALLBACK_BASE)
@MAI_YUKI_UPDATE$QV label far
public @EXALICE_UPDATE$QV
org (01A24Ah - CALLBACK_BASE)
@EXALICE_UPDATE$QV label far
public @SHINKI_UPDATE$QV
org (01B6DBh - CALLBACK_BASE)
@SHINKI_UPDATE$QV label far
public @MIDBOSS3_UPDATE$QV
org (01BD02h - CALLBACK_BASE)
@MIDBOSS3_UPDATE$QV label far
public @SARA_UPDATE$QV
org (01D66Fh - CALLBACK_BASE)
@SARA_UPDATE$QV label far
public @LOUISE_UPDATE$QV
org (01DD40h - CALLBACK_BASE)
@LOUISE_UPDATE$QV label far
public @ALICE_UPDATE$QV
org (01E996h - CALLBACK_BASE)
@ALICE_UPDATE$QV label far
public @YUMEKO_UPDATE$QV
org (01F782h - CALLBACK_BASE)
@YUMEKO_UPDATE$QV label far
STAGE_SETUP_CALLBACK_TEXT ends

STAGE_SETUP_DS_GAP segment byte public 'CODE' use16
org (DS_BASE - CALLBACK_END)
STAGE_SETUP_DS_GAP ends

; Compiler-owned flag + filename literals follow this prefix naturally.
; None of their 189 bytes are supplied by this object.
_DATA segment word public 'DATA' use16
org OWNED_DATA_START
_DATA ends

; External globals follow the whole compiler DATA contribution in a distinct
; byte-aligned segment. No labels may be inserted into its source-owned span.
STAGE_SETUP_DATA_TAIL segment byte public 'DATA' use16
org (0371Ah - OWNED_DATA_END)
public _boss_sprite_left
_boss_sprite_left label word
org (0371Ch - OWNED_DATA_END)
public _boss_sprite_right
_boss_sprite_right label word
org (0371Eh - OWNED_DATA_END)
public _boss_sprite_stay
_boss_sprite_stay label word
org (04446h - OWNED_DATA_END)
public _boss_backdrop_colorfill
_boss_backdrop_colorfill label word
org (04A86h - OWNED_DATA_END)
public _stage_invalidate
_stage_invalidate label word
org (04A88h - OWNED_DATA_END)
public _stage_render
_stage_render label word
org (05AA4h - OWNED_DATA_END)
public _midboss
_midboss label byte
org (05ABAh - OWNED_DATA_END)
public _boss
_boss label byte
org (05AD2h - OWNED_DATA_END)
public _boss2
_boss2 label byte
public _yuki
_yuki label byte
org (0C4B4h - OWNED_DATA_END)
public _midboss_update_func
_midboss_update_func label dword
org (0C4B8h - OWNED_DATA_END)
public _midboss_render_func
_midboss_render_func label word
org (0C672h - OWNED_DATA_END)
public _boss_update
_boss_update label dword
org (0C676h - OWNED_DATA_END)
public _boss_fg_render
_boss_fg_render label word
org (0C678h - OWNED_DATA_END)
public _boss_custombullets_render
_boss_custombullets_render label word
org (0C67Ah - OWNED_DATA_END)
public _boss_bg_render_func
_boss_bg_render_func label word
org (0C67Ch - OWNED_DATA_END)
public _boss_update_func
_boss_update_func label dword
org (0C680h - OWNED_DATA_END)
public _boss_fg_render_func
_boss_fg_render_func label word
org (0C682h - OWNED_DATA_END)
public _boss_statebyte
_boss_statebyte label byte
org (0C692h - OWNED_DATA_END)
public _bb_boss_seg
_bb_boss_seg label word
org (0C694h - OWNED_DATA_END)
public _boss_hitbox_radius
_boss_hitbox_radius label dword
STAGE_SETUP_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, STAGE_SETUP_DATA_TAIL, _BSS
end

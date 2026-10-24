; Symbol-only context for the complete maintained 1806-byte HUD overlay unit.
; No instructions, target bytes, external strings or dummy functions are emitted.
; All ORG extents precede or follow the credited C++ contribution. The observed
; main_01 frame must stay 0AE1: the near titles callback is naturally 711Dh.
.386
.model large
.stack 80h

MASTER_TEXT_END equ 0ae10h
UNIT_START equ 11d50h
UNIT_SIZE equ 070eh
UNIT_END equ (UNIT_START + UNIT_SIZE)
HUD_POINTS_SEGMENT_BASE equ 15270h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTCA, GAIJI_PUTSA, TEXT_PUTCA, TEXT_PUTSA, _strlen
org 1d7ah
GAIJI_PUTCA label far
org 1dbeh
GAIJI_PUTSA label far
org 2540h
TEXT_PUTCA label far
org 2598h
TEXT_PUTSA label far
org 684dh
_strlen label far
org MASTER_TEXT_END
_TEXT ends

HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
public TILES_INVALIDATE_AROUND, @grcg_setmode_rmw$qv
public @grcg_setcolor_direct_raw$qv, NULLFUNC_NEAR
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1, @bb_txt_put_8_raw$quiui
org (0bad2h - MASTER_TEXT_END)
TILES_INVALIDATE_AROUND label near
org (0c1f8h - MASTER_TEXT_END)
@grcg_setmode_rmw$qv label near
org (0c204h - MASTER_TEXT_END)
@grcg_setcolor_direct_raw$qv label near
org (0c73eh - MASTER_TEXT_END)
NULLFUNC_NEAR label near
org (0df28h - MASTER_TEXT_END)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (0e51ah - MASTER_TEXT_END)
@bb_txt_put_8_raw$quiui label near
org (UNIT_START - MASTER_TEXT_END)
HUD_OVRL_TEXT ends
main_01 group HUD_OVRL_TEXT

; The compiler contributes the entire UNIT_SIZE before this gap begins. The
; far HUD points helper belongs to its actual independent 1527 frame; there
; is no alias to frame zero and no padding inside HUD_OVRL_TEXT's C++ body.
HUD_POINTS_BINDING_GAP segment word public 'CODE' use16
org (HUD_POINTS_SEGMENT_BASE - UNIT_END)
HUD_POINTS_BINDING_GAP ends

HUD_POINTS_BINDING_TEXT segment word public 'CODE' use16
assume cs:HUD_POINTS_BINDING_TEXT
public @HUD_POINTS_PUT$QUIUIUL
org 0654h
@HUD_POINTS_PUT$QUIUIUL label far
HUD_POINTS_BINDING_TEXT ends

; DS-relative positions only. Declarations, widths and ownership remain in
; the maintained HUD headers; these labels allocate no data or string bytes.
_DATA segment word public 'DATA' use16
public _overlay_fade, _boss_bgm_frame, _popup_frame
public _gStage_1, _gFINAL_STAGE, _gEXTRA_STAGE, _POPUP_STRINGS
public _dissolve_sprite, _PLAYFIELD_BLANK_ROW, _gDEMO_PLAY
public _tile_invalidate_box, _resident
public _stage_title_len, _stage_bgm_title_len, _boss_bgm_title_len
public _popup_gaiji_len, _popup_id_cur, _popup_dest_reached, _popup_shiftbuf
public _popup_cur_tram_left, _popup_dest_tram_left, _overlay_popup_id_new
public _overlay1, _overlay2, _titles_frame, _overlay_popup_bonus
public _stage_title, _stage_bgm_title, _boss_bgm_title, _stage_id
org 19ach
_overlay_fade label byte
org 19adh
_boss_bgm_frame label byte
org 19aeh
_popup_frame label byte
org 19b2h
_gStage_1 label byte
org 19bah
_gFINAL_STAGE label byte
org 19c6h
_gEXTRA_STAGE label byte
org 19fah
_POPUP_STRINGS label dword
org 1a0eh
_dissolve_sprite label byte
org 1a10h
_PLAYFIELD_BLANK_ROW label dword
org 1a14h
_gDEMO_PLAY label byte
org 3502h
_tile_invalidate_box label word
org 41fch
_resident label dword
org 4aa0h
_stage_title_len label word
org 4aa2h
_stage_bgm_title_len label word
org 4aa4h
_boss_bgm_title_len label word
org 4aa6h
_popup_gaiji_len label word
org 4aa8h
_popup_id_cur label byte
org 4aa9h
_popup_dest_reached label byte
org 4aaah
_popup_shiftbuf label byte
org 4ab8h
_popup_cur_tram_left label word
org 4abah
_popup_dest_tram_left label word
org 4abdh
_overlay_popup_id_new label byte
org 4abeh
_overlay1 label word
org 4ac0h
_overlay2 label word
org 4ac2h
_titles_frame label byte
org 4ac4h
_overlay_popup_bonus label dword
org 4ac8h
_stage_title label dword
org 4acch
_stage_bgm_title label dword
org 4ad0h
_boss_bgm_title label dword
org 576eh
_stage_id label byte
_DATA ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

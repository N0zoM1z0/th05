; One immutable symbol-only source, assembled before and after actual C++.
; True far APIs, actual addresses and public SEGDEF; no owned bytes supplied.
.386
.model large
UNIT_START equ 0b237h
UNIT_END equ 0b55ah
ifdef BINDINGS_AFTER
STAGE_SESSION_TEXT segment byte public 'CODE' use16
assume cs:STAGE_SESSION_TEXT
public @stage_runtime_init$qv
org (0b55ah - UNIT_END)
@stage_runtime_init$qv label near
public @demo_load$qv
org (0b756h - UNIT_END)
@demo_load$qv label near
public @DemoPlay$qv
org (0b7b4h - UNIT_END)
@DemoPlay$qv label near
public @bomb_bg_load__ems_preload_playch$qv
org (0b8c1h - UNIT_END)
@bomb_bg_load__ems_preload_playch$qv label near
public @EMS_PRELOAD_BOSS_FACESET$QNXC
org (0b9cch - UNIT_END)
@EMS_PRELOAD_BOSS_FACESET$QNXC label near
public @eyecatch_animate$qv
org (0ba66h - UNIT_END)
@eyecatch_animate$qv label near
public TILES_FILL_INITIAL
org (0bb9eh - UNIT_END)
TILES_FILL_INITIAL label near
public @TILES_RENDER_ALL$QV
org (0bbech - UNIT_END)
@TILES_RENDER_ALL$QV label near
public @tiles_activate$qv
org (0bd8fh - UNIT_END)
@tiles_activate$qv label far
public NULLFUNC_NEAR
org (0c73eh - UNIT_END)
NULLFUNC_NEAR label near
public @std_load$qv
org (0c742h - UNIT_END)
@std_load$qv label near
public @hud_put$qv
org (0d323h - UNIT_END)
@hud_put$qv label far
public BB_CHEETO_LOAD
org (0de58h - UNIT_END)
BB_CHEETO_LOAD label near
public @shot_level_update$qv
org (0e3e2h - UNIT_END)
@shot_level_update$qv label far
public MPN_LOAD
org (0e57ch - UNIT_END)
MPN_LOAD label near
public @map_load$qv
org (0e5c2h - UNIT_END)
@map_load$qv label near
public BB_PLAYCHAR_LOAD
org (010432h - UNIT_END)
BB_PLAYCHAR_LOAD label near
public @clear_blue_vram_pages$qv
org (0105cah - UNIT_END)
@clear_blue_vram_pages$qv label near
public @SHINKI_BG_RENDER$QV
org (011411h - UNIT_END)
@SHINKI_BG_RENDER$QV label near
public @overlay_wipe$qv
org (011d50h - UNIT_END)
@overlay_wipe$qv label near
public @overlay_black$qv
org (011d72h - UNIT_END)
@overlay_black$qv label near
public @OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV
org (011d93h - UNIT_END)
@OVERLAY_STAGE_ENTER_UPDATE_AND_R$QV label near
public @dialog_load$qv
org (0139bbh - UNIT_END)
@dialog_load$qv label near
public @STAGE1_SETUP$QV
org (01453ch - UNIT_END)
@STAGE1_SETUP$QV label near
public @STAGE2_SETUP$QV
org (01460bh - UNIT_END)
@STAGE2_SETUP$QV label near
public @STAGE3_SETUP$QV
org (0146c8h - UNIT_END)
@STAGE3_SETUP$QV label near
public @STAGE4_SETUP$QV
org (014797h - UNIT_END)
@STAGE4_SETUP$QV label near
public @STAGE5_SETUP$QV
org (014871h - UNIT_END)
@STAGE5_SETUP$QV label near
public @STAGE6_SETUP$QV
org (01496eh - UNIT_END)
@STAGE6_SETUP$QV label near
public @STAGEX_SETUP$QV
org (0149feh - UNIT_END)
@STAGEX_SETUP$QV label near
org (14ab0h - UNIT_END)
STAGE_SESSION_TEXT ends
main_01 group STAGE_SESSION_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_LOAD, SND_KAJA_INTERRUPT
org 03f4h
SND_LOAD label far
org 04ach
SND_KAJA_INTERRUPT label far
org 07c0h
SHARED ends
STAGE_SESSION_MAIN03_CONTEXT segment byte public 'CODE' use16
assume cs:STAGE_SESSION_MAIN03_CONTEXT
public @midboss_reset$qv
org 07231h
@midboss_reset$qv label far
org (209d0h - 15270h)
STAGE_SESSION_MAIN03_CONTEXT ends
main_03 group STAGE_SESSION_MAIN03_CONTEXT
_DATA segment word public 'DATA' use16
public _debug_frame_step_enabled
org 091h
_debug_frame_step_enabled label byte
public _load_playchar_resources
org 0a0h
_load_playchar_resources label word
public _stage_bgm_name
org 0a2h
_stage_bgm_name label dword
public _SESSION_EYE_RGB
org 0cbh
_SESSION_EYE_RGB label byte
public _SESSION_REIMU_BFT
org 0d3h
_SESSION_REIMU_BFT label byte
public _SESSION_MARI_BFT
org 0ddh
_SESSION_MARI_BFT label byte
public _SESSION_MIMA_BFT
org 0e6h
_SESSION_MIMA_BFT label byte
public _SESSION_YUKA_BFT
org 0efh
_SESSION_YUKA_BFT label byte
public _SESSION_MIKOD_BFT
org 0f8h
_SESSION_MIKOD_BFT label byte
public _SESSION_MIKO32_BFT
org 0102h
_SESSION_MIKO32_BFT label byte
public _SESSION_REIMU16_BFT
org 010dh
_SESSION_REIMU16_BFT label byte
public _SESSION_MARI16_BFT
org 0119h
_SESSION_MARI16_BFT label byte
public _SESSION_MIMA16_BFT
org 0124h
_SESSION_MIMA16_BFT label byte
public _SESSION_YUKA16_BFT
org 012fh
_SESSION_YUKA16_BFT label byte
public _SESSION_MIKO16_BFT
org 013ah
_SESSION_MIKO16_BFT label byte
public _SESSION_BOMB_YUUKA_BFT
org 0145h
_SESSION_BOMB_YUUKA_BFT label byte
public _SESSION_BOMB_BFT
org 014fh
_SESSION_BOMB_BFT label byte
public _SESSION_BSS0_CD2
org 0159h
_SESSION_BSS0_CD2 label byte
public _SESSION_ST00_BFT
org 0162h
_SESSION_ST00_BFT label byte
public _SESSION_ST00_MPN
org 016bh
_SESSION_ST00_MPN label byte
public _SESSION_BSS1_CD2
org 0174h
_SESSION_BSS1_CD2 label byte
public _SESSION_ST01_BFT
org 017dh
_SESSION_ST01_BFT label byte
public _SESSION_ST01_MPN
org 0186h
_SESSION_ST01_MPN label byte
public _SESSION_BSS2_CD2
org 018fh
_SESSION_BSS2_CD2 label byte
public _SESSION_ST02_BFT
org 0198h
_SESSION_ST02_BFT label byte
public _SESSION_ST02_MPN
org 01a1h
_SESSION_ST02_MPN label byte
public _SESSION_BSS3_CD2
org 01aah
_SESSION_BSS3_CD2 label byte
public _SESSION_ST03_BFT
org 01b3h
_SESSION_ST03_BFT label byte
public _SESSION_ST03_MPN
org 01bch
_SESSION_ST03_MPN label byte
public _SESSION_BSS4_CD2
org 01c5h
_SESSION_BSS4_CD2 label byte
public _SESSION_ST04_BFT
org 01ceh
_SESSION_ST04_BFT label byte
public _SESSION_ST04_MPN
org 01d7h
_SESSION_ST04_MPN label byte
public _SESSION_BSS4_CD2_REPEAT
org 01e0h
_SESSION_BSS4_CD2_REPEAT label byte
public _SESSION_ST04_BFT_REPEAT
org 01e9h
_SESSION_ST04_BFT_REPEAT label byte
public _SESSION_BSS6_CD2
org 01f2h
_SESSION_BSS6_CD2 label byte
public _SESSION_ST06_BFT
org 01fbh
_SESSION_ST06_BFT label byte
public _SESSION_ST06_MPN
org 0204h
_SESSION_ST06_MPN label byte
public _PaletteTone
org 03dah
_PaletteTone label word
public _random_seed
org 0418h
_random_seed label dword
public _input_sense_hook
org 0261ch
_input_sense_hook label word
public _vsync_Count2
org 0267ch
_vsync_Count2 label word
public _bg_render_not_bombing
org 03506h
_bg_render_not_bombing label word
public _bg_render_bombing_func
org 0350ah
_bg_render_bombing_func label word
public _power
org 036f0h
_power label byte
public _resident
org 041fch
_resident label dword
public _overlay1
org 04abeh
_overlay1 label word
public _overlay2
org 04ac0h
_overlay2 label word
public _page_back
org 04ad6h
_page_back label byte
public _page_front
org 04ad7h
_page_front label byte
public _stage_id
org 0576eh
_stage_id label byte
public _playchar
org 05773h
_playchar label byte
public _pellet_bottom_col
org 0c33eh
_pellet_bottom_col label word
org 0c340h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
else
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
public PALETTE_ENTRY_RGB
org 023f0h
PALETTE_ENTRY_RGB label far
public TEXT_FILLCA
org 02508h
TEXT_FILLCA label far
public SUPER_ENTRY_BFNT
org 02d16h
SUPER_ENTRY_BFNT label far
public SUPER_CONVERT_TINY
org 035a2h
SUPER_CONVERT_TINY label far
org 0ae10h
_TEXT ends
STAGE_SESSION_TEXT segment byte public 'CODE' use16
assume cs:STAGE_SESSION_TEXT
public @gameplay_session_init$qv
org (0b063h - 0ae10h)
@gameplay_session_init$qv label near
org (UNIT_START - 0ae10h)
STAGE_SESSION_TEXT ends
main_01 group STAGE_SESSION_TEXT
endif
end

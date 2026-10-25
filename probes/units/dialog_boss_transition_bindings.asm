; Real MAIN frames and foreign symbols only; no instruction or value payloads.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 139f5h
UNIT_END equ 13a3eh
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
STD_ACTIVATE_TEXT segment byte public 'CODE' use16
assume cs:STD_ACTIVATE_TEXT
public @OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV
org (1213ah - MAIN01_BASE)
@OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV label near
org (UNIT_START - MAIN01_BASE)
STD_ACTIVATE_TEXT ends
STD_ACTIVATE_TAIL segment byte public 'CODE' use16
assume cs:STD_ACTIVATE_TAIL
public @dialog_animate$qv
org (13e58h - UNIT_END)
@dialog_animate$qv label far
org (14ab0h - UNIT_END)
STD_ACTIVATE_TAIL ends
main_01 group STD_ACTIVATE_TEXT, STD_ACTIVATE_TAIL
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
STD_ACTIVATE_MAIN03_SPACE segment byte public 'CODE' use16
org (209d0h - 15270h)
STD_ACTIVATE_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
public _total_std_frames, _bg_render_not_bombing, _scroll_speed, _overlay1
public _page_back, _std_update, _boss_update, _boss_fg_render
public _boss_bg_render_func, _boss_update_func, _boss_fg_render_func
org 01ecah
_total_std_frames label word
org 03506h
_bg_render_not_bombing label word
org 03515h
_scroll_speed label byte
org 04abeh
_overlay1 label word
org 04ad6h
_page_back label byte
org 0c656h
_std_update label word
org 0c672h
_boss_update label dword
org 0c676h
_boss_fg_render label word
org 0c67ah
_boss_bg_render_func label word
org 0c67ch
_boss_update_func label dword
org 0c680h
_boss_fg_render_func label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 0281ah
HMEM_ALLOCBYTE label far
org 0ae10h
_TEXT ends
STD_LOAD_PREFIX segment byte public 'CODE' use16
org (0c742h - 0ae10h)
STD_LOAD_PREFIX ends
STD_LOAD_TEXT segment byte public 'CODE' use16
STD_LOAD_TEXT ends
STD_FREE_TEXT segment byte public 'CODE' use16
assume cs:STD_FREE_TEXT
public @std_free$qv
@std_free$qv label near
org (014ab0h - 0c7fah)
STD_FREE_TEXT ends
main_01 group STD_LOAD_PREFIX, STD_LOAD_TEXT, STD_FREE_TEXT
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
STD_RUN_TEXT segment byte public 'CODE' use16
assume cs:STD_RUN_TEXT
public @std_run$qv, STD_RUN
org (016b76h - 015270h)
@std_run$qv label near
STD_RUN label near
STD_RUN_TEXT ends
STD_RUN_TAIL segment byte public 'CODE' use16
org (0209d0h - 016b76h)
STD_RUN_TAIL ends
main_03 group STD_RUN_TEXT, STD_RUN_TAIL
_DATA segment word public 'DATA' use16
public _std_seg, _std_fn, _std_size_in_data_segment, _stage_id
public _std_enemy_scripts, _std_ip, _stage_title, _stage_bgm_title
public _boss_bgm_title, _std_map_section_p, _tile_row_in_section
public _std_scroll_speed, _scroll_speed, _stage_vm
org 00f52h
_std_seg label word
org 00f54h
_std_fn label byte
org 03515h
_scroll_speed label byte
org 03628h
_std_size_in_data_segment label word
org 0362ah
_std_enemy_scripts label word
org 0366ah
_std_ip label dword
org 03f8eh
_stage_vm label dword
org 04ac8h
_stage_title label dword
org 04acch
_stage_bgm_title label dword
org 04ad0h
_boss_bgm_title label dword
org 0575ah
_std_map_section_p label word
org 0575ch
_tile_row_in_section label byte
org 0575eh
_std_scroll_speed label word
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

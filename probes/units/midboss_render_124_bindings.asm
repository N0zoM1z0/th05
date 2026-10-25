; True foreign symbols and outside gaps around the complete454-byte cohort.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 0dae1h
UNIT_END equ 0dca7h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SUPER_ROLL_PUT_1PLANE, SUPER_ROLL_PUT
org 02e1ah
SUPER_ROLL_PUT_1PLANE label far
org 02fe0h
SUPER_ROLL_PUT label far
org MAIN01_BASE
_TEXT ends
MID_FG_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN01_BASE)
MID_FG_TEXT ends
MID_FG_AFTER_TEXT segment byte public 'CODE' use16
assume cs:MID_FG_AFTER_TEXT
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1, @midboss_defeat_render$qv
org (0df28h - UNIT_END)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (132d3h - UNIT_END)
@midboss_defeat_render$qv label near
org (SHARED_BASE - UNIT_END)
MID_FG_AFTER_TEXT ends
main_01 group MID_FG_TEXT, MID_FG_AFTER_TEXT
MID_FG_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
MID_FG_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _stage_frame_mod8, _stage_frame_mod16, _midboss, _boss_statebyte
org 5768h
_stage_frame_mod8 label byte
org 5769h
_stage_frame_mod16 label byte
org 5aa4h
_midboss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

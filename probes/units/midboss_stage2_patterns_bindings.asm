; True symbol-only context, no initialized DATA or helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
M2_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
M2_MAIN01_CONTEXT ends
main_01 group M2_MAIN01_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
SHARED ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @randring2_next16$qv
org 002ch
@randring2_next16$qv label near
org (15cc1h - 15270h)
B4_UPDATE_TEXT ends
M2_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:M2_MAIN03_TAIL
public _bullets_add_regular
org (17204h - 15debh)
_bullets_add_regular label near
org (209d0h - 15debh)
M2_MAIN03_TAIL ends
main_03 group B4_UPDATE_TEXT, M2_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _midboss2_orbit_center, _bullet_template_tune
public _stage_frame_mod4, _stage_frame_mod16
public _bullet_template, _midboss, _boss_statebyte
org 3726h
_midboss2_orbit_center label byte
org 41deh
_bullet_template_tune label byte
org 5767h
_stage_frame_mod4 label byte
org 5769h
_stage_frame_mod16 label byte
org 577eh
_bullet_template label byte
org 5aa4h
_midboss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

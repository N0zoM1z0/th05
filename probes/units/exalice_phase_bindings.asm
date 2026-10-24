; Actual foreign symbols and outside context; no supplied game instructions.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1a1dbh
AFTER_BASE equ 1a250h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
X_PHASE_MAIN01_SPACE segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
X_PHASE_MAIN01_SPACE ends
main_01 group GENERIC_BOSS_MAIN01_TEXT, X_PHASE_MAIN01_SPACE
X_PHASE_SHARED_SPACE segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
X_PHASE_SHARED_SPACE ends
BOSS_TEXT segment byte public 'CODE' use16
assume cs:BOSS_TEXT
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org (176ddh - MAIN03_BASE)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (UNIT_START - MAIN03_BASE)
BOSS_TEXT ends
EXALICE_PHASE_TEXT segment byte public 'CODE' use16
EXALICE_PHASE_TEXT ends
X_PHASE_TAIL segment para public 'CODE' use16
assume cs:X_PHASE_TAIL
public @boss_hittest_shots$qv, @boss_items_drop$qv
org (1fad0h - AFTER_BASE)
@boss_hittest_shots$qv label near
org (1fb0ch - AFTER_BASE)
@boss_items_drop$qv label near
org (DGROUP_BASE - AFTER_BASE)
X_PHASE_TAIL ends
main_03 group BOSS_TEXT, EXALICE_PHASE_TEXT, X_PHASE_TAIL
_DATA segment word public 'DATA' use16
public _bullet_zap_drop_point_items, _boss_phase_timed_out, _bullet_zap
public _bombing, _exalice_bomb_invincibility, _boss
org 1a5ch
_bullet_zap_drop_point_items label byte
org 1fc8h
_boss_phase_timed_out label byte
org 3f96h
_bullet_zap label byte
org 4206h
_bombing label byte
org 4a8eh
_exalice_bomb_invincibility label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Symbol-only context around the complete natural default midboss owner.
; No helper bodies, target bytes, state values or inside-function padding.
.386
.model large

MAIN01_BASE equ 0ae10h
MAIN03_BASE equ 15270h
UNIT_START equ 1c54eh
FOREIGN_TAIL_BASE equ 1c670h
DGROUP_BASE equ 209d0h

_TEXT segment word public 'CODE' use16
org MAIN01_BASE
_TEXT ends
; Match the header's actual foreign segment name so its empty compiler
; contribution merges here, rather than appearing after the large DS gap.
MAI_TEXT segment word public 'CODE' use16
org (MAIN03_BASE - MAIN01_BASE)
MAI_TEXT ends
main_01 group MAI_TEXT

MIDBOSS_TEXT segment word public 'CODE' use16
MIDBOSS_TEXT ends

MB_DFT_TEXT segment word public 'CODE' use16
assume cs:MB_DFT_TEXT
public @RANDRING2_NEXT16_MOD$QUI, @POINTNUMS_ADD_YELLOW$QIIUI
public @midboss_reset$qv
org (152c0h - MAIN03_BASE)
@RANDRING2_NEXT16_MOD$QUI label near
org (16e28h - MAIN03_BASE)
@POINTNUMS_ADD_YELLOW$QIIUI label near
org (1c4a1h - MAIN03_BASE)
@midboss_reset$qv label far
org (UNIT_START - MAIN03_BASE)
MB_DFT_TEXT ends
main_03 group MIDBOSS_TEXT, MB_DFT_TEXT

; The compiler's whole contribution ends before this independent PARA segment.
; Original 283-byte code ends 1C669. A natural five-byte far-call relaxation
; instead of the original four-byte call would end 1C66A and remain inexact;
; either end aligns here at 1C670 without inserting a byte into any function.
; Verify this actual MAP boundary before interpreting diagnostic comparisons.
MIDBOSS_DEFAULT_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - FOREIGN_TAIL_BASE)
MIDBOSS_DEFAULT_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _pointnum_times_2, _boss_phase_timed_out, _playfield_shake_anim_time
public _score_delta, _midboss, _boss, _midboss_active
org 18aah
_pointnum_times_2 label byte
org 1fc8h
_boss_phase_timed_out label byte
org 3520h
_playfield_shake_anim_time label word
org 3712h
_score_delta label dword
org 5aa4h
_midboss label byte
org 5abah
_boss label byte
org 0c4aah
_midboss_active label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

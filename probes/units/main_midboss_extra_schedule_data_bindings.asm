; Original MAIN code frames + four independently reviewed near callback publics.
; No callback instructions, pointer values, or target DATA bytes are supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_TEXT segment byte public 'CODE' use16
MAI_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
MIDBOSSX_SCHED_MAIN01 segment byte public 'CODE' use16
org 09ca0h
MIDBOSSX_SCHED_MAIN01 ends
main_01 group MAI_TEXT, GENERIC_BOSS_MAIN01_TEXT, MIDBOSSX_SCHED_MAIN01
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
MIDBOSSX_SCHED_ORIG_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSSX_SCHED_ORIG_TEXT
public @midbossx_pattern_wait$qv
public @midbossx_pattern_spread$qv
public @midbossx_pattern_random$qv
public @midbossx_pattern_decelerate$qv
org 01234h
@midbossx_pattern_wait$qv label near
org 01246h
@midbossx_pattern_spread$qv label near
org 012a7h
@midbossx_pattern_random$qv label near
org 012deh
@midbossx_pattern_decelerate$qv label near
org 0b760h
MIDBOSSX_SCHED_ORIG_TEXT ends
MIDBOSSX_SCHED_TEXT segment byte public 'CODE' use16
MIDBOSSX_SCHED_TEXT ends
main_03 group BOSS_TEXT, MIDBOSSX_SCHED_ORIG_TEXT, MIDBOSSX_SCHED_TEXT
_DATA segment word public 'DATA' use16
org 0147ah
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

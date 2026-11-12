; Original MAIN frames and real accepted Stage 5 pattern CODE publics only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_TEXT segment byte public 'CODE' use16
MAI_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
MB5_SCHED_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
MB5_SCHED_MAIN01_SPACE ends
main_01 group MAI_TEXT, GENERIC_BOSS_MAIN01_TEXT, MB5_SCHED_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
MAIN_036_TEXT segment byte public 'CODE' use16
MAIN_036_TEXT ends
MIDBOSS5_SCHED_ORIG_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSS5_SCHED_ORIG_TEXT
public @midboss5_pattern_blue_spread$qv
public @midboss5_pattern_green_rings$qv
public @midboss5_pattern_aimed_stacks$qv
org 0157dh
@midboss5_pattern_blue_spread$qv label near
org 015c1h
@midboss5_pattern_green_rings$qv label near
org 0162ah
@midboss5_pattern_aimed_stacks$qv label near
org 0b760h
MIDBOSS5_SCHED_ORIG_TEXT ends
MIDBOSS5_SCHED_TEXT segment byte public 'CODE' use16
MIDBOSS5_SCHED_TEXT ends
main_03 group BOSS_TEXT, MAIN_036_TEXT, MIDBOSS5_SCHED_ORIG_TEXT, MIDBOSS5_SCHED_TEXT
_DATA segment word public 'DATA' use16
org 01490h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

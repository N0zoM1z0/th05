; Foreign real main-03 callbacks; source owns the entire36-byte DATA cohort.
; No instructions, pointer values, owned DATA labels or source bytes supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SOLO_TABLES_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
SOLO_TABLES_MAIN01_SPACE ends
main_01 group SOLO_TABLES_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @yuki_solo_ring_sweep$qv
org (1856ah - 15270h)
@yuki_solo_ring_sweep$qv label near
public @yuki_solo_random_spreads$qv
org (1863bh - 15270h)
@yuki_solo_random_spreads$qv label near
public @yuki_solo_random_rings$qv
org (186d7h - 15270h)
@yuki_solo_random_rings$qv label near
public @yuki_solo_snow_fan$qv
org (18767h - 15270h)
@yuki_solo_snow_fan$qv label near
public @yuki_solo_snow_cross$qv
org (18845h - 15270h)
@yuki_solo_snow_cross$qv label near
public @yuki_solo_vector_stacks$qv
org (188dbh - 15270h)
@yuki_solo_vector_stacks$qv label near
public @mai_solo_widening_fans$qv
org (18d3fh - 15270h)
@mai_solo_widening_fans$qv label near
public @mai_solo_turning_stacks$qv
org (18de3h - 15270h)
@mai_solo_turning_stacks$qv label near
public @mai_solo_rotating_fans$qv
org (18ea9h - 15270h)
@mai_solo_rotating_fans$qv label near
public @mai_solo_rotating_rings$qv
org (18f07h - 15270h)
@mai_solo_rotating_rings$qv label near
public @mai_solo_snow_rings$qv
org (18f60h - 15270h)
@mai_solo_snow_rings$qv label near
public @mai_solo_fans_and_snow$qv
org (18fedh - 15270h)
@mai_solo_fans_and_snow$qv label near
public @mai_solo_turning_fans$qv
org (190f7h - 15270h)
@mai_solo_turning_fans$qv label near
public @mai_solo_revenge_snow$qv
org (191a7h - 15270h)
@mai_solo_revenge_snow$qv label near
public @mai_solo_laser_bounce$qv
org (19250h - 15270h)
@mai_solo_laser_bounce$qv label near
org (209d0h - 15270h)
MAIN_035_TEXT ends
main_03 group MAIN_035_TEXT
_DATA segment word public 'DATA' use16
org 01964h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

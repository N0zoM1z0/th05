; Real foreign near-callback providers; source owns only the complete16DATA bytes.
.386
.model large
MAIN03_BASE equ 15270h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
EXALICE_PAIR_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
EXALICE_PAIR_MAIN01_SPACE ends
main_01 group EXALICE_PAIR_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
EXALICE_PAT_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_PAT_TEXT
public @exalice_pattern_random_fan$qv, @exalice_pattern_turning_rings$qv
org (198e3h - MAIN03_BASE)
@exalice_pattern_random_fan$qv label near
org (19939h - MAIN03_BASE)
@exalice_pattern_turning_rings$qv label near
org (199d5h - MAIN03_BASE)
EXALICE_PAT_TEXT ends
EXALICE_LAT_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_LAT_TEXT
public @exalice_pattern_gravity_stacks$qv, @exalice_pattern_diamond_rings$qv
org (19b13h - 199d5h)
@exalice_pattern_gravity_stacks$qv label near
org (19bc2h - 199d5h)
@exalice_pattern_diamond_rings$qv label near
org (19c2dh - 199d5h)
EXALICE_LAT_TEXT ends
EXALICE_LSR_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_LSR_TEXT
public @exalice_pattern_bouncing_rings$qv, @exalice_pattern_speedup_fans$qv
org (19c95h - 19c2dh)
@exalice_pattern_bouncing_rings$qv label near
org (19d82h - 19c2dh)
@exalice_pattern_speedup_fans$qv label near
org (19eb2h - 19c2dh)
EXALICE_LSR_TEXT ends
EXALICE_FIN_TEXT segment byte public 'CODE' use16
assume cs:EXALICE_FIN_TEXT
public @exalice_pattern_cross_cheetos$qv, @exalice_pattern_turning_cheetos$qv
@exalice_pattern_cross_cheetos$qv label near
org (19f41h - 19eb2h)
@exalice_pattern_turning_cheetos$qv label near
org (1a1dbh - 19eb2h)
EXALICE_FIN_TEXT ends
EXALICE_PAIR_DATA_TEXT segment byte public 'CODE' use16
org (209d0h - 1a1dbh)
EXALICE_PAIR_DATA_TEXT ends
main_03 group EXALICE_PAT_TEXT, EXALICE_LAT_TEXT, EXALICE_LSR_TEXT, EXALICE_FIN_TEXT, EXALICE_PAIR_DATA_TEXT
_DATA segment word public 'DATA' use16
org 0199ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

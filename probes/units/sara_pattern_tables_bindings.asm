; Real foreign callbacks; no instruction or initialized payload is supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
B1_TABLE_MAIN01_GAP segment byte public 'CODE' use16
org 09ca0h
B1_TABLE_MAIN01_GAP ends
MAIN_0_TEXT segment byte public 'CODE' use16
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group B1_TABLE_MAIN01_GAP, MAIN_0_TEXT, BOSS_BG_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
B1_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B1_UPDATE_TEXT
public @pattern_blue_curve_counterclockw$qv
org (1d1f4h - 15270h)
@pattern_blue_curve_counterclockw$qv label near
public @pattern_blue_curve_clockwise$qv
org (1d22fh - 15270h)
@pattern_blue_curve_clockwise$qv label near
public @pattern_aimed_red_spread_stack$qv
org (1d26ah - 15270h)
@pattern_aimed_red_spread_stack$qv label near
public @pattern_red_stacks$qv
org (1d2a6h - 15270h)
@pattern_red_stacks$qv label near
public @pattern_pellet_arcs_at_expanding$qv
org (1d3aeh - 15270h)
@pattern_pellet_arcs_at_expanding$qv label near
public @pattern_random_red_rings$qv
org (1d436h - 15270h)
@pattern_random_red_rings$qv label near
public @pattern_accelerating_spirals_clo$qv
org (1d475h - 15270h)
@pattern_accelerating_spirals_clo$qv label near
public @pattern_accelerating_spirals_cou$qv
org (1d4dfh - 15270h)
@pattern_accelerating_spirals_cou$qv label near
B1_UPDATE_TEXT ends
B1_TABLES_TEXT segment byte public 'CODE' use16
org (209d0h - 1d4dfh)
B1_TABLES_TEXT ends
main_03 group LASER_SC_TEXT, B1_UPDATE_TEXT, B1_TABLES_TEXT
_DATA segment word public 'DATA' use16
org 01f6eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

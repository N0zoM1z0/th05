; Real foreign callbacks; no instruction or initialized payload is supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
B6_TABLE_MAIN01_GAP segment byte public 'CODE' use16
org 09ca0h
B6_TABLE_MAIN01_GAP ends
MAIN_0_TEXT segment byte public 'CODE' use16
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group B6_TABLE_MAIN01_GAP, MAIN_0_TEXT, BOSS_BG_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
assume cs:B6_PATTERN_A_TEXT
public @pattern_curved_rings$qv
org (1ababh - 15270h)
@pattern_curved_rings$qv label near
public @pattern_dualspeed_rings$qv
org (1ac25h - 15270h)
@pattern_dualspeed_rings$qv label near
B6_PATTERN_A_TEXT ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B6_UPDATE_TEXT
public @pattern_random_directional_and_k$qv
org (1ad20h - 1ac25h)
@pattern_random_directional_and_k$qv label near
public @pattern_dense_blue_stacks$qv
org (1ad7eh - 1ac25h)
@pattern_dense_blue_stacks$qv label near
B6_UPDATE_TEXT ends
B6_TABLES_TEXT segment byte public 'CODE' use16
org (209d0h - 1ad7eh)
B6_TABLES_TEXT ends
main_03 group B6_BALLS_TEXT, LASER_SC_TEXT, BULLET_A_TEXT, B6_PATTERN_A_TEXT, B6_UPDATE_TEXT, B6_TABLES_TEXT
_DATA segment word public 'DATA' use16
org 01a50h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

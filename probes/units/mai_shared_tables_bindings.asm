; Outside-only providers; source owns the complete semantic DATA bank.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHARED_TABLES_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
SHARED_TABLES_MAIN01_SPACE ends
main_01 group SHARED_TABLES_MAIN01_SPACE
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
MAIN_035_TEXT segment byte public 'CODE' use16
assume cs:MAIN_035_TEXT
public @mai_pattern_random_crosses$qv
org 0277ch
@mai_pattern_random_crosses$qv label near
public @mai_pattern_turning_fan$qv
org 027e2h
@mai_pattern_turning_fan$qv label near
public @mai_pattern_sweeping_pellets$qv
org 0283ch
@mai_pattern_sweeping_pellets$qv label near
public @mai_pattern_small_ball_fan$qv
org 028aah
@mai_pattern_small_ball_fan$qv label near
public @mai_pattern_reversing_rings$qv
org 029c0h
@mai_pattern_reversing_rings$qv label near
public @yuki_pattern_random_aimed_fan$qv
org 02a5ah
@yuki_pattern_random_aimed_fan$qv label near
public @yuki_pattern_random_rings$qv
org 02ab2h
@yuki_pattern_random_rings$qv label near
public @yuki_pattern_small_ball_stacks$qv
org 02afbh
@yuki_pattern_small_ball_stacks$qv label near
public @yuki_pattern_small_ball_fan$qv
org 02b44h
@yuki_pattern_small_ball_fan$qv label near
public @yuki_pattern_ball_stacks$qv
org 02b94h
@yuki_pattern_ball_stacks$qv label near
public @yuki_pattern_random_pellets$qv
org 02bddh
@yuki_pattern_random_pellets$qv label near
public @yuki_pattern_reversing_rings$qv
org 02c2ch
@yuki_pattern_reversing_rings$qv label near
public @yuki_pattern_cheetos$qv
org 02cb0h
@yuki_pattern_cheetos$qv label near
public @mai_pattern_cheetos$qv
org 02d07h
@mai_pattern_cheetos$qv label near
org 0b760h
MAIN_035_TEXT ends
main_03 group MAIN_035_TEXT
_DATA segment word public 'DATA' use16
org 018e6h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

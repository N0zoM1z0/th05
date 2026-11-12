; Only near CODE publics; no instructions or pointer words in the binder.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
YUMEKO_SCHEDULE_MAIN01 segment byte public 'CODE' use16
org 09ca0h
YUMEKO_SCHEDULE_MAIN01 ends
main_01 group YUMEKO_SCHEDULE_MAIN01
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @yumeko_pattern_sword_fan$qv
org 09ce9h
@yumeko_pattern_sword_fan$qv label near
public @yumeko_pattern_red_ring$qv
org 09d7eh
@yumeko_pattern_red_ring$qv label near
public @yumeko_pattern_counterrotating_s$qv
org 09f7ah
@yumeko_pattern_counterrotating_s$qv label near
public @yumeko_pattern_mirrored_spreads$qv
org 0a0b4h
@yumeko_pattern_mirrored_spreads$qv label near
org 0b760h
B5_UPDATE_TEXT ends
YUMEKO_SCHEDULE_TEXT segment byte public 'CODE' use16
YUMEKO_SCHEDULE_TEXT ends
main_03 group B5_UPDATE_TEXT, YUMEKO_SCHEDULE_TEXT
_DATA segment word public 'DATA' use16
org 01f9eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

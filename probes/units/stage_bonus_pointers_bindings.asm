; Real text-object providers after the source-owned42-byte near-pointer bank.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BONUS_PTR_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
BONUS_PTR_MAIN01_SPACE ends
main_01 group BONUS_PTR_MAIN01_SPACE
BONUS_PTR_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
BONUS_PTR_SHARED_SPACE ends
BONUS_PTR_TEXT segment byte public 'CODE' use16
org 0b760h
BONUS_PTR_TEXT ends
main_03 group BONUS_PTR_TEXT
_DATA segment word public 'DATA' use16
org 01a64h
_DATA ends
BONUS_PTR_STRING_TARGETS segment byte public 'DATA' use16
public _bonus_timeout_text
org 013h
_bonus_timeout_text label byte
public _bonus_credit_six_text
org 040h
_bonus_credit_six_text label byte
public _bonus_credit_five_text
org 06dh
_bonus_credit_five_text label byte
public _bonus_credit_four_text
org 09ah
_bonus_credit_four_text label byte
public _bonus_continue_one_text
org 0c7h
_bonus_continue_one_text label byte
public _bonus_continue_two_text
org 0f4h
_bonus_continue_two_text label byte
public _bonus_continue_three_text
org 0121h
_bonus_continue_three_text label byte
public _bonus_easy_text
org 014eh
_bonus_easy_text label byte
public _bonus_normal_text
org 017bh
_bonus_normal_text label byte
public _bonus_hard_text
org 01a8h
_bonus_hard_text label byte
public _bonus_lunatic_text
org 01d5h
_bonus_lunatic_text label byte
public _bonus_stage_text
org 0202h
_bonus_stage_text label byte
public _bonus_dream_text
org 0219h
_bonus_dream_text label byte
public _bonus_graze_text
org 0230h
_bonus_graze_text label byte
public _bonus_point_items_text
org 0247h
_bonus_point_items_text label byte
public _bonus_no_miss_text
org 025eh
_bonus_no_miss_text label byte
public _bonus_no_bomb_text
org 0275h
_bonus_no_bomb_text label byte
public _bonus_total_text
org 028ch
_bonus_total_text label byte
public _bonus_all_clear_text
org 029dh
_bonus_all_clear_text label byte
public _bonus_lives_text
org 02b4h
_bonus_lives_text label byte
public _bonus_point_total_text
org 02cbh
_bonus_point_total_text label byte
BONUS_PTR_STRING_TARGETS ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, BONUS_PTR_STRING_TARGETS, _BSS
end

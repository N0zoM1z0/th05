; True outside-only symbol context, no helper bodies/data values/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01f3ah
IATAN2 label far
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
assume cs:HUD_OVRL_TEXT
HUD_OVRL_TEXT ends
ITEM_UPDATE_MAIN01 segment byte public 'CODE' use16
assume cs:ITEM_UPDATE_MAIN01
public PLAYPERF_RAISE
org 0216ah
PLAYPERF_RAISE label far
public PLAYPERF_LOWER
org 02184h
PLAYPERF_LOWER label far
public @hud_lives_put$qv
org 02225h
@hud_lives_put$qv label far
public @hud_bombs_put$qv
org 022d9h
@hud_bombs_put$qv label far
public HUD_POINT_ITEMS_PUT
org 02392h
HUD_POINT_ITEMS_PUT label far
public HUD_DREAM_PUT
org 023bdh
HUD_DREAM_PUT label far
public SHOT_LEVEL_UPDATE
org 035d2h
SHOT_LEVEL_UPDATE label far
public @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
org 07459h
@OVERLAY_POPUP_UPDATE_AND_RENDER$QV label near
org 09ca0h
ITEM_UPDATE_MAIN01 ends
main_01 group HUD_OVRL_TEXT, ITEM_UPDATE_MAIN01
ITEM_REW_SHARED segment para public 'CODE' use16
assume cs:ITEM_REW_SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
ITEM_REW_SHARED ends
ITEM_REW_SHARED_TAIL segment byte public 'CODE' use16
assume cs:ITEM_REW_SHARED_TAIL
org 058eh
ITEM_REW_SHARED_TAIL ends
ITEM_SPLASH_TEXT segment byte public 'CODE' use16
assume cs:ITEM_SPLASH_TEXT
ITEM_SPLASH_TEXT ends
ITEM_EXTEND_TEXT segment byte public 'CODE' use16
assume cs:ITEM_EXTEND_TEXT
ITEM_EXTEND_TEXT ends
ITEM_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:ITEM_UPDATE_TEXT
ITEM_UPDATE_TEXT ends
ITEM_REWARD_TEXT segment byte public 'CODE' use16
assume cs:ITEM_REWARD_TEXT
public @POINTNUMS_ADD_YELLOW$QIIUI
org 01bb8h
@POINTNUMS_ADD_YELLOW$QIIUI label near
public @POINTNUMS_ADD_WHITE$QIIUI
org 01bd2h
@POINTNUMS_ADD_WHITE$QIIUI label near
public @item_extend_check$qv
org 07b3ch
@item_extend_check$qv label near
org 07b8bh
ITEM_REWARD_TEXT ends
ITEM_REW_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ITEM_REW_MAIN03_TAIL
org 03923h
ITEM_REW_MAIN03_TAIL ends
main_03 group ITEM_SPLASH_TEXT, ITEM_EXTEND_TEXT, ITEM_UPDATE_TEXT, ITEM_REWARD_TEXT, ITEM_REW_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _item_playperf_raise
org 01e02h
_item_playperf_raise label byte
public _POWER_OVERFLOW_BONUS
org 01e12h
_POWER_OVERFLOW_BONUS label byte
public _power_overflow
org 01e78h
_power_overflow label byte
public _items_collected
org 01e7ch
_items_collected label byte
public _extend_point_items_collected
org 01e7eh
_extend_point_items_collected label byte
public _total_point_items_collected
org 01e80h
_total_point_items_collected label byte
public _total_max_valued_point_items_col
org 01e82h
_total_max_valued_point_items_col label byte
public _items_pull_to_player
org 01e84h
_items_pull_to_player label byte
public _power
org 036f0h
_power label byte
public _stage_point_items_collected
org 036f5h
_stage_point_items_collected label byte
public _dream
org 036f6h
_dream label byte
public _score_delta
org 03712h
_score_delta label byte
public _bullet_clear_time
org 03f97h
_bullet_clear_time label byte
public _overlay_popup_id_new
org 04abdh
_overlay_popup_id_new label byte
public _overlay2
org 04ac0h
_overlay2 label byte
public _lives
org 04ad4h
_lives label byte
public _bombs
org 04ad5h
_bombs label byte
public _item_point_score_at_full_dream
org 0c652h
_item_point_score_at_full_dream label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

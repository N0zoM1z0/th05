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
ITEM_REWARD_TEXT segment byte public 'CODE' use16
assume cs:ITEM_REWARD_TEXT
ITEM_REWARD_TEXT ends
ITEM_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:ITEM_UPDATE_TEXT
public @PlayfieldMotion@update_seg3$qv
org 0ch
@PlayfieldMotion@update_seg3$qv label near
public VECTOR2_NEAR
org 06ah
VECTOR2_NEAR label near
public @item_splashes_update$qv
org 01154h
@item_splashes_update$qv label near
public @ITEM_COLLECT$QP6ITEM_T
org 07b8bh
@ITEM_COLLECT$QP6ITEM_T label near
public @ITEM_MISS_PENALTY$QP6ITEM_T
org 07df7h
@ITEM_MISS_PENALTY$QP6ITEM_T label near
org 07e3dh
ITEM_UPDATE_TEXT ends
ITEM_REW_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ITEM_REW_MAIN03_TAIL
org 03832h
ITEM_REW_MAIN03_TAIL ends
main_03 group ITEM_SPLASH_TEXT, ITEM_EXTEND_TEXT, ITEM_REWARD_TEXT, ITEM_UPDATE_TEXT, ITEM_REW_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _pointnum_times_2
org 018aah
_pointnum_times_2 label byte
public _items_pull_to_player
org 01e84h
_items_pull_to_player label byte
public _player_pos
org 036d2h
_player_pos label byte
public _miss_time
org 036f4h
_miss_time label byte
public _items
org 0b084h
_items label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

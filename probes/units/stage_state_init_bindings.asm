; Outside-only real routine/whole-pool symbols. No owned bytes or state.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRC_SETCLIP
org 0130ch
GRC_SETCLIP label far
org 0ae10h
_TEXT ends
HUD_OVRL_TEXT segment byte public 'CODE' use16
HUD_OVRL_TEXT ends
SHOT_HIT_TEXT segment byte public 'CODE' use16
SHOT_HIT_TEXT ends
SHOT_RUNTIME_MAIN01_CONTEXT segment byte public 'CODE' use16
SHOT_RUNTIME_MAIN01_CONTEXT ends
SHOT_UPDATE_TEXT segment byte public 'CODE' use16
SHOT_UPDATE_TEXT ends
SPARK_LIFE_TEXT segment byte public 'CODE' use16
SPARK_LIFE_TEXT ends
STAGE_STATE_CLEAR_TEXT segment byte public 'CODE' use16
assume cs:STAGE_STATE_CLEAR_TEXT
public CLEAR_DWORDS
org (0cf62h - 0ae10h)
CLEAR_DWORDS label near
org (012ac4h - 0ae10h)
STAGE_STATE_CLEAR_TEXT ends
STAGE_STATE_TEXT segment byte public 'CODE' use16
STAGE_STATE_TEXT ends
STAGE_STATE_TAIL segment byte public 'CODE' use16
org (014ab0h - 012badh)
STAGE_STATE_TAIL ends
main_01 group HUD_OVRL_TEXT, SHOT_HIT_TEXT, SHOT_RUNTIME_MAIN01_CONTEXT, SHOT_UPDATE_TEXT, SPARK_LIFE_TEXT, STAGE_STATE_CLEAR_TEXT, STAGE_STATE_TEXT, STAGE_STATE_TAIL
STAGE_STATE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
STAGE_STATE_SHARED_SPACE ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
SHOT_RUNTIME_MAIN03_CONTEXT segment byte public 'CODE' use16
SHOT_RUNTIME_MAIN03_CONTEXT ends
STAGE_STATE_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
STAGE_STATE_MAIN03_SPACE ends
main_03 group LASER_SC_TEXT, SHOT_RUNTIME_MAIN03_CONTEXT, STAGE_STATE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _bullet_zap
org 03f96h
_bullet_zap label byte
public _stage_graze
org 03f98h
_stage_graze label word
public _circles_color
org 041dah
_circles_color label byte
public _frames_unused
org 05760h
_frames_unused label dword
public _stage_frame
org 05764h
_stage_frame label word
public _stage_frame_mod2
org 05766h
_stage_frame_mod2 label byte
public _stage_frame_mod4
org 05767h
_stage_frame_mod4 label byte
public _stage_frame_mod8
org 05768h
_stage_frame_mod8 label byte
public _stage_frame_mod16
org 05769h
_stage_frame_mod16 label byte
public _slowdown_factor
org 0576ah
_slowdown_factor label word
public _quit
org 0576ch
_quit label byte
public _palette_changed
org 0576dh
_palette_changed label byte
public _slowdown_caused_by_bullets
org 0577ch
_slowdown_caused_by_bullets label byte
public _lasers
org 0578ch
_lasers label byte
public _sparks
org 05aeah
_sparks label byte
public _bullets
org 05f2ah
_bullets label byte
public _enemies
org 093fah
_enemies label byte
public _gather_circles
org 09bfah
_gather_circles label byte
public _gather_template
org 09ea6h
_gather_template label byte
public _circles
org 09eb4h
_circles label byte
public _pointnums
org 09f04h
_pointnums label byte
public _items
org 0b084h
_items label byte
public _custom_entities
org 0b3f4h
_custom_entities label byte
public _shots
org 0ba8eh
_shots label byte
public _hitshots
org 0bf56h
_hitshots label byte
public _hitshot_next_free_id
org 0c64ah
_hitshot_next_free_id label word
public _shots_alive_count
org 0c64ch
_shots_alive_count label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

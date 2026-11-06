; Foreign native frames/state only; no instructions, initialized data or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_HELPERS_TEXT segment word public 'CODE' use16
assume cs:main_01
public HUD_POWER_PUT
org (0d255h - 0ae10h)
HUD_POWER_PUT label far
org (0e38ch - 0ae10h)
SHOT_HELPERS_TEXT ends
FOREIGN_SHOT_HELPERS_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e40eh)
FOREIGN_SHOT_HELPERS_TAIL ends
main_01 group SHOT_HELPERS_TEXT, FOREIGN_SHOT_HELPERS_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _VELOCITY_192_AT_ANGLE, _SHOT_LEVEL_TO_POWER
public _power, _shot_level, _player_pos, _shot_ptr
public _shots, _shots_end, _playchar_shot_func, _playchar_shot_funcs
org 00f72h
_VELOCITY_192_AT_ANGLE label dword
org (00f72h + (256 * 4))
org 018ach
_SHOT_LEVEL_TO_POWER label word
org (018ach + (9 * 2))
org 036d2h
_player_pos label dword
org (036d2h + 12)
org 036f0h
_power label byte
org 036f1h
_shot_level label byte
org 036f2h
org 04200h
_shot_ptr label word
org 04202h
org 0ba8eh
_shots label byte
org (0ba8eh + (64 * 18))
_shots_end label byte
org 0c4bch
_playchar_shot_func label word
org 0c4beh
_playchar_shot_funcs label word
org 0c4c0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

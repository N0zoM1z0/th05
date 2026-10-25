; Outside-only real context for complete player miss-state function CB0A..CC3D.
; No foreign instructions, initialized values, stack or inside-owner padding.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
PLAYER_MISS_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_MISS_TEXT
org 01cfah
PLAYER_MISS_TEXT ends
PLAYER_MISS_AFTER_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_MISS_AFTER_TEXT
public PLAYPERF_LOWER, @hud_lives_put$qv, @hud_bombs_put$qv
public HUD_DREAM_PUT, @gameover_run$qv, SHOT_LEVEL_UPDATE
org 00357h
PLAYPERF_LOWER label far
org 003f8h
@hud_lives_put$qv label far
org 004ach
@hud_bombs_put$qv label far
org 00590h
HUD_DREAM_PUT label far
org 00c1fh
@gameover_run$qv label near
org 017a5h
SHOT_LEVEL_UPDATE label far
org 07e73h
PLAYER_MISS_AFTER_TEXT ends
main_01 group PLAYER_MISS_TEXT, PLAYER_MISS_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 00232h
SND_SE_PLAY label far
org 007c0h
SHARED ends
PLAYER_MISS_MAIN03_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_MISS_MAIN03_TEXT
public ITEMS_MISS_ADD
org 07a60h
ITEMS_MISS_ADD label far
org 0b760h
PLAYER_MISS_MAIN03_TEXT ends
main_03 group PLAYER_MISS_MAIN03_TEXT
_DATA segment word public 'DATA' use16
public _PaletteTone, _power_overflow, _player_pos, _power, _miss_time, _dream
public _miss_explosion_angle, _miss_explosion_radius, _bullet_clear_time
public _resident, _lives, _bombs, _stage_frame_mod2, _quit, _palette_changed
public _playperf, _boss
org 003dah
_PaletteTone label word
org 01e78h
_power_overflow label word
org 036d2h
_player_pos label byte
org 036f0h
_power label byte
org 036f4h
_miss_time label byte
org 036f6h
_dream label byte
org 036f7h
_miss_explosion_angle label byte
org 036f8h
_miss_explosion_radius label word
org 03f97h
_bullet_clear_time label byte
org 041fch
_resident label dword
org 04ad4h
_lives label byte
org 04ad5h
_bombs label byte
org 05766h
_stage_frame_mod2 label byte
org 0576ch
_quit label byte
org 0576dh
_palette_changed label byte
org 05770h
_playperf label byte
org 05abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

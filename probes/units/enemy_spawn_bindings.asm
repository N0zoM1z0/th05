; Complete enemy allocator context, original foreign addresses only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
ENEMY_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
ENEMY_MAIN01_CONTEXT ends
HUD_OVRL_TEXT segment word public 'CODE' use16
HUD_OVRL_TEXT ends
main_01 group ENEMY_MAIN01_CONTEXT, HUD_OVRL_TEXT
ENEMY_SHARED_CONTEXT segment para public 'CODE' use16
org 07c0h
ENEMY_SHARED_CONTEXT ends
MIDBOSS_TEXT segment byte public 'CODE' use16
MIDBOSS_TEXT ends
ENEMY_SPAWN_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_SPAWN_TEXT
public @randring2_next16$qv
org 02ch
@randring2_next16$qv label near
public @RANDRING2_NEXT16_MOD$QUI
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
org 0180ah
ENEMY_SPAWN_TEXT ends
ENEMY_UPDATE_TEXT segment byte public 'CODE' use16
ENEMY_UPDATE_TEXT ends
main_03 group MIDBOSS_TEXT, ENEMY_SPAWN_TEXT, ENEMY_UPDATE_TEXT
ENEMY_MAIN03_TAIL segment byte public 'CODE' use16
org 09e5ah
ENEMY_MAIN03_TAIL ends
_DATA segment word public 'DATA' use16
public _std_enemy_scripts
org 0362ah
_std_enemy_scripts label word
public _std_ip
org 0366ah
_std_ip label dword
public _rank
org 0576fh
_rank label byte
public _enemies
org 093fah
_enemies label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

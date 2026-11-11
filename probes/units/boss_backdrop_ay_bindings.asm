.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
BOSS_BD_AY_PREFIX segment byte public 'CODE' use16
org (0C41Eh - 0AE10h)
BOSS_BD_AY_PREFIX ends
BOSS_BD_AY_TEXT segment byte public 'CODE' use16
BOSS_BD_AY_TEXT ends
BOSS_BD_AY_TAIL segment byte public 'CODE' use16
assume cs:BOSS_BD_AY_TAIL
public grcg_fill_playfield_rows
org (010600h - 0C43Ah)
grcg_fill_playfield_rows label near
org (014AB0h - 0C43Ah)
BOSS_BD_AY_TAIL ends
main_01 group BOSS_BD_AY_PREFIX, BOSS_BD_AY_TEXT, BOSS_BD_AY_TAIL
SHARED segment para public 'CODE' use16
org (0209D0h - 014AB0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

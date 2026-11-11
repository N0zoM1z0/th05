; Native CS AE1, DS 209D; the separately accepted row-painter is foreign.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BOSS_BD_EARLY_PREFIX segment byte public 'CODE' use16
org (0bef4h - 0ae10h)
BOSS_BD_EARLY_PREFIX ends
BOSS_BD_EARLY_TEXT segment byte public 'CODE' use16
BOSS_BD_EARLY_TEXT ends
BOSS_BD_EARLY_TAIL segment byte public 'CODE' use16
assume cs:BOSS_BD_EARLY_TAIL
public grcg_fill_playfield_rows
org (010600h - 0bf60h)
grcg_fill_playfield_rows label near
org (014ab0h - 0bf60h)
BOSS_BD_EARLY_TAIL ends
main_01 group BOSS_BD_EARLY_PREFIX, BOSS_BD_EARLY_TEXT, BOSS_BD_EARLY_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

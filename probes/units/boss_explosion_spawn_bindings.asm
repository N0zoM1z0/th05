; Symbol-only native context for the complete Boss explosion creation family.
.386
.model large

_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends

EXP_SPAWN_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
EXP_SPAWN_MAIN01_GAP ends

EXP_SPAWN_SHARED_TEXT segment word public 'CODE' use16
assume cs:EXP_SPAWN_SHARED_TEXT
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org (15270h - 14ab0h)
EXP_SPAWN_SHARED_TEXT ends

BOSS_EXP_SPAWN_TEXT segment byte public 'CODE' use16
org (176ceh - 15270h)
BOSS_EXP_SPAWN_TEXT ends
main_03 group BOSS_EXP_SPAWN_TEXT

EXP_SPAWN_DGROUP_GAP segment para public 'CODE' use16
org (209d0h - 177f0h)
EXP_SPAWN_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _explosions_small, _explosions_big, _boss, _boss2
org 43fch
_explosions_small label byte
org 441ch
_explosions_big label byte
org 5abah
_boss label byte
org 5ad2h
_boss2 label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

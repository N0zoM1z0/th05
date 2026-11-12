; True MAIN group frames and only outside initialized DATA prefix.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
BOSS_EXPLOSION_FRAME_TEXT segment byte public 'CODE' use16
org 09ca0h
BOSS_EXPLOSION_FRAME_TEXT ends
main_01 group BOSS_EXPLOSION_FRAME_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
BOSS_EXPLOSION_FRAME_MAIN03 segment byte public 'CODE' use16
org 0b760h
BOSS_EXPLOSION_FRAME_MAIN03 ends
main_03 group BOSS_EXPLOSION_FRAME_MAIN03
_DATA segment word public 'DATA' use16
org 018e4h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

; Actual MAIN01 CS and DS frames. Outside-only location anchors.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHINKI_BD_FILL_PREFIX segment byte public 'CODE' use16
org (0c68ah - 0ae10h)
SHINKI_BD_FILL_PREFIX ends
SHINKI_BD_FILL_TEXT segment byte public 'CODE' use16
SHINKI_BD_FILL_TEXT ends
SHINKI_BD_FILL_TAIL segment byte public 'CODE' use16
assume cs:SHINKI_BD_FILL_TAIL
public grcg_fill_playfield_rows
org (010600h - 0c6e8h)
grcg_fill_playfield_rows label near
org (014ab0h - 0c6e8h)
SHINKI_BD_FILL_TAIL ends
main_01 group SHINKI_BD_FILL_PREFIX, SHINKI_BD_FILL_TEXT, SHINKI_BD_FILL_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

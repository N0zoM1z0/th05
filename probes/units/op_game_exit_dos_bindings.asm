; Whole real DOS wrapper25 atD41C..D435; actual cleanup body remains foreign.
; No foreign instructions, values, artificial stack or inside-owner holes.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public KEY_BEEP_ON, TEXT_CURSOR_SHOW, TEXT_SYSTEMLINE_SHOW
org 0197ah
KEY_BEEP_ON label far
org 02136h
TEXT_CURSOR_SHOW label far
org 02142h
TEXT_SYSTEMLINE_SHOW label far
org 0d300h
_TEXT ends
EXIT_DOS_TEXT segment byte public 'CODE' use16
assume cs:EXIT_DOS_TEXT
org 0011ch
EXIT_DOS_TEXT ends
EXIT_DOS_AFTER_TEXT segment byte public 'CODE' use16
assume cs:EXIT_DOS_AFTER_TEXT
public @game_exit$qv
org 003b7h
@game_exit$qv label far
org 01babh
EXIT_DOS_AFTER_TEXT ends
shared_exit group EXIT_DOS_TEXT, EXIT_DOS_AFTER_TEXT
_DATA segment word public 'DATA' use16
; Actual foreign music DATA end, no values supplied.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Actual foreign frames and empty declaration segments; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_HLINE, GRCG_SETCOLOR, GRCG_VLINE, GRAPH_GAIJI_PUTS, GRAPH_GAIJI_PUTC
org 0e5eh
GRCG_HLINE label far
org 0f28h
GRCG_SETCOLOR label far
org 0f58h
GRCG_VLINE label far
org 0383ch
GRAPH_GAIJI_PUTS label far
org 038e6h
GRAPH_GAIJI_PUTC label far
org 0a540h
_TEXT ends
REG_VALUES_TEXT segment byte public 'CODE' use16
assume cs:REG_VALUES_TEXT
public @REGISTRATION_SCORE_PUT$QII, @REGISTRATION_STAGE_PUT$QIII
org (0b899h - 0a540h)
@REGISTRATION_SCORE_PUT$QII label near
org (0b9c1h - 0a540h)
@REGISTRATION_STAGE_PUT$QIII label near
org (0ba84h - 0a540h)
REG_VALUES_TEXT ends
REG_NAME_TEXT segment byte public 'CODE' use16
REG_NAME_TEXT ends
REG_PLACE_ENTRY_TEXT segment byte public 'CODE' use16
REG_PLACE_ENTRY_TEXT ends
REG_DISPLAY_TEXT segment byte public 'CODE' use16
REG_DISPLAY_TEXT ends
REG_DISPLAY_TAIL segment byte public 'CODE' use16
org (0e800h - 0bcd3h)
REG_DISPLAY_TAIL ends
GROUP_01 group REG_VALUES_TEXT, REG_NAME_TEXT, REG_PLACE_ENTRY_TEXT, REG_DISPLAY_TEXT, REG_DISPLAY_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public BGIMAGE_PUT_RECT_16
org 04e4h
BGIMAGE_PUT_RECT_16 label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _hi, _entered_place, _playchar
org 04f1ah
_hi label byte
org 05076h
_entered_place label byte
org 05078h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

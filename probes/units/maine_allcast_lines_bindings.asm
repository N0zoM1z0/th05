; Symbol-only outside context for the complete all-cast line helper.
; No instructions, strings, table contents, substitute state, or .stack.
.386
.model large

GROUP01_BASE equ 0A540h
UNIT_START equ 0B1B5h
UNIT_END equ 0B273h
WAIT_START equ 0B37Ch
SHARED_BASE equ 0E800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
org GROUP01_BASE
_TEXT ends

ALLCAST_LINES_TEXT segment byte public 'CODE' use16
org (UNIT_START - GROUP01_BASE)
ALLCAST_LINES_TEXT ends

MAINE_01_TEXT segment byte public 'CODE' use16
assume cs:MAINE_01_TEXT
public @wait_flip_and_check_measure_targ$qv
org (WAIT_START - UNIT_END)
@wait_flip_and_check_measure_targ$qv label near
MAINE_01_TEXT ends
group_01 group ALLCAST_LINES_TEXT, MAINE_01_TEXT

ALLCAST_LINES_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - WAIT_START)
ALLCAST_LINES_SHARED_GAP ends

SHARED segment word public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
SHARED ends

ALLCAST_LINES_DATA_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE - 011Ah)
ALLCAST_LINES_DATA_GAP ends

_DATA segment word public 'DATA' use16
public _graph_putsa_fx_func
org 06BCh
_graph_putsa_fx_func label word
public _LINES
org 0820h
_LINES label dword
public _allcast_lines_per_screen
org 08DCh
_allcast_lines_per_screen label word
public _line_id_on_screen
org 08ECh
_line_id_on_screen label word
public _loaded_screen_id
org 04F14h
_loaded_screen_id label word
public _line_id_total
org 04F16h
_line_id_total label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

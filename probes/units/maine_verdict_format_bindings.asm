; Actual MAINE scalar-formatter addresses; symbols/foreign extents only.
.386
.model large
GROUP01_BASE equ 0A540h
UNIT_START equ 0C5E7h
UNIT_SIZE equ 02C7h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0E800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_GAIJI_PUTS
org 0383Ch
GRAPH_GAIJI_PUTS label far
org GROUP01_BASE
_TEXT ends

VERDICT_FMT_TEXT segment byte public 'CODE' use16
assume cs:VERDICT_FMT_TEXT
org (UNIT_START - GROUP01_BASE)
VERDICT_FMT_TEXT ends

VERDICT_FMT_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
VERDICT_FMT_TAIL ends
group_01 group VERDICT_FMT_TEXT, VERDICT_FMT_TAIL

SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends

; All formatter state and UI strings are foreign original objects.
_DATA segment word public 'DATA' use16
public _verdict_text_color
org 015E4h
_verdict_text_color label word
public _skill_subtract
org 015EAh
_skill_subtract label byte
; Actual identifier truncation, corroborated by retained OMF PUBDEF.
public _graph_3_digit_put_as_fixed_2_dig
org 01613h
_graph_3_digit_put_as_fixed_2_dig label byte
public _verdict_score_unit
org 01614h
_verdict_score_unit label byte
public _verdict_decimal_point
org 01617h
_verdict_decimal_point label byte
public _verdict_percent_sign
org 0161Ah
_verdict_percent_sign label byte
public _verdict_fraction_point
org 0161Dh
_verdict_fraction_point label byte
public _verdict_capture_quarter
org 0507Ch
_verdict_capture_quarter label byte
public _skill
org 0507Eh
_skill label dword
public _verdict_skill_quarter
org 05082h
_verdict_skill_quarter label dword
org 05086h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

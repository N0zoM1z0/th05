; Foreign extents and real symbols only, outside the complete493-byte owner.
.386
.model large
GROUP01_BASE equ 0A540h
UNIT_START equ 0C8AEh
UNIT_END equ 0CA9Bh
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
public @GRAPH_FRACTION_OF_MILLION_PUT$QIIUL
org (0C835h - GROUP01_BASE)
@GRAPH_FRACTION_OF_MILLION_PUT$QIIUL label near
org (UNIT_START - GROUP01_BASE)
VERDICT_FMT_TEXT ends
VERDICT_LOGIC_TEXT segment byte public 'CODE' use16
VERDICT_LOGIC_TEXT ends
VERDICT_LOGIC_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
VERDICT_LOGIC_TAIL ends
group_01 group VERDICT_FMT_TEXT, VERDICT_LOGIC_TEXT, VERDICT_LOGIC_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends
_DATA segment word public 'DATA' use16
public _random_seed
org 0276h
_random_seed label dword
public _verdict_text_left
org 015E2h
_verdict_text_left label word
public _verdict_text_color
org 015E4h
_verdict_text_color label word
public _verdict_text_top
org 015E8h
_verdict_text_top label word
public _verdict_bonus_percent_sign
org 01620h
_verdict_bonus_percent_sign label byte
public _resident
org 01D6Eh
_resident label dword
public _skill
org 0507Eh
_skill label dword
org 05086h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

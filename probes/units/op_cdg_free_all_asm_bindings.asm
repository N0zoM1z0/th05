; Genuine OP 14-byte CDG_FREE_ALL source-only native context.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
main_01 group FOREIGN_MAIN
SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_FREE
org 00f94h
CDG_FREE label near
org 00fcah
SHARED ends
CDG_FREE_ALL_TAIL segment para public 'CODE' use16
org 00d00h
CDG_FREE_ALL_TAIL ends
_DATA segment word public 'DATA' use16
; Actual foreign OP 64-slot CDG bank at DGROUP:3A96.
; Source-independent uninitialized outside range also satisfies MZ stack allocation.
public _cdg_slots
org 03a96h
_cdg_slots label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

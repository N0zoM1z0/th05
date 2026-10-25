; Only real external labels; all origin holes lie outside the complete helper.
.386
.model large
GROUP01_BASE equ 0A540h
UNIT_START equ 0DBE6h
UNIT_SIZE equ 011Bh
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0E800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BYTEBOXFILL_X
org 00C9Eh
GRCG_BYTEBOXFILL_X label far
public GRCG_SETCOLOR
org 00F28h
GRCG_SETCOLOR label far
public GAIJI_PUTSA
org 0125Eh
GAIJI_PUTSA label far
org GROUP01_BASE
_TEXT ends

STAFF_WIPE_PREFIX segment byte public 'CODE' use16
org (UNIT_START - GROUP01_BASE)
STAFF_WIPE_PREFIX ends
STAFF_WIPE_TEXT segment byte public 'CODE' use16
STAFF_WIPE_TEXT ends
STAFF_WIPE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
STAFF_WIPE_TAIL ends
group_01 group STAFF_WIPE_PREFIX, STAFF_WIPE_TEXT, STAFF_WIPE_TAIL

SHARED_CONTEXT segment para public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
SHARED_CONTEXT ends

_DATA segment word public 'DATA' use16
public _staff_text_clear_requested
org 01746h
_staff_text_clear_requested label byte
org 0C4D8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

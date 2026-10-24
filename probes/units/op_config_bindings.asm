; TH05 OP configuration original-address symbol-only context.
; No instruction bodies, source-owned filename or aggregate initializer data.
.386
.model large
; No .stack: this producer has no BSS objects.
OP01_BASE equ 0a390h
UNIT_START equ 0ba94h
UNIT_SIZE equ 017bh
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0d300h
DGROUP_BASE equ 0efe0h
OWNED_DATA_START equ 00f20h
OWNED_DATA_SIZE equ 0013h
OWNED_DATA_END equ (OWNED_DATA_START + OWNED_DATA_SIZE)

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_APPEND
org 0878h
FILE_APPEND label far
public FILE_CLOSE
org 0938h
FILE_CLOSE label far
public FILE_READ
org 09a4h
FILE_READ label far
public FILE_ROPEN
org 0a58h
FILE_ROPEN label far
public FILE_SEEK
org 0a94h
FILE_SEEK label far
public FILE_WRITE
org 0ad6h
FILE_WRITE label far
public F_SCOPY@
org 03e52h
F_SCOPY@ label far
org OP01_BASE
_TEXT ends

CFG_TEXT segment byte public 'CODE' use16
assume cs:CFG_TEXT
org (UNIT_START - OP01_BASE)
CFG_TEXT ends

OP_CFG_CODE_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
OP_CFG_CODE_TAIL ends
op_01 group CFG_TEXT, OP_CFG_CODE_TAIL

OP_CFG_FOREIGN_SHARED_SPACE segment para public 'CODE' use16
org (DGROUP_BASE - SHARED_BASE)
OP_CFG_FOREIGN_SHARED_SPACE ends

_DATA segment word public 'DATA' use16
org OWNED_DATA_START
_DATA ends

OP_CFG_DATA_TAIL segment byte public 'DATA' use16
public _resident
org (02dech - OWNED_DATA_END)
_resident label dword
OP_CFG_DATA_TAIL ends

_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, OP_CFG_DATA_TAIL, _BSS
end

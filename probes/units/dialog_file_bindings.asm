; Original TH05 .TX2 loader foreign-symbol context. No instructions, data
; initializers, stack or shim. All ORG holes are outside the real202-byte TU.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 1392bh
UNIT_END equ 139f5h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_CLOSE, FILE_READ, FILE_ROPEN, FILE_SEEK, HMEM_ALLOCBYTE, HMEM_FREE
org 0d2eh
FILE_CLOSE label far
org 0d3eh
FILE_READ label far
org 0df2h
FILE_ROPEN label far
org 0e2eh
FILE_SEEK label far
org 0281ah
HMEM_ALLOCBYTE label far
org 0291eh
HMEM_FREE label far
org MAIN01_BASE
_TEXT ends
F_DIALOG_TEXT segment byte public 'CODE' use16
assume cs:F_DIALOG_TEXT
org (UNIT_START - MAIN01_BASE)
F_DIALOG_TEXT ends
main_01 group F_DIALOG_TEXT
DIALOG_FILE_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
DIALOG_FILE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _dialog_fn, _stage_id, _playchar, _dialog_p
org 01ecch
_dialog_fn label dword
org 0576eh
_stage_id label byte
org 05773h
_playchar label byte
org 0c658h
_dialog_p label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Native SHARED code frame and original CDG external library functions.
; All model providers are symbol-only, with no copied executable CODE/DATA.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_ROPEN, FILE_READ, FILE_SEEK, FILE_CLOSE, HMEM_ALLOCBYTE, HMEM_FREE
org 00d2eh
FILE_CLOSE label far
org 00d3eh
FILE_READ label far
org 00df2h
FILE_ROPEN label far
org 00e2eh
FILE_SEEK label far
org 0281ah
HMEM_ALLOCBYTE label far
org 0291eh
HMEM_FREE label far
org 0ae10h
_TEXT ends
MAIN01_FOREIGN segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
MAIN01_FOREIGN ends
main_01 group MAIN01_FOREIGN
SHARED segment para public 'CODE' use16
org (015118h - 014ab0h)
SHARED ends
CDG_FREE_ALL_CONTEXT segment byte public 'CODE' use16
org 000eh
CDG_FREE_ALL_CONTEXT ends
FOREIGN_SHARED_TAIL segment para public 'CODE' use16
org (0209d0h - 015280h)
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _cdg_noalpha, _cdg_slots, _cdg_images_to_load
org 00848h
_cdg_noalpha label byte
org 0306ch
_cdg_slots label byte
org 0346ch
_cdg_images_to_load label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

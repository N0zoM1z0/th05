; OP genuine physical SHARED CDG resource source-only symbol context.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public FILE_CLOSE, FILE_READ, FILE_ROPEN, FILE_SEEK, HMEM_ALLOCBYTE, HMEM_FREE
org 00938h
FILE_CLOSE label far
org 009a4h
FILE_READ label far
org 00a58h
FILE_ROPEN label far
org 00a94h
FILE_SEEK label far
org 02322h
HMEM_ALLOCBYTE label far
org 02426h
HMEM_FREE label far
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
main_01 group FOREIGN_MAIN
SHARED segment para public 'CODE' use16
org 00e74h
SHARED ends
CDG_FREE_ALL_CONTEXT segment byte public 'CODE' use16
org 000eh
CDG_FREE_ALL_CONTEXT ends
FOREIGN_SHARED_TAIL segment para public 'CODE' use16
org 00d00h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _cdg_noalpha, _cdg_slots, _cdg_images_to_load
org 00ab4h
_cdg_noalpha label byte
org 03a96h
_cdg_slots label byte
org 03e96h
_cdg_images_to_load label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

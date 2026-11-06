; Real allocator/global slots and outside-only reserves. No initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 0281ah
HMEM_ALLOCBYTE label far
org 0ae10h
_TEXT ends
BB_LOAD_TEXT segment byte public 'CODE' use16
org (0f930h - 0ae10h)
BB_LOAD_TEXT ends
BB_LOAD_ALIGN segment para public 'CODE' use16
BB_LOAD_ALIGN ends
BB_LOAD_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h - 0f970h)
BB_LOAD_MAIN01_TAIL ends
main_01 group BB_LOAD_TEXT, BB_LOAD_ALIGN, BB_LOAD_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _bb_load_seg
org 04204h
_bb_load_seg label word
org 04206h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

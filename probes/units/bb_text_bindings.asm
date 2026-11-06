; Actual foreign allocator, filename and segment state; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 0281ah
HMEM_ALLOCBYTE label far
public HMEM_FREE
org 0291eh
HMEM_FREE label far
org 0ae10h
_TEXT ends
BB_LOAD_TEXT segment byte public 'CODE' use16
BB_LOAD_TEXT ends
BB_TEXT_LOAD_TEXT segment byte public 'CODE' use16
org (0e4b6h - 0ae10h)
BB_TEXT_LOAD_TEXT ends
BB_TEXT_ALIGN segment para public 'CODE' use16
BB_TEXT_ALIGN ends
BB_TEXT_MAIN01_TAIL segment byte public 'CODE' use16
org (14ab0h - 0e520h)
BB_TEXT_MAIN01_TAIL ends
main_01 group BB_LOAD_TEXT, BB_TEXT_LOAD_TEXT, BB_TEXT_ALIGN, BB_TEXT_MAIN01_TAIL
SHARED segment para public 'CODE' use16
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _bb_txt_fn
org 018c0h
_bb_txt_fn label byte
public _bb_txt_seg
org 019b0h
_bb_txt_seg label word
org 019b2h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

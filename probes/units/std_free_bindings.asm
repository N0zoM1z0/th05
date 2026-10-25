; Outside-only context for genuine STD release; no owned body or90 supplied.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 0291eh
HMEM_FREE label far
org 0ae10h
_TEXT ends
STD_FREE_PREFIX segment byte public 'CODE' use16
org (0c7fah - 0ae10h)
STD_FREE_PREFIX ends
STD_FREE_TEXT segment byte public 'CODE' use16
STD_FREE_TEXT ends
STD_FREE_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c811h)
STD_FREE_TAIL ends
main_01 group STD_FREE_PREFIX, STD_FREE_TEXT, STD_FREE_TAIL
STD_FREE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
STD_FREE_SHARED_SPACE ends
STD_FREE_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
STD_FREE_MAIN03_SPACE ends
main_03 group STD_FREE_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _std_seg
org 00f52h
_std_seg label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

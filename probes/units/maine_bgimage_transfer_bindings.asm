; Original MAINE _TEXT and group_01 to E800, SHARED to 10110.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE
org 02560h
HMEM_ALLOCBYTE label far
org 0A540h
_TEXT ends
BGTRANSFER_MAIN01_GAP segment byte public 'CODE' use16
org 042C0h
BGTRANSFER_MAIN01_GAP ends
group_01 group BGTRANSFER_MAIN01_GAP
SHARED segment byte public 'CODE' use16
org 0036Ch
SHARED ends
BGTRANSFER_AFTER segment byte public 'CODE' use16
org 01507h
BGTRANSFER_AFTER ends
_DATA segment word public 'DATA' use16
public _bgimage
org 006C2h
_bgimage label byte
org 04F0Eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

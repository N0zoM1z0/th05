; Real external symbols; no bitmap data or helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 0291eh
HMEM_FREE label far
org 0ae10h
_TEXT ends
BB_PLAYCHAR_TEXT segment byte public 'CODE' use16
assume cs:BB_PLAYCHAR_TEXT
public @BB_LOAD$QNXC
org (0f930h - 0ae10h)
@BB_LOAD$QNXC label near
org (10432h - 0ae10h)
BB_PLAYCHAR_TEXT ends
main_01 group BB_PLAYCHAR_TEXT
BB_PLAYCHAR_SHARED_GAP segment byte public 'CODE' use16
org (14ab0h - 1045bh)
BB_PLAYCHAR_SHARED_GAP ends
BB_PLAYCHAR_MAIN03_GAP segment byte public 'CODE' use16
org (209d0h - 14ab0h)
BB_PLAYCHAR_MAIN03_GAP ends
_DATA segment word public 'DATA' use16
org 018dch
_DATA ends
; The compiler owns the seven-byte filename; BSS aligns after its contribution.
_BSS segment word public 'BSS' use16
public _bb_playchar_seg, _playchar
org (0420ah - 018e4h)
_bb_playchar_seg label word
org (05773h - 018e4h)
_playchar label byte
_BSS ends
DGROUP group _DATA, _BSS
end

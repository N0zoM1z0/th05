; Complete dot helper: actual CODE/DGROUP context, no supplied instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
ITEM_DOT_TEXT segment byte public 'CODE' use16
org (0e152h - 0ae10h)
ITEM_DOT_TEXT ends
main_01 group ITEM_DOT_TEXT
ITEM_DOT_DATA_GAP segment byte public 'CODE' use16
org (14ab0h - 0e16eh)
ITEM_DOT_DATA_GAP ends
ITEM_DOT_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
ITEM_DOT_SHARED_SPACE ends
ITEM_DOT_MAIN03_SPACE segment byte public 'CODE' use16
org (209d0h - 15270h)
ITEM_DOT_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Foreign frames and independently anchored WORD globals, no initial values.
.386
.model large
_TEXT segment word public 'CODE' use16
org (0ae10h - 0130ch)
_TEXT ends
FOREIGN_CIRCLEX_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_CIRCLEX_MAIN01 ends
main_01 group FOREIGN_CIRCLEX_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_CIRCLEX_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_CIRCLEX_MAIN03 ends
main_03 group FOREIGN_CIRCLEX_MAIN03
_DATA segment word public 'DATA' use16
public ClipYT, ClipYT_seg, graph_VramZoom
org 00372h
ClipYT label word
org 00378h
ClipYT_seg label word
org 003cch
graph_VramZoom label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

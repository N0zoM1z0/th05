; Actual FAR helper addresses in the same public _TEXT, no helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_HLINE, GRCG_PSET
org (01690h - 010a4h)
GRCG_HLINE label far
org (01a44h - 010a4h)
GRCG_PSET label far
org (0ae10h - 010a4h)
_TEXT ends
FOREIGN_CIRCLE_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_CIRCLE_MAIN01 ends
main_01 group FOREIGN_CIRCLE_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_CIRCLE_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_CIRCLE_MAIN03 ends
main_03 group FOREIGN_CIRCLE_MAIN03
_DATA segment word public 'DATA' use16
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

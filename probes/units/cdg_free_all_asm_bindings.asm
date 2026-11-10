; Original MAIN shared library call context, with outside-only reserved extents.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
CDG_MAIN01_CONTEXT segment byte public 'CODE' use16
org (014AB0h - 0AE10h)
CDG_MAIN01_CONTEXT ends
main_01 group CDG_MAIN01_CONTEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_FREE
org (015238h - 014AB0h)
CDG_FREE label near
org (01526Eh - 014AB0h)
SHARED ends
CDG_RELEASE_FOREIGN_TAIL segment para public 'CODE' use16
org (0209D0h - 015280h)
CDG_RELEASE_FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

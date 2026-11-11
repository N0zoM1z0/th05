; Original MAIN _TEXT, SHARED, main_01/main_03 and DGROUP layout. The
; foreign source is symbols and segment extents only, with zero LEDATA.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SOUND_O, SOUND_I
org 0247eh
SOUND_O label near
org 02494h
SOUND_I label near
org 0363eh
_TEXT ends
FOREIGN_MAIN_JOY_PREFIX segment byte public 'CODE' use16
org (0ae10h - 03668h)
FOREIGN_MAIN_JOY_PREFIX ends
FOREIGN_MAIN_JOY_MAIN01 segment word public 'CODE' use16
org (014ab0h - 0ae10h)
FOREIGN_MAIN_JOY_MAIN01 ends
main_01 group FOREIGN_MAIN_JOY_MAIN01
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_MAIN_JOY_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_MAIN_JOY_MAIN03 ends
main_03 group FOREIGN_MAIN_JOY_MAIN03
_DATA segment word public 'DATA' use16
public js_bexist
org 003d0h
js_bexist label word
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

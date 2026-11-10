; Full 58-byte real TH05 SHARED input held/wait source-free context.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 09ca0h
FOREIGN_MAIN ends
main_01 group FOREIGN_MAIN
SHARED segment para public 'CODE' use16
assume cs:SHARED
public @input_reset_sense$qv, @input_sense$qv
org 00512h
@input_reset_sense$qv label far
org 0051ah
@input_sense$qv label far
org 00618h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org (015270h - 015102h)
FOREIGN_SHARED_TAIL ends
FOREIGN_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_MAIN03 ends
main_03 group FOREIGN_MAIN03
_DATA segment word public 'DATA' use16
public _vsync_Count1
org 0267ah
_vsync_Count1 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

; Real native frames and foreign bank address only, no payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment word public 'CODE' use16
org (0e020h - 0ae10h)
MAIN_01_TEXT ends
FOREIGN_SPARK_MASK_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e086h)
FOREIGN_SPARK_MASK_TAIL ends
main_01 group MAIN_01_TEXT, FOREIGN_SPARK_MASK_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_SPARK_MASK_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_SPARK_MASK_MAIN03 ends
main_03 group FOREIGN_SPARK_MASK_MAIN03
_DATA segment word public 'DATA' use16
public _sSPARKS
org 014aah
_sSPARKS label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

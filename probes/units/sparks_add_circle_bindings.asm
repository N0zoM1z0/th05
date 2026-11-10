; Source-independent native MAIN03 spark-circle CODE/DS provider addresses.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPARK_CIRCLE_MAIN01_FOREIGN segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
SPARK_CIRCLE_MAIN01_FOREIGN ends
main_01 group SPARK_CIRCLE_MAIN01_FOREIGN
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
SPARK_CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:SPARK_CIRCLE_TEXT
public VECTOR2_NEAR
org (0152dah - 015270h)
VECTOR2_NEAR label near
org (016ee8h - 015270h)
SPARK_CIRCLE_TEXT ends
SPARK_CIRCLE_TAIL segment byte public 'CODE' use16
org (0209d0h - 016f52h)
SPARK_CIRCLE_TAIL ends
main_03 group SPARK_CIRCLE_TEXT, SPARK_CIRCLE_TAIL
_DATA segment word public 'DATA' use16
public _spark_ring_offset, _sparks
org 041dch
_spark_ring_offset label word
org 05aeah
_sparks label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

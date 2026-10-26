; Whole native batch scope E0D2..E10E; foreign helpers/state only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPARK_BATCH_PREFIX segment byte public 'CODE' use16
assume cs:SPARK_BATCH_PREFIX
public @grcg_setcolor_direct_raw$qv, SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1, @spark_render
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (0df28h - 0ae10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (0e020h - 0ae10h)
@spark_render label near
org (0e0d2h - 0ae10h)
SPARK_BATCH_PREFIX ends
SPARK_BATCH_TEXT segment byte public 'CODE' use16
SPARK_BATCH_TEXT ends
; Even an empty foreign declaration keeps the accepted lifecycle group context.
SPARK_LIFE_TEXT segment byte public 'CODE' use16
SPARK_LIFE_TEXT ends
SPARK_BATCH_TAIL segment byte public 'CODE' use16
org (014ab0h - 0e10eh)
SPARK_BATCH_TAIL ends
main_01 group SPARK_BATCH_PREFIX, SPARK_BATCH_TEXT, SPARK_LIFE_TEXT, SPARK_BATCH_TAIL
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
FOREIGN_SPARK_BATCH_MAIN03 segment word public 'CODE' use16
org (0209d0h - 015270h)
FOREIGN_SPARK_BATCH_MAIN03 ends
main_03 group FOREIGN_SPARK_BATCH_MAIN03
_DATA segment word public 'DATA' use16
public _sparks
org 05aeah
_sparks label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

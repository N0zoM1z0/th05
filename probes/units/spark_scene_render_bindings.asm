; Authentic MAIN01 source prefix and foreign graphics, target-backed DS context.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPARK_SCENE_PREFIX segment byte public 'CODE' use16
assume cs:SPARK_SCENE_PREFIX
public @grcg_setcolor_direct_raw$qv, SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1, @spark_render
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (0df28h - 0ae10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (0e020h - 0ae10h)
@spark_render label near
org (0e0d2h - 0ae10h)
SPARK_SCENE_PREFIX ends
SPARK_SCENE_RENDER_TEXT segment byte public 'CODE' use16
SPARK_SCENE_RENDER_TEXT ends
SPARK_SCENE_TAIL segment para public 'CODE' use16
org (014ab0h - 0e110h)
SPARK_SCENE_TAIL ends
main_01 group SPARK_SCENE_PREFIX, SPARK_SCENE_RENDER_TEXT, SPARK_SCENE_TAIL
SPARK_SCENE_SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SPARK_SCENE_SHARED ends
SPARK_SCENE_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
SPARK_SCENE_MAIN03 ends
main_03 group SPARK_SCENE_MAIN03
_DATA segment word public 'DATA' use16
public _sparks
org 05aeah
_sparks label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

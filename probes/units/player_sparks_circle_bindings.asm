; Original MAIN01 and SHARED physical frames; real main03 source wrapper.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
PLAYER_SPARK_MAIN01_FOREIGN segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
PLAYER_SPARK_MAIN01_FOREIGN ends
main_01 group PLAYER_SPARK_MAIN01_FOREIGN
SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SHARED ends
PLAYER_SPARK_RING_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_SPARK_RING_TEXT
public @SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II
org (016ee8h - 015270h)
@SPARKS_ADD_CIRCLE$Q20%SUBPIXELBASE$TI$TI%T1II label near
org (0176b8h - 015270h)
PLAYER_SPARK_RING_TEXT ends
PLAYER_SPARK_RING_TAIL segment byte public 'CODE' use16
org (0209d0h - 0176ceh)
PLAYER_SPARK_RING_TAIL ends
main_03 group PLAYER_SPARK_RING_TEXT, PLAYER_SPARK_RING_TAIL
_DATA segment word public 'DATA' use16
public _player_pos
org 036d2h
_player_pos label word
org 036d6h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

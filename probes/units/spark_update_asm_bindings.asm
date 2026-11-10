; Original MAIN01 physical prefix, near Point return and uninitialized pool.
; No source-generated instruction or game-state initialization in the binder.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SPARK_UPDATE_PREFIX segment byte public 'CODE' use16
assume cs:SPARK_UPDATE_PREFIX
public @PlayfieldMotion@update_seg1$qv
org (0be1ah - 0ae10h)
@PlayfieldMotion@update_seg1$qv label near
org (0e086h - 0ae10h)
SPARK_UPDATE_PREFIX ends
SPARK_UPDATE_TEXT segment byte public 'CODE' use16
SPARK_UPDATE_TEXT ends
SPARK_UPDATE_AFTER segment para public 'CODE' use16
org (014ab0h - 0e0e0h)
SPARK_UPDATE_AFTER ends
main_01 group SPARK_UPDATE_PREFIX, SPARK_UPDATE_TEXT, SPARK_UPDATE_AFTER
SPARK_UPDATE_SHARED segment para public 'CODE' use16
org (015270h - 014ab0h)
SPARK_UPDATE_SHARED ends
SPARK_UPDATE_MAIN03 segment byte public 'CODE' use16
org (0209d0h - 015270h)
SPARK_UPDATE_MAIN03 ends
main_03 group SPARK_UPDATE_MAIN03
_DATA segment word public 'DATA' use16
public _sparks
org 05aeah
_sparks label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

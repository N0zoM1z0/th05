; Actual foreign entry points/state and outside-owned context only.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 0e086h
AFTER_BASE equ 0e0d0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 023c6h
IRAND label far
org MAIN01_BASE
_TEXT ends
SPARK_UPDATE_PREFIX segment byte public 'CODE' use16
assume cs:SPARK_UPDATE_PREFIX
public TILES_INVALIDATE_AROUND
org (0bad2h - MAIN01_BASE)
TILES_INVALIDATE_AROUND label near
public @PlayfieldMotion@update_seg1$qv
org (0be1ah - MAIN01_BASE)
@PlayfieldMotion@update_seg1$qv label near
org (UNIT_START - MAIN01_BASE)
SPARK_UPDATE_PREFIX ends
SPARK_LIFE_TEXT segment byte public 'CODE' use16
SPARK_LIFE_TEXT ends
SPARK_UPDATE_TEXT segment byte public 'CODE' use16
SPARK_UPDATE_TEXT ends
SPARK_UPDATE_AFTER segment para public 'CODE' use16
org (SHARED_BASE - AFTER_BASE)
SPARK_UPDATE_AFTER ends
main_01 group SPARK_LIFE_TEXT, SPARK_UPDATE_PREFIX, SPARK_UPDATE_TEXT, SPARK_UPDATE_AFTER
SPARK_UPDATE_SHARED segment para public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
SPARK_UPDATE_SHARED ends
SPARK_UPDATE_MAIN03 segment byte public 'CODE' use16
org (DGROUP_BASE - MAIN03_BASE)
SPARK_UPDATE_MAIN03 ends
main_03 group SPARK_UPDATE_MAIN03
_DATA segment word public 'DATA' use16
public _tile_invalidate_box, _spark_ring_offset, _sparks
org 3502h
_tile_invalidate_box label byte
org 41dch
_spark_ring_offset label word
org 5aeah
_sparks label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Original external symbols only; no function bodies, state or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_CIRCLEFILL
org 0100eh
GRCG_CIRCLEFILL label far
public GRCG_LINE
org 01716h
GRCG_LINE label far
org 0ae10h
_TEXT ends
LASER_RENDER_TEXT segment byte public 'CODE' use16
assume cs:LASER_RENDER_TEXT
public @grcg_setcolor_direct_raw$qv
org 013f4h
@grcg_setcolor_direct_raw$qv label near
public @LASER_RENDER_RAY$QRX14LASER_COORDS_T
org 02816h
@LASER_RENDER_RAY$QRX14LASER_COORDS_T label near
org 07ed5h
LASER_RENDER_TEXT ends
LASER_MAIN01_TAIL segment byte public 'CODE' use16
org 01b85h
LASER_MAIN01_TAIL ends
main_01 group LASER_RENDER_TEXT, LASER_MAIN01_TAIL
LASER_SHARED_CONTEXT segment para public 'CODE' use16
assume cs:LASER_SHARED_CONTEXT
public VECTOR2_AT
org 03b0h
VECTOR2_AT label far
org 07c0h
LASER_SHARED_CONTEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
main_03 group LASER_SC_TEXT
LASER_MAIN03_CONTEXT segment byte public 'CODE' use16
org 0b760h
LASER_MAIN03_CONTEXT ends
_DATA segment word public 'DATA' use16
public _drawpoint
org 036feh
_drawpoint label byte
public _lasers
org 0578ch
_lasers label byte
public _laser_line_endpoint
org 0c0a6h
_laser_line_endpoint label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

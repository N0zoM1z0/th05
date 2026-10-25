; Real foreign frames/symbols only; no initialized payload or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_OFF
org 0083ah
EGC_OFF label far
public GRAPH_PACK_PUT_8_NOCLIP
org 03778h
GRAPH_PACK_PUT_8_NOCLIP label far
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 006b8h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public @pi_mask_setup_egc_and_advance$qv
@pi_mask_setup_egc_and_advance$qv label near
org 011d1h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _PI_MASKS
org 006deh
_PI_MASKS label word
public _pi_mask_ptr
org 027b4h
_pi_mask_ptr label word
public _pi_mask_y
org 027b6h
_pi_mask_y label word
public _pi_put_masked_vram_offset
org 027b8h
_pi_put_masked_vram_offset label word
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

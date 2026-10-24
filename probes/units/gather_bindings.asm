; Symbol-only real MAIN gather context. Two ASM copy helpers are external.
; Only holes outside the two complete compiler CODE contributions occur.
; No instructions, target arrays, dummy helpers, DATA values, or .stack.
.386
.model large

MAIN03_BASE equ 15270h
ADD_START equ 16F8Bh
RUN_START equ 170A2h
IFNDEF GATHER_ADD_SIZE
GATHER_ADD_SIZE equ 0FCh
ENDIF
IFNDEF GATHER_RUN_SIZE
GATHER_RUN_SIZE equ 129h
ENDIF
ADD_END equ (ADD_START + GATHER_ADD_SIZE)
RUN_END equ (RUN_START + GATHER_RUN_SIZE)
SHARED_BASE equ 14AB0h
DGROUP_BASE equ 209D0h

_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
GATHER_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - 0AE10h)
GATHER_SHARED_GAP ends

GATHER_VECTOR_TEXT segment word public 'CODE' use16
assume cs:GATHER_VECTOR_TEXT
public VECTOR2_AT
org 03B0h
VECTOR2_AT label far
GATHER_VECTOR_TEXT ends

GATHER_MAIN03_GAP segment byte public 'CODE' use16
org (MAIN03_BASE - (SHARED_BASE + 03B0h))
GATHER_MAIN03_GAP ends

GATHER_ADD_TEXT segment word public 'CODE' use16
assume cs:GATHER_ADD_TEXT
public @PlayfieldMotion@update_seg3$qv
org 0Ch
@PlayfieldMotion@update_seg3$qv label near
public @grcg_setcolor_direct_seg3_raw$qv
org 0A2h
@grcg_setcolor_direct_seg3_raw$qv label near
public @gather_point_render$qii
org 0C2h
@gather_point_render$qii label near
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG3
org 017C0h
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG3 label near
public @SET_GATHER_TEMPLATE_TO_BULLET_TE$QR8GATHER_T
org 01D00h
@SET_GATHER_TEMPLATE_TO_BULLET_TE$QR8GATHER_T label near
org (ADD_START - MAIN03_BASE)
GATHER_ADD_TEXT ends

; The foreign ASM copy routine occupies this outside-contribution interval.
GATHER_RUN_TEXT segment byte public 'CODE' use16
assume cs:GATHER_RUN_TEXT
public @SET_BULLET_TEMPLATE_TO_GATHER_TE$QR8GATHER_T
@SET_BULLET_TEMPLATE_TO_GATHER_TE$QR8GATHER_T label near
org (RUN_START - ADD_END)
GATHER_RUN_TEXT ends

GATHER_TAIL_TEXT segment byte public 'CODE' use16
assume cs:GATHER_TAIL_TEXT
public _bullets_add_regular, _bullets_add_special
org (17204h - RUN_END)
_bullets_add_regular label near
org (17218h - RUN_END)
_bullets_add_special label near
GATHER_TAIL_TEXT ends
main_03 group GATHER_ADD_TEXT, GATHER_RUN_TEXT, GATHER_TAIL_TEXT

GATHER_DGROUP_GAP segment byte public 'CODE' use16
org (DGROUP_BASE - 17218h)
GATHER_DGROUP_GAP ends

_DATA segment word public 'DATA' use16
public _drawpoint
org 036FEh
_drawpoint label dword
public _bullet_template
org 0577Eh
_bullet_template label byte
public _gather_circles
org 09BFAh
_gather_circles label byte
public _gather_template
org 09EA6h
_gather_template label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

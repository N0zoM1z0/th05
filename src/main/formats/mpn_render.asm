; Semantic MPN tile blitter; reviewed native handwritten-ASM inference.
; Candidate architecture: maintained TH04 MPN renderer and native TH05 ABI.
.386
.model large
locals
include types.inc
include symbols.inc

MPN_ROWS equ MPN_TILE_H

; All four planes share one source cursor and the same destination origin.
COPY_IMAGE_PLANE macro video_segment
 mov ax, video_segment
 call near ptr mpn_copy_plane
endm

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public MPN_PUT
MPN_PUT proc far
 ; Far Pascal (left, top, image). Capture the argument frame before saving SI.
 mov bx, sp
 push si
 mov si, ss:[bx+MPN_ARG_IMAGE]
 cmp si, _mpn_last_image
 ja short @@done
 shl si, MPN_IMAGE_SHIFT
 push di
 ; VRAM destination = signed(left / 8) + top * 80.
 mov ax, ss:[bx+MPN_ARG_LEFT]
 mov di, ss:[bx+MPN_ARG_TOP]
 mov dx, di
 sar ax, 3
 shl di, 2
 add di, dx
 shl di, 4
 add di, ax
 push ds
 mov ds, _mpn_images_seg
 COPY_IMAGE_PLANE SEG_PLANE_B
 COPY_IMAGE_PLANE SEG_PLANE_R
 COPY_IMAGE_PLANE SEG_PLANE_G
 COPY_IMAGE_PLANE SEG_PLANE_E
 pop ds
 pop di
@@done:
 pop si
 retf 6
MPN_PUT endp
 even

; Private ABI: AX=video segment, DS:SI=next image plane, DI=VRAM origin.
; Clear DF is incoming. Each call consumes one plane and restores its origin.
public mpn_copy_plane
mpn_copy_plane proc near
 mov es, ax
 mov cx, MPN_ROWS
@@row:
 movsw
 add di, (VRAM_ROW_BYTES - MPN_ROW_BYTES)
 loop @@row
 sub di, (MPN_ROWS * VRAM_ROW_BYTES)
 ret
mpn_copy_plane endp
public mpn_render_end
mpn_render_end label byte
_TEXT ends
end

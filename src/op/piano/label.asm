; Maintained semantic TH05 piano kernels, pinned ReC98 b6ba5b0a candidate.
.386
.model large
locals
include types.inc
include symbols.inc
PIANO_LABEL_FONT_H equ 8
PIANO_LABEL_FONT_W equ 8
PIANO_LABEL_ROWS equ 8
; This procedure starts at an original odd intra-contribution address.
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public @piano_label_put_raw
@piano_label_put_raw proc near
	xor	ah, ah
	shl	al, 3 ; *= PIANO_LABEL_FONT_H
	add	ax, offset _sPIANO_LABEL_FONT
	mov	si, ax
	mov	cx, PIANO_LABEL_ROWS

@@row_loop:
	movsb
	add	di, (ROW_SIZE - (PIANO_LABEL_FONT_W / BYTE_DOTS))
	loop	@@row_loop
	retn
@piano_label_put_raw endp
public piano_label_end
piano_label_end label byte
SHARED ends
end

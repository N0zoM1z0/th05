; Maintained semantic TH05 piano kernels, pinned ReC98 b6ba5b0a candidate.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc
PIANO_LEFT equ 384
PIANO_H equ 15
PIANO_KEY_W equ 4
PIANO_BLACK_H equ 9
PIANO_BLACK_PRESSED_H equ 8
PIANO_OCTAVES equ 8
PIANO_OCTAVE_W equ (7*PIANO_KEY_W)
PIANO_VRAM_LEFT equ (PIANO_LEFT/8)
PIANO_VRAM_W equ ((PIANO_OCTAVES*PIANO_OCTAVE_W)/8)
; Three filled pixels and one key-edge pixel, repeated through a video word.
PIANO_KEYS_WHITE equ (((1 shl PIANO_KEY_W)-2)*(1+(1 shl 4)+(1 shl 8)+(1 shl 12)))
.code SHARED
public _piano_part_keys_put_raw
_piano_part_keys_put_raw proc near
	push	di
	push	si
	mov	ah, 3
	call	@grcg_setcolor_direct_raw$qv
	add	di, PIANO_VRAM_LEFT
	mov	ax, PIANO_KEYS_WHITE
	mov	dl, PIANO_H

@@white_key_loop:
	mov	cx, PIANO_VRAM_W / 2
	rep stosw
	add	di, ROW_SIZE - PIANO_VRAM_W
	dec	dl
	jnz	short @@white_key_loop
	mov	ah, 1
	call	@grcg_setcolor_direct_raw$qv
	mov	si, offset _PIANO_KEYS_BLACK
	sub	di, ROW_SIZE * PIANO_H
	mov	dl, PIANO_BLACK_H

@@black_key_loop:
	mov	cx, PIANO_VRAM_W / 2
	rep movsw
	sub	si, PIANO_VRAM_W
	add	di, ROW_SIZE - PIANO_VRAM_W
	dec	dl
	jnz	short @@black_key_loop
	pop	si
	pop	di
	retn
_piano_part_keys_put_raw endp


; void __fastcall near @piano_pressed_key_put(
; 	void far *vram_at_x0_and_top_of_part<es:di>, char onkai
; )
public @piano_pressed_key_put
@piano_pressed_key_put proc near
	cmp	al, ONKAI_REST
	jnz	short @@note_is_active
	retn
; ---------------------------------------------------------------------------

@@note_is_active:
	push	bx
	push	di
	mov	ah, al
	and	ah, ONKAI_NOTE_MASK
	xor	bh, bh
	mov	bl, ah
	shr	al, 4
	mov	dl, PIANO_OCTAVE_W
	mul	dl
	mov	dl, cs:PIANO_KEY_PRESSED_TOP[bx]
	add	bx, bx
	add	ax, cs:PIANO_NOTE_LEFT[bx]
	mov	cx, ax
	shr	ax, 3
	add	di, ax
	and	cl, 7
	jmp	cs:BLACK_OR_WHITE[bx]

@@white_key:
public piano_white_key
piano_white_key label near
	shr	dl, cl
	mov	al, cl
	mov	cx, PIANO_BLACK_H

@@white_key_top_loop:
	mov	es:[di], dl
	add	di, ROW_SIZE
	loop	@@white_key_top_loop
	mov	cl, al
	mov	al, (111b shl 5)	; bottom part of any pressed key
	shr	al, cl
	mov	cx, PIANO_H - PIANO_BLACK_H

@@white_key_bottom_loop:
	mov	es:[di], al
	add	di, ROW_SIZE
	loop	@@white_key_bottom_loop
	jmp	short @@ret
; ---------------------------------------------------------------------------

@@black_key:
public piano_black_key
piano_black_key label near
	xor	dh, dh
	ror	dx, cl
	mov	cx, PIANO_BLACK_PRESSED_H

@@black_key_loop:
	mov	es:[di], dx
	add	di, ROW_SIZE
	loop	@@black_key_loop

@@ret:
	pop	di
	pop	bx
	retn

; ---------------------------------------------------------------------------
public BLACK_OR_WHITE, piano_dispatch_end
BLACK_OR_WHITE label word
	dw offset @@white_key	; C
	dw offset @@black_key	; C#
	dw offset @@white_key	; D
	dw offset @@black_key	; D#
	dw offset @@white_key	; E
	dw offset @@white_key	; F
	dw offset @@black_key	; F#
	dw offset @@white_key	; G
	dw offset @@black_key	; G#
	dw offset @@white_key	; A
	dw offset @@black_key	; A#
	dw offset @@white_key	; B

piano_dispatch_end label byte
public PIANO_NOTE_LEFT, piano_key_positions_end
PIANO_NOTE_LEFT label word
 dw (PIANO_LEFT+(0*PIANO_KEY_W))
 dw (PIANO_LEFT+(0*PIANO_KEY_W)+(PIANO_KEY_W/2))
 dw (PIANO_LEFT+(1*PIANO_KEY_W))
 dw (PIANO_LEFT+(1*PIANO_KEY_W)+(PIANO_KEY_W/2))
 dw (PIANO_LEFT+(2*PIANO_KEY_W))
 dw (PIANO_LEFT+(3*PIANO_KEY_W))
 dw (PIANO_LEFT+(3*PIANO_KEY_W)+(PIANO_KEY_W/2))
 dw (PIANO_LEFT+(4*PIANO_KEY_W))
 dw (PIANO_LEFT+(4*PIANO_KEY_W)+(PIANO_KEY_W/2))
 dw (PIANO_LEFT+(5*PIANO_KEY_W))
 dw (PIANO_LEFT+(5*PIANO_KEY_W)+(PIANO_KEY_W/2))
 dw (PIANO_LEFT+(6*PIANO_KEY_W))
piano_key_positions_end label byte
@piano_pressed_key_put endp
public piano_keys_end
piano_keys_end label byte
end

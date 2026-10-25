; Maintained semantic TH05 piano kernels, pinned ReC98 b6ba5b0a candidate.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc
.code SHARED
public @piano_fm_part_put_raw
@piano_fm_part_put_raw proc near
	call	@piano_current_note_from
	push	ds
	push	fs
	pop	ds
	cmp	al, _piano_notes_cur.fm[si]
	jnz	short @@note_changed
	cmp	al, _piano_notes_prev.fm[si]
	jz	short @@ret

@@note_changed:
	mov	ah, _piano_notes_cur.fm[si]
	mov	_piano_notes_prev.fm[si], ah
	mov	_piano_notes_cur.fm[si], al
	call	_piano_part_keys_put_raw
	mov	ah, 5
	call	@grcg_setcolor_direct_raw$qv
	mov	al, _piano_notes_cur.fm[si]
	call	@piano_pressed_key_put

@@ret:
	pop	ds
	retn
@piano_fm_part_put_raw endp
public piano_fm_end
piano_fm_end label byte
end

		.8086
		.model tiny
		.code
		org 100h
public start, entry, print_procs, findentry, fixup
public proc_count, proc_names, proc_entries, moveup_indirect
public member_O, member_I, member_S, member_G, member_M, inner_moveup
start:
		jmp	short entry

var102		dw 0
aNoComSoft	db 'No COM-Soft !!!',13,10,10,'$'

entry:
		cld
		mov	cx, word ptr proc_count
		or	cx, cx
		jz	short error
		mov	si, 80h
		lodsb
		or	al, al
		jz	short print_procs

@scanargs:
		lodsb
		cmp	al, 13
		jz	short print_procs
		cmp	al, 32
		jz	short @scanargs
		jmp	short findentry

; Outputs names of all embedded COM files and then exits
print_procs:
		mov	cx, word ptr proc_count
		mov	si, offset proc_names
		mov	dl, 13
		mov	ah, 2		; INT=21/AH=02h - WRITE CHARACTER TO STANDARD OUTPUT
		int	21h
		mov	dl, 10
		int	21h
@outerloop:
		push	cx
		mov	dl, 32
		int	21h
		mov	cx, 8
@innerloop:
		lodsb
		mov	dl, al
		int	21h
		loop	@innerloop
		mov	dl, 32
		int	21h
		pop	cx
		loop	@outerloop
		mov	dl, 13
		int	21h
		mov	dl, 10
		int	21h
		mov	ah, 4Ch		; INT=21/AH=4Ch - TERMINATE WITH RETURN CODE
		int	21h
; ---------------------------------------------------------------------------

findentry:
		mov	bx, offset proc_entries
		mov	cx, word ptr proc_count
		mov	si, offset proc_names
@loop:
		mov	word ptr var102, si
		mov	di, 5Dh		; Standard FCB 1 filename
		push	cx
		mov	cx, 8
		repe cmpsb
		jz	short fixup
		add	bx, 2
		mov	si, word ptr var102
		add	si, 8
		pop	cx
		loop	@loop

error:
		mov	dx, offset aNoComSoft
		mov	ah, 9		; INT=21/AH=09h - WRITE STRING TO STANDARD OUTPUT
		int	21h
		mov	ah, 4Ch		; INT=21/AH=4Ch - TERMINATE WITH RETURN CODE
		int	21h
; ---------------------------------------------------------------------------

; Fixup FCB and args before continuing
; BX points to the entry in proc_entries
fixup:
		; Copy FCB 2 into FCB 1
		mov	di, 5Ch
		mov	si, 6Ch
		mov	cx, 10h
		rep movsb
		; Move arguments
		mov	si, 80h
		lodsb
		mov	dl, al
@skipspace:
		lodsb
		dec	dl
		cmp	al, 32
		jz	short @skipspace
@skipnonspace:
		lodsb
		dec	dl
		cmp	al, 13
		jz	short @moveargs
		cmp	al, 32
		jnz	short @skipnonspace
@moveargs:
		inc	dl
		mov	di, 80h
		mov	al, dl
		stosb
		or	dl,dl
		jz	short @emptyargs
		dec	si
		mov	cl, dl
		xor	ch, ch
		rep movsb
@emptyargs:
		mov	byte ptr [di], 13
		; setup registers for moventry
		mov	ax, [bx]
		mov	cx, [bx+2]
		mov	si, ax
		sub	cx, ax
		mov	di, 100h
		jmp	moveup_indirect

; ---------------------------------------------------------------------------
; Five game-specific subprograms are independently bounded in the
; authenticated launcher. These are *lengths*, never copied payload bytes.
O_BYTES equ 926
I_BYTES equ 1009
S_BYTES equ 6564
G_BYTES equ 8377
M_BYTES equ 311
MAX_SUBPROGRAMS equ 32

proc_count dw 5
proc_names label byte
    db '-O      ', '-I      ', '-S      ', '-G      ', '-M      '
    db (MAX_SUBPROGRAMS - 5) * 8 dup(' ')
proc_entries label word
    dw member_O, member_I, member_S, member_G, member_M, inner_moveup
    dw (MAX_SUBPROGRAMS + 1 - 6) dup(0)
moveup_indirect:
    call inner_moveup

; The five child payloads below belong to independent source owners and
; are never included in this reconstruction. ORG reserves their authentic
; span only so that the near transfer call resolves by *ordinary* TLINK.
member_O label byte
    org $+O_BYTES
member_I label byte
    org $+I_BYTES
member_S label byte
    org $+S_BYTES
member_G label byte
    org $+G_BYTES
member_M label byte
    org $+M_BYTES

inner_moveup:
    rep movsb
    pop ax
    mov ax, 100h
    push ax
    retn

end start

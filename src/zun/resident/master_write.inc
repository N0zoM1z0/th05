; Original Master MS-DOS file write near-Pascal register logic.
func FILE_WRITE
	push	BP
	mov	BP,SP
	push	SI
	push	DI
	cmp	file_BufferSize,0
	je	short @@DIRECT
	@@buf	= (RETSIZE+2)*2
	@@wsize	= (RETSIZE+1)*2
	mov	BX,[BP+@@wsize]
	mov	SI,[BP+@@buf]
@@WLOOP:
	mov	CX,file_BufferSize
	sub	CX,file_BufPtr
	sub	CX,BX
	sbb	AX,AX
	and	CX,AX
	add	CX,BX
	les	DI,file_Buffer
	add	DI,file_BufPtr
	sub	BX,CX
	add	file_BufPtr,CX
	push	DS
	mov	DS,[BP+@@buf+2]
	shr	CX,1
	rep	movsw
	adc	CX,CX
	rep	movsb
	pop	DS
	or	AX,AX
	jns	short @@LOOPEND
	push	DS
	push	BX
	mov	CX,file_BufferSize
	mov	BX,file_Handle
	lds	DX,file_Buffer
	mov	AH,40h
	int	21h
	pop	BX
	pop	DS
	jc	short @@WERROR
	cmp	file_BufferSize,AX
	jne	short @@WERROR
	mov	file_BufPtr,0
	add	WORD PTR file_BufferPos,AX
	adc	WORD PTR file_BufferPos+2,0
@@LOOPEND:
	or	BX,BX
	jne	short @@WLOOP
	mov	AX,1
	jmp	short @@DONE
	EVEN
@@DIRECT:
	push	DS
	mov	CX,[BP+@@wsize]
	mov	BX,file_Handle
	lds	DX,[BP+@@buf]
	mov	AH,40h
	int	21h
	pop	DS
	jnc	short @@EXIT
@@WERROR:
	mov	file_ErrorStat,1
	xor	AX,AX
@@EXIT:
	add	WORD PTR file_BufferPos,AX
	adc	WORD PTR file_BufferPos+2,0
	add	AX,-1
	sbb	AX,AX
@@DONE:
	pop	DI
	pop	SI
	mov	SP,BP
	pop	BP
	ret	6
	EVEN
endfunc

; Original Master MS-DOS file read near-Pascal register logic.
func FILE_READ
	push	BP
	mov	BP,SP
	push	SI
	push	DI
	@@buf	= (RETSIZE+2)*2
	@@bsize	= (RETSIZE+1)*2
	cmp	file_BufferSize,0
	je	short @@DIRECT
	mov	BX,[BP+@@bsize]
	les	DI,[BP+@@buf]
@@RLOOP:
	mov	AX,file_InReadBuf
	cmp	file_BufPtr,AX
	jb	short @@MADA_ARU
	add	WORD PTR file_BufferPos,AX
	adc	WORD PTR file_BufferPos+2,0
	push	BX
	push	DS
	mov	CX,file_BufferSize
	mov	BX,file_Handle
	lds	DX,file_Buffer
	mov	AH,3Fh
	int	21h
	pop	DS
	pop	BX
	cmc
	sbb	DX,DX
	and	AX,DX
	mov	file_InReadBuf,AX
	jz	short @@EOF
	mov	file_BufPtr,0
@@MADA_ARU:
	mov	SI,file_InReadBuf
	sub	SI,file_BufPtr
	sub	SI,BX
	sbb	AX,AX
	and	SI,AX
	add	SI,BX
	mov	AX,ES
	or	AX,DI
	je	short @@LOOPEND
	or	SI,SI
	je	short @@LOOPEND
	push	SI
	push	DS
	mov	CX,SI
	mov	AX,file_BufPtr
	lds	SI,file_Buffer
	add	SI,AX
	shr	CX,1
	rep	movsw
	adc	CX,CX
	rep	movsb
	pop	DS
	pop	SI
@@LOOPEND:
	add	file_BufPtr,SI
	sub	BX,SI
	jne	short @@RLOOP
	jmp	short @@EXITLOOP
	EVEN
@@DIRECT:
	push	DS
	mov	CX,[BP+@@bsize]
	mov	BX,file_Handle
	lds	DX,[BP+@@buf]
	mov	AH,3Fh
	int	21h
	pop	DS
	add	WORD PTR file_BufferPos,AX
	adc	WORD PTR file_BufferPos+2,0
	mov	BX,CX
	sub	BX,AX
	je	short @@EXITLOOP
@@EOF:
	mov	file_Eof,1
@@EXITLOOP:
	mov	AX,[BP+@@bsize]
	sub	AX,BX
	pop	DI
	pop	SI
	pop	BP
	ret	6
	EVEN
endfunc

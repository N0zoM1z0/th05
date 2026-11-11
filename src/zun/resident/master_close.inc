; Original Master MS-DOS file close near-Pascal register logic.
func FILE_FLUSH
	mov	BX,file_Handle
	cmp	BX,-1
	je	short @@F_IGNORE
	mov	AX,file_BufPtr
	cmp	file_InReadBuf,AX
	jae	short @@F_READ
	push	DS
	mov	CX,file_BufPtr
	lds	DX,file_Buffer
	mov	AH,40h
	int	21h
	pop	DS
	jc	short @@ERROR
	add	WORD PTR file_BufferPos,AX
	adc	WORD PTR file_BufferPos+2,0
	cmp	file_BufPtr,AX
	je	short @@WDONE
@@ERROR:
	mov	file_ErrorStat,1
@@WDONE:
	mov	file_BufPtr,0
	ret
@@F_READ:
	cmp	file_InReadBuf,0
	je	short @@F_IGNORE
	mov	DX,AX
	mov	CX,0
	add	DX,WORD PTR file_BufferPos
	mov	file_InReadBuf,CX
	mov	file_BufPtr,CX
	adc	CX,WORD PTR file_BufferPos+2
	mov	AX,4200h
	mov	BX,file_Handle
	int	21h
	mov	WORD PTR file_BufferPos,AX
	mov	WORD PTR file_BufferPos+2,DX
@@F_IGNORE:
	ret
endfunc
func FILE_CLOSE
	call	FILE_FLUSH
	mov	AH,3Eh
	int	21h
	mov	file_Handle,-1
@@IGNORE:
	ret
endfunc

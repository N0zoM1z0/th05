; Original Master MS-DOS file seek near-Pascal register logic.
func FILE_SEEK
	call	FILE_FLUSH
	cmp	BX,-1
	je	short @@ERROR
	push	BP
	mov	BP,SP
	@@pos	= (RETSIZE+2)*2
	@@dir	= (RETSIZE+1)*2
	mov	AL,[BP+@@dir]
	mov	AH,42h
	mov	DX,[BP+@@pos]
	mov	CX,[BP+@@pos+2]
	int	21h
	pop	BP
	mov	AX,4201h
	mov	DX,0
	mov	CX,DX
	int	21h
	mov	file_Eof,0
	mov	WORD PTR file_BufferPos,AX
	mov	WORD PTR file_BufferPos+2,DX
@@ERROR:
	ret	6
endfunc
func FILE_TELL
	mov	AX,file_BufPtr
	xor	DX,DX
	add	AX,WORD PTR file_BufferPos
	adc	DX,WORD PTR file_BufferPos+2
	ret
endfunc

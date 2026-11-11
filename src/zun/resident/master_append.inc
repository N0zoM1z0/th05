; Original Master MS-DOS file append near-Pascal register logic.
func FILE_APPEND
	push	BP
	mov	BP,SP
	@@filename = (RETSIZE+1)*2
	mov	AX,0
	mov	BX,file_Handle
	cmp	BX,-1
	jne	short @@EXIT
	mov	AX,3d02h
	push	AX
if LDATA
	push	word ptr [BP+@@filename+2]
endif
	push	word ptr [BP+@@filename]
	_call	DOS_AXDX
	or	AX,DX
	mov	file_Handle,AX
	mov	CX,AX
	xor	AX,AX
	mov	file_InReadBuf,AX
	mov	file_BufPtr,AX
	mov	file_Eof,AX
	mov	file_ErrorStat,AX
	mov	WORD PTR file_BufferPos,AX
	mov	WORD PTR file_BufferPos+2,AX
	inc	DX
	jz	short @@EXIT
	mov	BX,CX
	xor	CX,CX
	mov	DX,CX
	mov	AX,4202h
	int	21h
	mov	WORD PTR file_BufferPos,AX
	mov	WORD PTR file_BufferPos+2,DX
	mov	AX,1
@@EXIT:	pop	BP
	ret	DATASIZE*2
endfunc

; Original Master MS-DOS file ropen near-Pascal register logic.
func FILE_ROPEN
	push	BP
	mov	BP,SP
	@@filename = (RETSIZE+1)*2
	xor	AX,AX
	mov	BX,file_Handle
	cmp	BX,-1
	jne	short @@EXIT
if LDATA
	push	word ptr [BP+@@filename+2]
endif
	push	word ptr [BP+@@filename]
	nopcall	DOS_ROPEN
	sbb	BX,BX
	or	AX,BX
	mov	file_Handle,AX
	xor	AX,AX
	mov	file_InReadBuf,AX
	mov	WORD PTR file_BufferPos,AX
	mov	WORD PTR file_BufferPos+2,AX
	mov	file_BufPtr,AX
	mov	file_Eof,AX
	mov	file_ErrorStat,AX
	lea	AX,[BX+1]
@@EXIT:
	pop	BP
	ret	DATASIZE*2
	EVEN
endfunc

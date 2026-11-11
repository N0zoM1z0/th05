; Original Master MS-DOS puts2 near-Pascal register services.
func DOS_PUTS2
	mov	BX,SP
	mov	CX,SI
	_push	DS
	_lds	SI,SS:[BX+RETSIZE*2]
	lodsb
	or	AL,AL
	je	short @@EXIT
	mov	AH,2
@@CLOOP:	cmp	AL,0ah
	jne	short @@NOT_LF
	mov	DL,0dh
	int	21h
	mov	AL,0ah
@@NOT_LF:
	mov	DL,AL
	int	21h
	lodsb
	or	AL,AL
	jne	short @@CLOOP
@@EXIT:
	_pop	DS
	mov	SI,CX
	ret	DATASIZE*2
endfunc

; Original Master MS-DOS axdx near-Pascal register services.
func	DOS_AXDX
	push	BP
	mov	BP,SP
	axval	= (RETSIZE+1+DATASIZE)*2
	string	= (RETSIZE+1)*2
	_push	DS
	_lds	DX,[BP+string]
	mov	AX,[BP+axval]
	int	21h
	_pop	DS
	sbb	DX,DX
	xor	AX,DX
	sub	AX,DX
	pop	BP
	ret	(1+DATASIZE)*2
endfunc

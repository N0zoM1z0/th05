; Original Master MS-DOS free near-Pascal register services.
public DOS_FREE
func MEM_FREE
DOS_FREE label proc
	push	BP
	push	ES
	mov	BP,SP
	mov	ES,[BP+(RETSIZE+2)*2]
	mov	AH,49h
	int	21h
	pop	ES
	pop	BP
	ret	2
endfunc

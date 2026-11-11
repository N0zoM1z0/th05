; Original Master MS-DOS ropen near-Pascal register services.
func DOS_ROPEN
endfunc
func FONTFILE_OPEN
	mov	BX,SP
	filename = (RETSIZE+0)*2
	mov	AH,3dh
	mov	AL,byte ptr file_sharingmode
	_push	DS
	_lds	DX,SS:[BX+filename]
	int	21h
	_pop	DS
	jc	short OPEN_ERROR
	ret	DATASIZE*2
	EVEN
OPEN_ERROR:
	mov	AX,FileNotFound
	ret	DATASIZE*2
endfunc

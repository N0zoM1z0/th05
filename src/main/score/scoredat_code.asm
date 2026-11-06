; MAIN-only GENSOU.SCR byte transforms and unsigned additive checksums.
; References: maintained TH04 scoredat_code.asm and ReC98 scoredat_code_asm.asm.
.386
.model large
include types.inc
include symbols.inc
SCORE_ROTATE_BITS equ 3

main_01 group SCORE_CODE_TEXT
SCORE_CODE_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP

public @SCOREDAT_DECODE$QV
@SCOREDAT_DECODE$QV proc near
 push si
 mov bx, offset _hi
 mov si, bx
 mov cx, (size SCORE_PAYLOAD - 1)
 mov dx, word ptr [bx+SCORE_SECTION.SS_key1]
 add bx, SCORE_SECTION.SS_payload
decode_forward:
 mov al, [bx+1]
 ror al, SCORE_ROTATE_BITS
 xor al, dh
 add al, dl
 add [bx], al
 inc bx
 loop decode_forward
 add [bx], dl

 mov cx, size SCORE_PAYLOAD
 xor bx, bx
 xor dx, dx
 mov ax, [si+SCORE_SECTION.SS_sum]
 add si, SCORE_SECTION.SS_payload
decode_checksum:
 mov bl, [si]
 add dx, bx
 inc si
 loop decode_checksum
 sub ax, dx
 pop si
 ret
@SCOREDAT_DECODE$QV endp

public @SCOREDAT_ENCODE$QV
@SCOREDAT_ENCODE$QV proc near
 push si
 mov bx, offset _hi
 mov si, bx
 xor dx, dx
 xor ax, ax
 add bx, SCORE_SECTION.SS_payload
 mov cx, size SCORE_PAYLOAD
encode_checksum:
 mov dl, [bx]
 add ax, dx
 inc bx
 loop encode_checksum
 mov [si+SCORE_SECTION.SS_sum], ax
 call IRAND
 mov word ptr [si+SCORE_SECTION.SS_key1], ax

 xor dx, dx
 add si, (size SCORE_SECTION - 1)
 mov cx, size SCORE_PAYLOAD
encode_backward:
 add dl, al
 sub [si], dl
 mov dl, [si]
 ror dl, SCORE_ROTATE_BITS
 xor dl, ah
 dec si
 loop encode_backward
 pop si
 ret
@SCOREDAT_ENCODE$QV endp

public scoredat_code_end
scoredat_code_end label byte
SCORE_CODE_TEXT ends
end

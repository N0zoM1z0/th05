; Exact near-Pascal 386 zero-fill helper used by all eleven stage pools.
; The caller pushes the byte offset followed by the 32-bit element count.
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group CLEAR_DWORDS_TEXT
CLEAR_DWORDS_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public clear_dwords, clear_dwords_end
clear_dwords proc near
    mov bx, sp
    push di
    mov di, ss:[bx + FRAME_DEST_OFFSET]
    mov cx, ss:[bx + FRAME_DWORD_COUNT_OFFSET]
    push ds
    pop es
    xor eax, eax
    rep stosd
    pop di
    ret 4
clear_dwords endp
clear_dwords_end label byte
CLEAR_DWORDS_TEXT ends
end

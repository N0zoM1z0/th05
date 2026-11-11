; Generate the original 256-byte horizontal-flip lookup table at runtime.
; Construct every reversed-byte lookup value at runtime, preserving the
; original 8086 register protocol and the native far return convention.
.386
.model large
locals
include types.inc
include symbols.inc
SHARED segment byte public 'CODE' use16
assume cs:SHARED, ds:DGROUP
public _hflip_lut_generate, hflip_lut_generate_end
_hflip_lut_generate proc far
    push di
    xor ax, ax
    mov di, offset _hflip_lut
    xor dl, dl
    jmp short @@store
@@next:
    xor dl, dl
    mov cx, BITS_PER_BYTE
@@reverse_bits:
    rol al, 1
    rcr dl, 1
    loop @@reverse_bits
@@store:
    mov [di], dl
    inc di
    inc al
    jnz short @@next
    pop di
    retf
_hflip_lut_generate endp
hflip_lut_generate_end label byte
SHARED ends
end

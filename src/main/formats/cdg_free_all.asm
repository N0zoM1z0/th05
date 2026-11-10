; Complete shared CDG bank release: 64 slots, descending native order.
; The referenced handwritten TH04 cdg_load.asm documents this device/resource
; routine's control semantics; this code is a reconstruction, not a source copy.
.386
.model large
locals
include types.inc
include symbols.inc

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public CDG_FREE_ALL
CDG_FREE_ALL proc far
    push si
    mov si, CDG_SLOT_COUNT - 1
@@next_slot:
    push si
    ; The actual provider shares this CS and still returns as FAR Pascal.
    push cs
    call CDG_FREE
    dec si
    jge short @@next_slot
    pop si
    retf
CDG_FREE_ALL endp
public cdg_free_all_end
cdg_free_all_end label byte
SHARED ends
end

; Shared byte ring: overlapping WORD samples, low-byte cursor wrap, near ABI.
; Candidate: ReC98 b6ba5b0a th04/math/randring.inc, both MAIN instances.
.386
.model large
include types.inc
include symbols.inc
RING_CURSOR_BYTE equ 0

SAMPLE_RING_WORD macro
 mov bx, _randring_p
 mov ax, word ptr _randring[bx]
 inc byte ptr _randring_p[RING_CURSOR_BYTE]
endm

; Each Pascal helper consumes one WORD without creating a BP frame.
; BX snapshots the real entry SP only after the ring index is no longer live.
DEFINE_RING_READERS macro instance
 public @randring&instance&_next16$qv
@randring&instance&_next16$qv proc near
 SAMPLE_RING_WORD
 ret
@randring&instance&_next16$qv endp
 even

 public @RANDRING&INSTANCE&_NEXT16_AND$QUI
@RANDRING&INSTANCE&_NEXT16_AND$QUI proc near
 SAMPLE_RING_WORD
 mov bx, sp
 and ax, word ptr ss:[bx + RING_NEAR_ARGUMENT]
 ret RING_WORD_BYTES
@RANDRING&INSTANCE&_NEXT16_AND$QUI endp
 even

 public @RANDRING&INSTANCE&_NEXT16_MOD$QUI
@RANDRING&INSTANCE&_NEXT16_MOD$QUI proc near
 SAMPLE_RING_WORD
 xor dx, dx
 mov bx, sp
 div word ptr ss:[bx + RING_NEAR_ARGUMENT]
 mov ax, dx
 ret RING_WORD_BYTES
@RANDRING&INSTANCE&_NEXT16_MOD$QUI endp
endm

if RING_INSTANCE eq 1
 main_01 group RANDRING_1_TEXT
 RANDRING_1_TEXT segment word public 'CODE' use16
 assume cs:main_01, ds:DGROUP
 DEFINE_RING_READERS 1
 even
 public randring_readers_end
randring_readers_end label byte
 RANDRING_1_TEXT ends
else
 main_03 group RANDRING_2_TEXT
 RANDRING_2_TEXT segment word public 'CODE' use16
 assume cs:main_03, ds:DGROUP
 DEFINE_RING_READERS 2
 public randring_readers_end
randring_readers_end label byte
 RANDRING_2_TEXT ends
endif
end

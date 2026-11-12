# OP title-screen masked PI fade: four exact coverage stages

The decoded TH05 OP interval `[FA44,FA64)` is a complete **32-byte**
source-initialized near-DATA contribution, the real `_PI_MASKS[4][4]`
bank. Each entry is a sixteen-pixel row containing a four-pixel coverage
nibble repeated four times. Its four stages progress from sparse single
bits, through staggered vertical columns, to alternate checkerboard and
three-of-four-column coverage. The semantic row values and their order
are documented in the original
`_reference/ReC98/th03/formats/pi_put_masked[data].asm`. These are
**screen-fade coverage masks**, not stored sprite/PI image pixels or
an assembler instruction table.

The accepted OP title controller actually invokes `pi_put_masked_8()`
with the current phase `frame / FADE_FRAMES_PER_CEL`, so this bank is a
real gameplay-facing UI dependency. The separately accepted MAINE PI
fade bank uses the same semantic sixteen-word pattern, but the OP C
translation unit creates its **own** independent physical DATA and public
`PI_MASKS`, rather than borrowing MAINE addresses. Source-level bit
occupancy expressions construct the word values and the ordinary Borland
C object asserts the 4×4×2 extent.

The symbol-free binder retains the original OP code frames, DS `0EFE`
and only the outside `_DATA` prefix to offset `0A64`. The downstream
OP DATA suffix is reserved *after the 32-byte contribution* only to
satisfy the original MZ stack-memory requirement; it supplies no
candidate bytes, zero padding, instructions or relocation values.
The next 32 original all-zero bytes `[FA64,FA84)` remain **unknown**, not
part of this owner.

The focused native receipt
`.analysis/unit-replays/gpt-web-op-pi-mask-fade-a/receipt.json` records
two independent pinned Borland C producers, all original raw bytes,
complete OMF/LEDATA and MAP boundaries, empty ordered MZ fixups, and a
rejected compiled mutation that changes the final stage's last nibble.
No full OP or unrelated native replay was run.

# Input-sense source and deferred origin

`input_sense.asm` is maintained semantic source without exact acceptance or
authored credit. It adapts pinned ReC98 b6ba5b0a's
`th04/hardware/input_s.asm`, selected by `th05/input_s.asm`. The source contains
named firmware groups, key masks and game input bits rather than copied bytes.
It defines no keyboard bitmap, initialized state or joystick implementation.

| Artifact | Complete native range | CS / DS | key_det / shiftkey | js_stat / js_bexist | JS_SENSE |
| --- | --- | --- | --- | --- | --- |
| MAIN | 14FC2..150C8 | 14AB / 209D | 3064 / 3066 | 2646 / 03D0 | 0000:367A |
| OP | DF8E..E094 | 0D30 / 0EFE | 3A92 / 3A94 | 2E1A / 0544 | 0000:2CBA |
| MAINE | F102..F208 | 0E80 / 1011 | 29FA / 29FC | 1D96 / 022E | 0000:2E82 |

State columns are offsets in the actual game DS. Reset clears the input word
and the first legacy joystick-state word, then falls through at relative 8 to
the FAR sense entry. It does not have its own return. Both entry paths share
the RETF at relative 260. The complete 262-byte family contains 77 instructions
covering 261 bytes, then an instruction NOP at 261. That final EVEN alignment
byte has zero authored credit. The sole ordered MZ fixup is 251, at JS_SENSE.
No table, inert branch or runtime placeholder lies in the family.

Sense sets ES to zero and caches each BIOS keyboard-group byte in AH while
testing the applicable keys. TH05 ORs individual low/high input bytes. Diagonal
keypad flags are distinct high-byte values, rather than invented combinations
of cardinal flags. BIOS INT18/AH2 supplies Shift in AL; only bit 0 is stored.
If the joystick-existence word is nonzero, the real FAR vendor provider is
called and its AX result is ORed into the input word. Final AX reloads that
word. DS remains the game frame; ES/AX/flags are changed. No extra save/restore,
release clearing, IF guarantee or held-key delay is introduced. The normal
firmware/vendor clobber contracts still apply.

Reference history e4eed85c44283c8b48ac9a00cf152cfd5b9210d6 explicitly describes
manual tail-call optimization at the reset prefix. This supports deliberate
fallthrough organization; it does not independently prove the historical
source language of the complete ordinary no-argument FAR sense body. The
remaining keyboard tests and BIOS boundary could also come from C/intrinsics
or mixed source. No positive compiler-origin proof is asserted either.

The bounded 653-member vendor review finds related BIOS input work in
JSSENSE.ASM but a different aggregated bit-mapping algorithm. That is relevant
ancestry of the separate joystick provider, not proof that this whole game
wrapper is vendor code or original ASM. Both bodies and the trailing alignment
remain unknown ownership. Do not promote all 262 bytes from the eight-byte
reset prefix's evidence or count a non-returning prefix as a separate exact
function merely to gain credit.

Independent report `.analysis/input-sense-native-source-origin-review.json`
has SHA-256 `c09a88cd011ccad6dc966b679cec6e652ff543444b2df38e9e97aba9ab11f08a`.
It records complete native boundaries, NOP/fixup enumeration, history, bounded
vendor search and an independent semantic review of the maintained source.
No assembler, linker, Ghidra session or target runtime was run for this owner.
There is no live exact proposal, binder, producer or acceptance receipt.
The adjacent [held-input C++ failure](input_held.md) remains separate evidence.

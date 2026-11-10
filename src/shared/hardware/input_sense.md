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

## 2026-11-11: source-backed complete MAIN keyboard/joystick scanner accepted

The *entire* original two-entry SHARED family is now accepted for MAIN at
`[14FC2,150C8)` as `main-input-sense-original-asm`: **262/262 original
bytes**, 261 decoded instruction bytes and one original trailing `EVEN` NOP
at +261. Both real TASM32/TLINK producers reproduce the full raw scope,
original single far `JS_SENSE` relocation at +251, native shared code frame
14AB and DGROUP data frame 209D. The compiled semantic negative changes the
original PC-98 BIOS shift-status `MOV AH,2` to `MOV AH,3` and is rejected.

The source is the original-register implementation in
`src/shared/hardware/input_sense.asm`, whose *complete* TH05 key map,
low/high input byte OR masks, independent numpad diagonals, BIOS INT18
shift-mask logic, and joystick conditional callback are corroborated by the
pinned ReC98 `th04/hardware/input_s.asm` (`GAME=5`). A separate full native
review decodes all 78 instructions, confirms both live public entrypoints
at relative 0 and 8, and distinguishes the real reset-entry fallthrough
from an invented separately returning helper. The symbol-only binder anchors
real memory globals at DS03D0/2646/3064/3066 and JS_SENSE at 0000:367A;
no firmware bytes, joystick body, initialized DATA or BSS are supplied.

This is an *exact reviewed original-register ASM reconstruction*, not proof
that the game authors originally wrote the complete body in assembly rather
than C or a mixture. The earlier origin cautions above remain valid: the
known hand-optimized eight-byte reset prefix **by itself** would not justify
whole-body authorship. Here the independent **full** semantic source review,
complete 262-byte native comparison, all original relocation/entry boundaries,
and compiled negative provide the additional evidence for source-backed ASM
ownership. Credit is 261 assembly instruction bytes; the one NOP compares
but earns no authored credit. No C++ or vendor source authorship is inferred.

Strict receipt:
`.analysis/gpt-web-main-input-sense-262-asm-c/receipt.json`.

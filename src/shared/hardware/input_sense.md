# Input sense: reviewed original ASM

`input_sense.asm` is the accepted owner of the complete 262-byte two-entry
keyboard/joystick scanner in all three executables (`main-`, `op-` and
`maine-input-sense-original-asm` in `config/asm_families.toml`). Two TASM32/TLINK
producers reproduce every byte and the single far `JS_SENSE` relocation at
+251; the compiled negative changes the BIOS shift-status `MOV AH,2` to
`MOV AH,3`. Credit is the 261 instruction bytes; the trailing EVEN NOP at +261
compares with zero credit. The source follows pinned ReC98 b6ba5b0a
`th04/hardware/input_s.asm` (selected by `th05/input_s.asm`, `GAME=5`).

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

## Origin

ReC98 history e4eed85c describes manual tail-call optimization at the reset
prefix, which explains the fallthrough. On its own it would not prove that the
whole body was written in assembly. The ASM decision rests on the full native
review: both public entries at 0 and 8, the shared RETF at 260, register-carried
state and the shape of the keyboard tests. The bounded vendor review found
related BIOS input code in master.lib `JSSENSE.ASM`, but with a different bit
mapping, so the wrapper is game code rather than vendor code. The binder
anchors only DS globals and `JS_SENSE`; it supplies no firmware bytes,
joystick body, DATA or BSS.

Receipt (MAIN): `.analysis/gpt-web-main-input-sense-262-asm-c/receipt.json`.

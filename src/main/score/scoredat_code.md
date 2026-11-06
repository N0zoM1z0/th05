# MAIN score-section codec

The complete consecutive functions at MAIN C812..C882 are decoder 55 and
encoder 57: 112 instruction bytes, no NOPs, table, padding, initialized DATA
or BSS. Both are no-argument near Pascal procedures ending in RET0. Their
single original MZ relocation is relative 84, the real far IRAND call at
0000:23C6; CS is main_01/0AE1 and DS 209D.

Maintained TH04 `src/main/score/scoredat_code.asm` provides the semantic
forward/backward byte loops and checksum passes. TH05 changes to the real
five-place 92-byte payload, global 96-byte section, no argument, and packed
DX key caching. The full declared layout retains five 9-byte names, five 8-byte
scores, five stage bytes, cleared and unused bytes, plus both keys and the
WORD checksum. It agrees with unchanged canonical `src/op/hiscore/view.hpp`.
The section at DS 366E and all random-provider state remain foreign.

The decoder mutates 91 bytes from the following ciphertext byte, then adds
key1 to the final byte. It sums all 92 decoded bytes as unsigned values and
returns the stored WORD checksum minus that sum in AX. The genuine C++ byte
status interface reads AL; no stronger output or carry contract is invented.
The encoder stores the plaintext checksum, obtains both key bytes from actual
IRAND, then processes all 92 bytes backwards with DL feedback. SI is saved and
restored; no new allocation, error handling or state storage is introduced.

Original assembly classification has independent historical support: ReC98
commit 8dbb45050f5e6475d26ed146a03a8ad4db813c0e explicitly describes separate
micro-optimized ASM implementations for MAIN.EXE. The native frameless,
packed-key LOOP pipelines corroborate that family. This decision does not
relabel the failed OP C++ decoder or any compiler-generated body. Historical
source and assembler identity are unproved; TH04 acceptance does not transfer.
ReC98 c1b0a1c1 independently confirms that the parameterless TH05 variants
keep Pascal declarations for the shared ASM implementation.

The semantic source uses full structures, symbolic sizes, named byte passes
and a genuine far provider. The outside-only binder supplies no instructions,
section values or artificial stack. The final focused replay passes two fresh deterministic producers, complete
valid OMF/MAP, all 112 raw bytes and ordered fixup `[84]`. The shared
rotate 3-to-2 assembled negative is rejected for this complete family. Other accepted
objects and installed tool probes are reused after input identity checks;
no CPU behavior model or whole-game test is added.

Native boundary/language/ABI review:
`.analysis/scoredat-code-native-review.json`, SHA-256
`965557bfa853466f091fd26953ae083828e2e68cc74cd1b85a1db86db6420581`.

Accepted receipt: `.analysis/asm-replays/main-scoredat-code-b/receipt.json`,
SHA-256 `64fec90ba3e7ef3414dc246a8eee943f92407ce1489cd09a43d21c5c6249b30c`.
The first attempt's two positives matched all 112 bytes, but its negative
anchor was incorrectly placed in the type include. It has no receipt or credit.
The final shared constant lives in the assembly source and its negative is
actually assembled. Adoption adds 112 reviewed ASM instruction bytes; C/C++
counts and the unknown global authored denominator remain separate.

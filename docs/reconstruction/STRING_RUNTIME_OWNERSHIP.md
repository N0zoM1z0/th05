# Complete Borland string-library CODE ownership

Six complete distributed CL.LIB CODE contributions, totaling4,034 bytes, are
explicitly classified as third-party library code. They add zero authored
bytes, functions, C/C++ units or ASM credit. This is object provenance and
native linked-byte verification, not a reconstruction of Borland's source.
The authored denominator and global98% percentage remain unreviewed.

The original MAIN is the candidate-local-attested Japanese copy, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
CL.LIB retains its existing toolchain pin
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
All game/tool binaries and source archives remain private. No library payload
or target-derived code array is published.

| Complete member contribution | Original load interval | Bytes |
| --- | --- | ---: |
| ctor2 / _TEXT | A73C..A79C | 96 |
| ctor2 / _TEXTC | 1FD7A..1FE63 | 233 |
| ctor3 / _TEXT | A79C..A86B | 207 |
| ctor3 / _TEXTC | 1FE63..2007F | 540 |
| strings / _TEXT | A86B..AAB6 | 587 |
| strings / _TEXTC | 2007F..209C2 | 2371 |

The two CODE SEGDEFs in each member are independently complete. Ordinary
OMF checksums, segment identity, every LEDATA byte and full gapless coverage
are verified. All209 original fixup actions and131 original loader relocation
sites retain their order. Each full linked contribution occurs uniquely in
the pinned native image. No selected public/function slice, internal hole,
relocation sorting or byte normalization can substitute for a contribution.

Both string constructors and the complete string implementation use _TEXTC;
_TEXT additionally contains exception/cleanup support and compiler metadata.
Class CODE therefore does not imply that every byte is an instruction. No
instruction-byte denominator is inferred from the4,034 CODE bytes. The
separate102-byte strings DATA object is already reviewed by the earlier CL
DATA owner and adds no new credit here. BSS, preceding/following gaps and
other library members are not adopted by this decision.

## Native binding evidence

The unchanged distributed objects first reproduce the pinned calibration
image, then reproduce the original directly under the reviewed native symbol
model. Original object bytes, addends, OMF action identity, self-relative
semantics and linker transformations are retained. The two image buffers are
never edited. Calibration names and masked discovery alone supply no credit.

The existing CRT/DATA/BSS review supplies the native DGROUP and the eight
complete initialized-DATA anchors, including the strings DATA object. Its
late DATA shift-18 and late runtime BSS shift-20 are reused without changing
that review, old members or their evidence.

The combined _TEXTC base is calibration1FD8D versus original1FD7A. Its frame
moves1FD80 to1FD70 and its offsets change by-3; together these give the actual
linear change-19. Seven original far CALL/loader-relocation anchors verify
the native class frame and include both constructor entries. All other CODE
bindings remain unchanged. Every resulting relocation field is checked
against actual original bytes; this is rebinding unchanged OMF, not adjusting
a comparison result. The rest of MAIN's layout and whole EXE are unaccepted.

## NOPs and controls

All28 instruction NOPs are the actual first byte of TLINK's five-byte
NOP/PUSHCS/CALL relaxation. Per-contribution offsets are explicit in the proof:

| Contribution | Instruction NOP offsets |
| --- | --- |
| ctor2 / _TEXT | 32,59,79 |
| ctor2 / _TEXTC | none |
| ctor3 / _TEXT | 66,93,113,143,170,190 |
| ctor3 / _TEXTC | 116 |
| strings / _TEXT | 320,328,369,396,416,446,473,493,523,550,570 |
| strings / _TEXTC | 93,222,412,599,769,1059,1163 |

These are checked padding with zero authored credit and remain inside the
full comparisons. Two other90 bytes are not NOP instructions: ctor3/_TEXTC203
is embedded compiler metadata after the constructor's RETF200; strings/_TEXT526
is the CALL displacement inside the relaxation at523. The native gate accounts
for every90 byte and verifies each actual90/0E/E8 instruction sequence.

Each of the six contributions has its own fixed, nonrelocated byte-zero
mutation in the decoded distributed-OMF model. All six are rejected by the
same full-byte oracle as one-byte mismatches. These are model negatives,
not newly compiled or assembled game-source controls. The vendor review
executes no compiler, assembler, Wine process or new calibration build.

`scripts/review_string_runtime.py --check` replays the actual private objects,
calibration, native image, DATA anchors, complete bytes and ordered fixups.
`--structural-check` needs only public metadata and checks fixed full scopes,
identity/model pins, gapless coverage, fixup writes/order, NOP roles, controls
and native anchors. Nine regression tests exercise tampering and explicit
adoption. Neither mode grants authored-source acceptance.

The separate `config/reviewed_string_runtime_units.json` decision binds the
proof and this note. The normal ownership inventory accepts exactly the six
listed contributions. Unknown falls127882 to123848; MAIN unknown falls48172
to44138. Verified vendor CODE rises69770 to73804. All authored C/C++/ASM/DATA
counters, existing accepted sources and old ownership decisions stay unchanged.

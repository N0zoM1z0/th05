# MAIN compiler runtime ownership

An explicit ownership decision now classifies **24 additional complete CL.LIB
CODE contributions, 18,129 bytes**, as third-party runtime. This adds **zero
authored bytes, zero functions, zero C/C++ units and zero ASM credit**. It does
not reconstruct the runtime from maintained source or accept the whole EXE.
The authored denominator and global percentage remain unreviewed.

The original Japanese MAIN.EXE retains candidate-local-attested provenance,
not independently proved pristine status. Its complete SHA-256 is
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`;
its unrelocated MZ load-module SHA-256 is
`25860b4e1061c9d78f1cf7862716b02a88b150addfecf31de265acbca8361a41`.
The actual distributed Borland CL.LIB is pinned at
`7d53ed1864b8b778040aa8203ebe4e01385112d9b3f134744a461aec0b171ba7`.
Its member records, full CODE SEGDEF/LEDATA coverage, fixups and publics supply
positive runtime provenance. Reference names or opcode shapes alone do not.

## Complete adopted members

All coordinates below are original unrelocated MAIN load-module offsets.
CODE is the actual OMF class: a complete member can include compiler/runtime
constants, tables and linker padding. None of these bytes receives instruction
or authored credit. Each range is half-open and covers the whole real CODE
contribution, with no internal gap or selected function slice.

| Member | Original interval | Bytes |
| --- | --- | ---: |
| _abort | 45E8..4603 | 27 |
| atexit | 4654..4685 | 49 |
| errormsg | 484E..4878 | 42 |
| exit | 4878..4922 | 170 |
| ioerror | 4A79..4ACB | 82 |
| lseek | 4AE0..4B0D | 45 |
| setupio | 4E37..4EDB | 164 |
| toupper | 4EDB..4F0B | 48 |
| xxv | 4F9A..5223 | 649 |
| cputype | 5223..527F | 92 |
| fbrk | 56DA..583A | 352 |
| _pathops | 5B76..5C46 | 208 |
| flushall | 5D38..5D84 | 76 |
| fseek | 5D84..5F70 | 492 |
| fullpath | 5F70..62B2 | 834 |
| getenv | 634F..63BF | 112 |
| srchenv | 64CA..6511 | 71 |
| srchstr | 6511..6653 | 322 |
| setvbuf | 6653..6774 | 289 |
| write | 68BB..6A21 | 358 |
| writea | 6A21..6A7C | 91 |
| xfflush | 6A7C..6ABB | 63 |
| xx | 7077..A1C5 | 12622 |
| loadprog | AAB6..AE1D | 871 |

The large `xx` member implements Borland exception handling and RTTI, with
actual library publics including `__GetTypeInfo`, `__DynamicCast`,
`_ThrowException`, `_ReThrowException` and `__ExceptionHandler`. All 12 raw
calibration/native differing bytes are inside original OMF fixup fields, but
that observation alone would be insufficient. The review reconstructs every
byte from the unchanged distributed object and independently justified native
bindings. Its 187 fixup actions and all 20 original loader relocations retain
their actual order; sorting is forbidden.

`loadprog` ends with its genuine RET at AE1C. The zero at AE1D is outside this
member and remains unknown. The next accepted slowdown function starts AE1E.
AE10 is the paragraph frame of main_01, not a new function boundary; it lies
inside the last library call path. The complete native 871-byte function
contains 376 instructions and 14 real TLINK relaxation NOPs, at
AAD3/AB4D/AB5D/AB7B/AB99/ABAA/AC1B/AC5D/ACE7/AD50/AD68/ADC0/AE01/AE0C.
Each is followed by PUSH CS / CALL. They are compared normally and add zero
source credit. Across all24 adopted members, all116 actual far-call relaxation
NOPs are explicitly enumerated in `config/main_runtime_padding.json` as
checked vendor padding, with zero authored credit. The original OMF record
order is retained. This role metadata is orthogonal to the complete vendor
CODE owner and does not add to the79 checked padding bytes of accepted C/C++
units. The full library contribution is classified as vendor CODE;
this does not convert its NOPs into authored instructions.

## Independent native binding model

The older MAIN CL review accepted only complete members whose calibration
bytes already equaled the original. Most other runtime members refer to DATA
or BSS that moved in the calibration. A single DGROUP frame change does not
explain those differences: it was tested privately and grants no new scope.

The new model keeps every CODE address, object byte, OMF fixup identity,
displacement and linker transformation unchanged. Only the following native
symbol-address relationships are applied:

| Surface | Calibration | Original |
| --- | --- | --- |
| DGROUP load address | 209E0 | 209D0 |
| Late runtime DATA offsets | 2098..262C | original offsets minus 18 |
| Final runtime BSS offsets | C6B2..C748 | original offsets minus 20 |
| Initial SS | 2D13 | 2D11, separate from DGROUP |

The DATA interval includes the original initializer/exit markers, not game
CODE. Eight already reviewed complete initialized DATA objects independently
anchor the offset change: _abort31, files2 42, ioerror91, ctype257, signal38,
xx18, strings102 and loadprog40. Their actual complete library LEDATA bytes
occur uniquely at both retained and native DATA positions, with empty original
relocation lists. These unchanged prior DATA proofs are reused, not relabelled.
Early CRT DATA offsets remain unchanged. No arbitrary per-operand binding is
solved backward from target CODE words.

The real pinned C0L.OBJ, SHA-256
`09fe156e5dceb4afa30235e8d9cf7a17a40a91ee646babe16b3286731eb429a2`,
provides an independent object-level anchor for the startup's boundary fields.
Its actual CODE FIXUPP at B9 is an offset16 DGROUP reference to `_BSSEND`,
and B6 references `_BSS`. The four initializer/exit fields likewise refer to
`_INIT_`, `_INITEND_`, `_EXIT_` and `_EXITEND_`. Native startup clears
261A..C734 and iterates INIT25F6..2614 and EXIT2614..261A. Three real relocated
DGROUP immediates agree at209D. SS is checked separately and is never translated
as DGROUP; foreign segment bases also remain unchanged.

The complete final ordinary library BSS suffix has the pinned WORD-aligned
member order atexit128, sigdata4, xxv4, signal4 and xx10. The actual library
SEGDEF sizes and retained MAP order place it at calibration C6B2..C748.
The independently anchored native end C734 gives native C69E..C734, with xx's
own ten bytes at C72A..C734. This is a symbol binding model for the CODE proof;
BSS is uninitialized and receives no initialized-byte ownership credit.

## Gates, adoption and limits

`scripts/review_main_runtime.py` first reconstructs each complete unchanged
CL object against the real pinned calibration MZ/MAP. It then reconstructs
expected bytes with the fixed native addresses and compares the entire result
against the actual original MZ. It preserves complete ordinary LEDATA coverage,
original OMF record and fixup order, and the actual linker far-call relaxation
operation. Both comparisons require the complete contribution's unique byte
occurrence and all original ordered loader relocations. There is no masking,
patched candidate, synthetic executable, copied target instruction body or
normalization of compared bytes. No compiler, Wine, Ghidra, download or target
execution occurs. Existing accepted objects and installed execution proofs are
untouched.

`config/main_runtime_ownership.json` remains a proposal with hashes and full
control/native fixup evidence. `config/reviewed_main_runtime_units.json` is the
separate explicit adoption of exactly the 24 named complete members.
The gapless ownership overlay rejects overlap with any existing accepted or
vendor scope. It changes no previous C/C++/ASM receipt or source dependency.
Public CI verifies source/input identities, metadata, complete scope/coverage,
fixed binding transformations and adoption without pretending to read private
bytes. `--check` and ownership `--verify-targets` redo the actual byte proof.

Fourteen new public tests cover malformed credit/provenance, changed input
pins, unknown/duplicate/clipped members, DATA/BSS/SS confusion, missing anchors,
per-operand binding changes, relocation sorting, LEDATA gaps, out-of-range
writes, malformed hashes, foreign segment preservation, actual C0 OMF segment
roles, startup opcodes/zeroing topology and missing real relocations. Separate
private challenges reject seven actual byte/model failures: changed native
nonfixup CODE, changed native fixup bytes, wrong DATA or BSS offset changes,
reordered original loader relocations, a clipped complete extent and changed
library CODE. These are read-only mutated views; original files are untouched.

Previously adopted 31 CL members / 2,901 bytes retain their original evidence.
The present addition is not a blanket runtime-prefix exclusion. Ten other
complete library candidates remain deferred: xxas, farheap, signal, exec,
setenvp, new, xmsg, ctor2, ctor3 and strings. Unsupported group fixups, LIDATA,
unwritten SEGDEF gaps or remaining raw-byte differences require their own
reviews. No internal hole, inter-member alignment, C0 startup, Master include,
other target, game routine, DATA or asset receives ownership from this decision.

The observation universe stays319,268 bytes. Unknown ownership decreases from
153,745 to135,616; verified vendor CODE grows from50,007 to68,136. Authored C/C++
remains97,289 bytes /495 functions /310 units. Reviewed ASM remains separate.
The global authored denominator and percentage remain null.

Independent native/model/complete-boundary report:
`.analysis/vendor-review/main-runtime-independent-review.json`, SHA-256
`4e950255528366465e063cb50607bdf36579ec864a8d9c4fe313a55b9e8c4a75`.
Root actual negative review:
`.analysis/vendor-review/main-runtime-negative-review.json`, SHA-256
`99ec0452283426e0f3e523c9bb01c0fb3600e841c74a416111312f0226e16523`.

Final independent adoption/overlay gate:
`.analysis/vendor-review/main-runtime-final-gate-review.json`, SHA-256
`70481d0fb6eceec74e6825163207eb19609e2b9ca95fccab07ea3d322c48b2f7`.
All four incremental compiler plans are empty.

Full CI passes317 tests, including the14 new ownership/padding tests. Native
ownership replay and `review_main_runtime.py --check` also pass. Root final
audit is `.analysis/vendor-review/main-runtime-root-final-review.json`, SHA-256
`ac0524934853084a54b42f6ad2bae463141dabf76e8271c2ea983a74010c814c`.

Independent verification of all116 native padding roles:
`.analysis/vendor-review/main-runtime-padding-review.json`, SHA-256
`0cdcbdbaa8bd276ea12c2c3e2808e70844c24ae05822b09c95b39636e56d6ea4`.

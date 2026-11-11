# TH05 sound-effect controller candidate

The single natural TU `se.cpp` follows ReC98 `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th02/snd/se.cpp` (wrapped by`th04/snd_se.cpp`) and the TH04 maintained sound owners. `se.hpp` keeps the real SE-mode enum, unsigned-byte state, seventeen-entry priority arrays, Pascal far play entry, cdecl far update entry and master.lib `int pascal far bgm_sound(int)` ABI. The first declarations belong to SHARED before either definition.

Ordinary parameter access is `new_se`, and ordinary priority lookup is C++ indexing by the unsigned-byte current SE. The reference/TH04 register templates for SP/peek parameter retrieval and BL/BH array indexing are deliberately absent. Registers only appear at the genuine driver boundary: PMD interrupt`60h` consumes AH=`0Ch`, AL=effect; Beep receives the same selected effect zero-extended to the actual Pascal word argument. No carry-flag API is inferred.

Independent original decoding finds the same function bodies in all three pinned artifacts:

| Artifact | Play load address / actual frame:offset | Update load address | DS frame | BGM_SOUND frame:offset |
|---|---|---|---|---|
| MAIN | `14CE2` / `14AB:0232` | `14D1C` | `209D` | `0000:3C44` |
| OP | `D602` / `0D30:0302` | `D63C` | `0EFE` | `0000:3284` |
| MAINE | `EAE6` / `0E80:02E6` | `EB20` | `1011` | `0000:344C` |

These frames are read from actual original relocated far callers. In particular OP does not use a guessed D3D frame, and MAINE does not use calibration E7F. The complete original134-byte source contribution contains57 play instructions bytes, one`90` alignment byte at relative57, then76 update instruction bytes. There are no compiler tables or zero padding bytes. The sole original MZ relocation is relative101 (relative43 inside update), from its real BGM_SOUND call. Every local direct branch lands on an original instruction boundary.

The original/reference source explicitly inserts its inter-function NOP through `codestring`. This owner injects no codestring, emits no opcodes and supplies no padding bytes. Natural ordinary C++ parameter/index code may also compile differently. The private proposal therefore offers two complete function scopes, play57 and update76, from one TU compiled once per round. They are candidates until actual MAP bounds and full raw/ordered comparisons pass; neither full134 nor either function is presently claimed exact. A fresh diagnostic may be useful before two-producer registration. No alternative source variants have been prepared.

Both priority arrays were independently verified as seventeen bytes in each original against the readable semantic DB definitions in`th04/snd/se_priority[data].asm`. They remain foreign to this CODE TU; their separate maintained DATA owner is now [independently accepted](se_priority_data.md) in all three artifacts. The64-byte gaps between the second table and current state in OP/MAINE do not enlarge either array:

| Artifact | Priorities | Priority frames | Playing | Elapsed frame | Mode |
|---|---:|---:|---:|---:|---:|
| MAIN | `0800` | `0811` | `0822` | `0823` | `0835` |
| OP | `0980` | `0991` | `09E2` | `09E3` | `0A61` |
| MAINE | `065E` | `066F` | `06C0` | `06C1` | `06DB` |

All columns are offsets in the genuine DS frame above. This TU owns zero initialized DATA and BSS. The independent binders contain only foreign labels and ORG extents. Their DS gap begins at an outside-function paragraph, so missing the one original NOP does not shift DS or introduce a byte into a function. OP retains only the already accepted foreign Music Room DATA end at DS`2817`, without values or credit, to preserve a valid harness minimum allocation without `.stack`. All ORG values are below65536.

Private native evidence and actual instructions: `.analysis/semantic-sound-review/se-boundaries.json`. Config/control proposals: `se-candidates.json` in that directory. The sole source negative changes the initial driver-start frame from0 to1, a real one-frame sound-start delay. This preparation has run no compiler and has not changed kaja/modes, existing headers, core, live configs or acceptance.

Root diagnostic `se-natural-a` compiled this one natural TU once with the
pinned tools and real MAIN context. Play is60 bytes versus original57 and
update77 versus76; both remain entirely unaccepted. No negative or two-cold
acceptance is claimed. The public C symbols are not demangled function
boundaries under the strict scope parser; the proposed private function-scope
registrations are not adopted. Future acceptance needs genuine complete
compiler contributions, without relabelling C symbols or adding lookup/parameter
register templates. No additional compiler variants were tried.

## 2026-11-11: exact complete SE play/update functions in all three artifacts

The original MAIN far-Pascal `SND_SE_PLAY` (57 bytes) and far-cdecl
`_snd_se_update` (76 bytes) now compile exactly from maintained C++. They
also pass the identical complete native extents independently in OP and MAINE,
using each binary's original CODE, DATA, and `BGM_SOUND` far-call frames.
**Six complete functions / 399 C++ instruction bytes** are accepted.
The three inter-function `90` alignment bytes at MAIN `14D1B`, OP `D63B`,
and MAINE `EB1F` remain outside the compiled functions and earn no credit.

The real far-Pascal play entry fetches its word argument through the Borland
`SS:[SP+4]` interface and retains it in `DX`. The original priority comparison
loads the current effect into `BL`, clears `BH` and then indexes the existing
unsigned-byte priority table; `DX` preserves the new effect. This removes the
unwanted ordinary BP frame and three extra compiled bytes. Update likewise
uses `BL`/`BH` for its priority-frame lookup, removing the previous extra
byte without rewriting driver semantics. The genuine PMD `INT 60h`, Beep
far-Pascal call, unchecked state transitions and unsigned priority/age
comparisons are unchanged.

`se_play_body.inl`, `se_update_body.inl` and `se_driver_play.inl` share
maintained definitions with the original-order `se.cpp`. Each exact owner has
an independent one-function compiler source (`se_play.cpp`/`se_update.cpp`)
and a foreign-symbol-only binder for each artifact. This avoids injecting an
alignment NOP with `codestring`, duplicating function bodies, or treating a
partial compiler contribution as a complete owner. The existing accepted
34-byte priority DATA per binary is unchanged.

Focused receipts (two distinct positive producers, complete raw bytes, native
ordered relocations, and a compiled source negative per artifact):

- `.analysis/unit-replays/gpt-web-main-sound-se-both-a/receipt.json`
- `.analysis/unit-replays/gpt-web-op-sound-se-both-b/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-sound-se-both-b/receipt.json`

Each receipt selects exactly its two affected functions. The original ordered
fixups are empty for play and `[43]` for update. The single mutation per
artifact changes the actual play argument-stack word offset from `+4` to
`+6`; the oracle rejects the modified code. Whole-game linkage and packed
OP/MAINE executable identity are separate, not claimed by this acceptance.

# TH05 collection and update candidates

Natural semantic donor: maintained TH04 `src/main/item/items_update.cpp`.
TH05 behavior, complete returns, operands, data widths, branches and call frames
were independently reviewed in the supplied original MAIN. ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47` is disassembly corroboration; its old
IDA labels/digest are not our original-address oracle. Existing item20, splash10,
canonical entity/item enums, geometry and accepted headers are unchanged.

| New owner | Complete original range | Functions | Raw bytes |
| --- | --- | ---: | ---: |
| `extend.cpp` | `1CDAC..1CDFB` | extend check | 79 |
| `collect.cpp` | `1CDFB..1D0AD` | collect + miss penalty | 690 |
| `update.cpp` | `1D0AD..1D19E` | main update | 241 |

The rewards owner has605 collection instruction bytes, one zero padding byte,
a14-byte compiler switch table, then70 penalty instruction bytes. The table
starts at unit offset606 and all seven entries point to instruction boundaries
for real item types0..6. Its actual complete function boundary is the next real
penalty function at1D067. The distinct odd rewards start is a real function
boundary; no padding is inserted into source to imitate target bytes. All1,010
raw bytes must compare; at most995 instruction and14 semantic table bytes could
receive code credit. No initialized DATA or BSS is defined by these owners.
They are source candidates, not accepted contributions.

The functions use normal pointer-on-stack Pascal helpers with RET2, or the
observed no-argument near/far entries. No CF-returning or SI-input custom helper
is introduced. Semantic helper names are reconstructed; their actual complete
functions, argument frames and target locations are the evidence. The new
`update.hpp` supplies only local declarations and ordinary state-action macros.
It does not alter the frozen item/splash definitions.

TH05 differences from the donor are substantial:

- Point value depends on `y - dream*24 - 896`, or the external full-dream reward.
  Dream pickups fill dream, or award12,800 when already full. Full-power overflow
  can increase dream outside bomb attraction.
- Score delta receives the unsigned base reward directly. The times-two display
  latch is not used to double this score addition.
- Stage point items are a real BYTE at DS:36F5, adjacent to dream at36F6. The
  collector at1CF0F increments the byte without saturation; HUD code atD1AB also
  reads one byte. The reference listing's saturating word path is not applied.
- Point extends first raise performance and increment extends_gained even when
  lives is already99. Only that path applies the99 cap; direct1UP collection
  retains its own byte increment.
- Missing a point item lowers dream only between1 and128. Bomb/1UP misses lower
  performance, and the miss helper always refreshes dream HUD. TH04's separate
  missed-item accumulator behavior is absent.
- Main update sets the display latch only while processing attracted live items,
  then clears it after splash update. It does not preinitialize it before looping.

The main loop keeps the genuine `PlayfieldPoint` result of Motion.update_seg3.
The pre-clamp returned coordinates are necessary: pickup tests still use the
returned Y after current item Y is clamped, while collection reads the clamped
item field. A natural typed local may lower differently from historical physical
AX/DX usage. That is an explicit code-generation uncertainty; no pseudoregister,
instruction template, ASM body or inert barrier is used to force a result.

The big-power case retains the historical table-read-before-clamp order, including
its above-cap access whose result is immediately replaced. No extra target data
array or compensating guard is introduced. All score/counter tables remain
external semantic objects with their real word/byte widths.

## Ordered-fixup limitation

The original rewards offsets, in actual loader-table order, are:

```
485,478,469,460,398,318,286,237,138,78,683,678,593,531
```

An independent690-byte C++ producer may emit a different order even if every raw
byte matches. The observed grouping is consistent with a1024-byte producer
record boundary at collect+531. Taking the preceding natural init entry1CC0E as
producer start gives collect offset493, but original OMF/TU boundaries are not
available: this is an inference, not historical source-object proof. No init
body, artificial prefix, record rewriting, relocation sorting or forced metadata
is added to work around it. Keep any raw/order failures unaccepted.

An optional complete `item_miss_penalty(item_t near*)` scope covers
`1D067..1D0AD`,70 bytes, with two descending original fixups. It uses the same
single real source body and actual final-function contribution boundary; no
alternate implementation or artificial public label exists. Confirm the actual
compiler MAP spelling before registration. Accept this scope or the complete
690-byte owner, never both as overlapping credit. Its own negative changes
playperf_lower(4) to5, so the failed collection need not own its negative control.

Private proposals and address-only binders are under
`.analysis/item-update-{suggested.toml,boundary-review.json,bindings/}`. Aliases
are `th05/it_extnd.cpp`, `th05/it_rewrd.cpp`, `th05/it_updat.cpp`, GAME5/BINARY M,
main_03, ordinary pinned large-model flags with BP enabled. Bindings contain no
helper bodies, values or stack, and place all empty foreign segment declarations
at their true group frames. Full global game layout and standalone gameplay
remain separate from any bounded exact result.

`main-item-extends-a` accepts the complete79-byte extend helper from two
fresh raw/ordered producers and its compiled performance mutation.
`main-item-miss-penalty-d` separately accepts the complete70-byte final Pascal
function from two fresh producers and the real penalty mutation4→5. Its actual
MAP boundary is the compiler contribution end; no prefix fragment is credited.

Collection remains unaccepted. The natural rewards TU is689 versus original690;
all ordinary bytes correspond, but the original zero at collection+605 and
the switch-table address differ. A normal `-a2` trial did not resolve it and
was removed; no hand padding or producer-record manipulation is used. The
original nonmonotone ordered fixups remain a separate unresolved gate.

The natural main updater is248 versus original241. Its true typed Motion
return is DX:AX coordinates, not a far pointer. Two local word stores and
resulting memory-based comparisons account for the net7 extra bytes; the
pre-clamp coordinate semantics are correct. No fake return type, register
math template or optimizer barrier replaces that code. Evidence is the private
`main-items-update-spill-review.json`; the whole241 target remains unaccepted.


## Subsequent bounded ABI trial

The one genuine packed-return borrow trial emitted235 bytes and was stopped
after the first producer. Native instructions show the actual X return was
overwritten while evaluating the X pickup expression, which then became
SUB AX,AX; DX remained correct. There was no second producer or compiled
pull-speed negative. This long-borrow candidate is abandoned, not accepted.
The safe248 typed-point source was restored exactly from
`.analysis/item-update-before-abi.cpp`. Current status and native evidence
are recorded in `update_abi.md` and
`.analysis/item-update-abi-protocol-result.json`. No further ABI/register/
flags variant or donor BX/inline-ASM implementation is proposed. Accepted
immediate-return consumers retain their independent evidence.

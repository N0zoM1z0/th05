# Per-stage entity and effect reset candidate

The complete original function is `[12AC4,12BAD)` in MAIN's unrelocated MZ
program image:233 instruction bytes, one original segment fixup at relative98,
no tables or NOPs. It is the real C near cdecl `stage_state_init(void)` used
by the accepted stage runtime initializer. The owner defines no DATA or BSS.

Maintained TH04 `src/main/stage_state_init.cpp` supplies the ordinary reset
algorithm and buffer-helper interface. Its `unsigned long[]` storage aliases
are not reused. This owner passes real arrays of their complete canonical
records, using `sizeof(array) / sizeof(unsigned long)` solely as the genuine
foreign helper's word count. All eleven sizes match both the actual TH05
allocation extents and the original call arguments:

| Real pool | Count × record bytes | Allocation bytes | DWORD count |
| --- | ---: | ---: | ---: |
| hitshots | 24 ×14 | 336 | 84 |
| lasers | 32 ×24 | 768 | 192 |
| shots | 64 ×18 | 1152 | 288 |
| enemies | 32 ×64 | 2048 | 512 |
| sparks | 64 ×16 | 1024 | 256 |
| bullets | 400 ×32 | 12800 | 3200 |
| custom entities | 64 ×26 | 1664 | 416 |
| circles | 8 ×10 | 80 | 20 |
| items | 40 ×20 | 800 | 200 |
| point numbers | 280 ×16 | 4480 | 1120 |
| gather circles | 16 ×38 | 608 | 152 |

No oversized clear was found in these calls. Compatible accepted headers are
reused unchanged. The complete `custom_t`, `gather_t` and `gather_template_t`
definitions are repeated literally from their canonical headers to avoid
unrelated cheeto macros and a duplicate gather entity enum. No record is
shortened or replaced by an opaque byte/word array. The GAME5 point-number
record retains flag, age, full point, previous Y, unsigned width word, five
digits and its actual unused final byte, corroborated by pinned ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`
`th04/main/pointnum/pointnum.hpp` and BSS. Assertions cover every pool extent
and the new record's real offsets.

The original23-byte helper at `CF62..CF79` reads a near buffer offset and a
word DWORD count from its Pascal stack arguments and returns with RET4.
Its genuine interface is `void pascal near clear_dwords(void near *,unsigned)`;
no carry/bool/scalar result is invented. It preserves DS and DI, sets ES to
DS, and otherwise clobbers the observed working registers/flags. Its string
operation requires the normal clear direction flag. The C++ owner consumes
no result or flags and imports no helper instructions. That helper's original
language/ownership is not classified or credited here.

The only Master call is true far Pascal `grc_setclip` at0000:130C, with four
word bounds `(32,16,415,383)`. Code frame is AE1 and DS209D. Actual TH05 state
adds the shot cache/ring indices, frame/slowdown state and the real laser pool
to the donor's pattern. The complete14-byte gather template gets ring points8,
color9, radius1024, angle delta2 and zero velocity. Its existing center remains
untouched, matching the original. There are no pseudoregister algorithms,
inline ASM, fake callback prototypes or source padding.

Initial producer options retain only the donor's ordinary CODE/group selectors;
there is no new `-G`, frame option or flag search. Private native target
boundaries, every call/count, canonical-header hashes, literal record-copy
proof, outside-only binder and proposal are in `.analysis/stage-state-init/`.
The current corrected source remains unaccepted and requires fresh comparison.
Two fresh complete raw/original-order comparisons and its own ring-points8-to7
compiled negative remain required. Accepted headers and source are unchanged.

## Retained first producer and common-zero correction

`main-stage-state-init-a` stopped at its first producer's whole-contribution
gate:237 bytes instead of233. It compiled all complete-type/pool assertions,
but no second positive or negative was compiled. The actual237-byte size is
already present in the OMF before linking.

Both frame prologues and epilogues are identical. The extra four bytes come
from the initial two independent assignments: original code computes one zero
and stores that value first to the shot-cache count and then to the hitshot
ring index, taking eight bytes; two separate immediate-zero stores take12.
The subsequent instruction shapes and all eleven clear counts match. The
larger code moves the bounded foreign tail/shared/DATA layout by four bytes,
giving DATA209D:0004 and DS label offsets plus4, rather than changing any
entity record or pool extent. Its one segment-fixup position moves from98 to102.

The ordinary chained assignment
`hitshot_next_free_id = shots_alive_count = 0` was authorized to preserve
that shared value and the real shots-first/hitshot-second store order. Only
these two assignments changed; all types, headers, counts, options, binder and
remaining statements remain identical. No frame flag, physical register,
barrier, empty expression or layout variant was introduced. Exact output of
this source expression is still unproved until the new producer runs.

The first failed artifacts/source and
`.analysis/stage-state-init/first-a-native-review.json` remain intact. Its
historical boundary manifest is preserved separately; no237-byte observation
is relabeled as233-byte acceptance.

## Accepted focused b

`main-stage-state-init-b` passes both fresh deterministic whole233-byte raw
comparisons, the original ordered `[98]` fixup, all complete-type/pool assertions
and OMF checks. Its own compiled ring-points8-to7 control was rejected. The
ordinary shared-zero chain preserves the observed value flow and store order;
no flags, record layouts or allocation lengths changed. The first237-byte
producer remains a separate failed observation. CPP, header and maintained
binder are now frozen accepted dependencies.

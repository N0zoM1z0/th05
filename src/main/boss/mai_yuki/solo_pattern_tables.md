# Survivor pattern-pointer banks

Candidate semantic initialized DATA for MAIN load `22334..22358`, corresponding
to DS `1964..1988`. The entire 36-byte contribution consists of 18 near function
pointers. It contains no functions, assets, opaque values, alignment bytes or
original MZ relocation sites. It has not been compiled or accepted.

| DS start | Definition | Entries | Callback return |
| --- | --- | ---: | --- |
| 1964 | `yuki_solo_pattern_pair1` | 2 | bool |
| 1968 | `yuki_solo_pattern_pair2` | 2 | bool |
| 196C | `yuki_solo_pattern_final` | 5 | bool |
| 1976 | `mai_solo_laser_patterns` | 3 | void |
| 197C | `mai_solo_pattern_pair_middle` | 2 | bool |
| 1980 | `mai_solo_pattern_pair_final` | 2 | bool |
| 1984 | `mai_solo_pattern_pair_first` | 2 | bool |

All callbacks take no arguments and use the genuine near cdecl interface in
frame `1527`. Boolean completion returns in AL; the three inner laser
subpatterns return no completion value. The independent interface preserves
the canonical `MaiYukiPattern` and `MaiSoloLaserPattern` typedefs. Only the
small canonical ABI header is included, avoiding unrelated Boss state and
enum declarations. No existing header changes.

The original Yuki final bank deliberately repeats `yuki_solo_vector_stacks`
four times after `yuki_solo_snow_cross`; these are meaningful pattern-schedule
entries. Every initializer is a named real function, and all 15 distinct
providers already have accepted complete CODE evidence. No address integers,
casts between callback types, target-byte arrays or fake helper definitions
appear in the source.

Native indexed reads corroborate all seven banks: three in Yuki's survivor
update, one in Mai's laser cycle, and three in Mai's survivor update. Both
survivor updates write the same real current-pattern slot at DS `4438`.
Mai's nested laser callback uses the distinct void slot at DS `443A`.
Neither is the shared-fight Yuki callback at DS `4430` or shared-fight Mai
callback at DS `442E`. This DATA owner defines the banks only, leaving those
uninitialized runtime slots foreign.

The shared fight's five callback banks form a separate earlier DATA cohort.
Intervening dialogue filenames and BGM titles separate them from these survivor
banks. They are outside this complete contribution rather than folded into
an unexplained larger array.

The binder contributes only real foreign CODE labels, origin holes outside
the owned DATA, and the foreign DATA prefix ending at DS `1964`. The C++
producer supplies every owned pointer word. Main-03 frame `1527` and DS
`209D` are retained, without allocating a stack or substituting target data.
Actual compiler/MAP contribution size and gapless OMF LEDATA must prove that
the source owns precisely the whole 36-byte initialized DATA contribution.

Private `.analysis/mai-yuki-solo-tables-boundary-review.json` records the
original target/extent digests, exact bank bounds, true function identities,
accepted provider ownership, seven native cross-references, and empty original
ordered relocation list. `.analysis/mai-yuki-solo-tables-candidate.json`
proposes one initialized-DATA unit with DOS8.3 module `th05/b4_stbl.cpp` and
a fresh compiled negative swapping the first Mai bank's widening-fan and
turning-stack callbacks. This changes actual scheduling and linked DATA;
no CODE-only mutation can satisfy the DATA negative gate.

Only this new owner requires two fresh producers and its DATA-specific
negative. Existing unchanged provider evidence remains independent.

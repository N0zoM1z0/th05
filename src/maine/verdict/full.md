# Complete verdict logic family

`full.cpp` compiles ten natural C++ functions in native order, covering original
MAINE `[C5E7,D31F)`:3384 bytes,3350 instructions plus34 generated switch-table
bytes. All boundaries decode completely through their returns. There are no
NOPs, padding, emitted instruction bodies, DATA, BSS or asset definitions.

| Function | Complete bytes | Status |
| --- | ---: | --- |
| Three-digit formatter | 152 | Previously accepted |
| Score formatter | 170 | Previously accepted |
| Percentage formatter | 268 | Previously accepted |
| Million-fraction formatter | 121 | Previously accepted |
| Apply bonus | 340 | Previously accepted |
| Choose comment | 153 | Previously accepted |
| Main verdict calculation | 1748 | Newly accepted |
| Display comments | 66 | Previously accepted |
| Animate verdict | 108 | Newly accepted |
| Display stage scores | 258 | Previously accepted |

The new coverage is1856 bytes and two complete functions. The previous1528
bytes retain their coverage through four reused IDs and six additional IDs,
partitioning all ten complete functions without overlap. Each function body
lives once in `body/`; standalone wrappers include those same bodies. Reversing
the include factor restores every previously accepted function literally.
Guarded code selectors preserve the old standalone first-declaration contexts
and select one shared context only for this complete family.

The main calculation uses the unchanged complete128-byte Resident and eight-byte
Score types. It computes stage completion, enemy/item collection, bonus and
slowdown percentages; applies rank, starting lives/bombs, turbo, misses and bomb
penalties; clamps the signed result; then selects and reads two30-byte comments
through the actual far Pascal FILE APIs. The generated main tables are22 bytes.
No shortened resident, fake carry boolean or custom return facade is used.

Animation uses the real palette, PI, input and frame APIs plus standard
`outportb` hardware selectors. Its108 complete bytes include the original
nonmonotonic relocation list `[36,29,12,104,97,87,67,60,53,46]`. The coherent
family supplies a real compiler record context; no filler, copied opcode,
fixup sorting or OMF rewriting supplies that order.

The rank strings remain an external complete mutable `char[5][8]` with the
large model's default data distance. The maintained TH04 donor both declares
and defines that type. The draft's unsupported `const near` override generated
the same argument values with a different placement of `push DS`. Explicitly
spelling `&row[0]` alone changed no bytes; restoring the genuine object type
resolved the12-byte discrepancy. Original/calibration OMF has no type records
that could prove historical TH05 spelling, and physical DGROUP placement alone
does not establish a near C++ pointer type. API signatures, full array bounds,
foreign storage addresses, compiler options and linker layout are preserved.

`maine-verdict-full-family-c` contains two fresh deterministic actual producers
and the compiled completion-clamp46000-to-46001 control. All3384 raw bytes and
all50 original relocation sites in literal order match; the control is rejected.
The actual c OMF LEDATA ends are1018,2040,3062,3384 (record sizes
1018/1022/1022/322), identical in both positives and the negative. Animation's
observed local record cut is44; earlier speculative cuts are not producer
evidence. These actual records reproduce the original order without proving
the original compiler's historical chunk boundaries.
Failed a/b receipts remain unchanged. The whole-family trial is never imported
as additional coverage. `maine-verdict-full-scopes-c` revalidates those intact
MZ/MAP/OMF producers and projects ten complete function records with zero
compiler invocations. The single shared CODE control belongs to main; it is
not a claim of ten independently compiled function mutations.

Only this affected family was replayed. Unrelated accepted source closures and
records were preserved. The real foreign binder supplies master frame0, shared
frameE80, CODE frameA54 and DS1011, with no own internal holes or function bodies.
This demonstrates exact reproducibility from coherent maintained source, not
identity with the historical original translation unit or packed executable.

## Exact verdict score policy and two-comment disk protocol

The maintained 1,748-byte `verdict_main()` now names the *original* starting
life choices 1–6 and starting bomb choices 0–2 as values of two small switch
key domains. These selectors are never serialized as new enum objects;
`resident->credit_lives` and `resident->credit_bombs` retain their original
canonical 128-byte resident layout and original integer values. The first
and second kinds of starting resources continue to change **both** skill and
max_skill independently. The original missed-shot penalty caps at ten misses
and 30,000 per miss; the used-bomb penalty caps at fifteen and 15,000 each.
Named limit/per-use constants preserve the original saturating 300,000 and
225,000 penalties, the signed clamp and the rank multipliers.

The final score also indexes exactly two **30-byte** comment records from
the original archive: the score-selected comment record and a second record
with its own base displacement of 780 bytes. Each read remains 30 bytes and
is explicitly null-terminated at index 28. The names make the original
disk-record protocol visible without changing the `FILE_ROPEN` / `FILE_SEEK`
/ `FILE_READ` far ABI or any Japanese asset data.

All ten affected complete source owners in the same original 3,384-byte
translation-unit context were twice compiled with the real pinned Borland
producer. They matched **3,384/3,384 original bytes**, including both of the
main scoring function's compiler switch tables and every literal ordered MZ
relocation. The compiled semantic negative was rejected. Focused receipt:
`.analysis/unit-replays/gpt-web-verdict-scoring-policy-20261111/receipt.json`.
No additional CODE coverage, new denominator or unrelated MAINE cold replay
is inferred from this exact source-semantic improvement.

# Point-popup lifecycle

The native procedure bodies are init `[E16E,E179)` (11 bytes), invalidate
`[E17A,E1A6)` (44), and update `[E1A6,E215)` (111). Separate EVEN NOPs at E179
and E215 complete the old168-byte family extent. All original ordered MZ fixup
lists are empty; neither NOP has authored credit. No table or initialized DATA
belongs to these scopes. The accepted renderer starts at E216 and is excluded.
The initializer now has independent [11-byte C++ acceptance](init.md);
invalidation, update and both alignment bytes remain unaccepted.

`lifecycle.cpp` recovers ordinary C++ semantics, using the complete 16-byte
record also maintained in `stage_state_init.hpp`. The 280 records, 281 near
pointer list entries, two byte cursors, and first-yellow near pointer remain
foreign BSS. Invalidation uses the real near Pascal scalar interface with
previous Y at record offset 6 and current X at offset 2; they cannot be passed
as a contiguous SPPoint. The tile box height is set once, while its width is
updated only for nonfree records.

Update processes every flag except free (0) and pending removal (2) as alive.
It saves previous Y, moves upward by eight subpixels when the old unsigned
age is at least 24, and clips signed Y at -64 before incrementing age. Byte
age wraps, then values above 36 mark removal. The next update frees pending
removal. Only survivors enter the near pointer list; the first yellow is the
first surviving record in slots 200..279, and the output always ends in zero.
Init resets only the two byte cursors.

The initial binder failed before compilation because its near provider label
lacked ASSUME CS. After correcting that declaration, one natural `-k-`
producer compiled and linked successfully. Its complete contribution is
184 bytes: init 11, invalidate 47, update 126. It lacks the two native NOPs;
the invalidator lowers the two scalar arguments directly, and the updater
has a stack local/frame and different allocation and branch merging. The
strict size gate rejected it before a second positive or compiled negative.
No padding, ABI retagging, instruction transcription, flag search or ASM
promotion follows from this failure. The provisional entry is parked outside
the live exact manifest. That failed whole producer grants no acceptance;
the later independent initializer does not transfer credit to its neighbors.

The actual failed producer's DATA frame shifted by one paragraph because its
CODE extent was larger; this is not an accepted original layout.

`.analysis/check-pointnum-lifecycle.py` compares the original and retained
compiled C++ against an independent scalar model. All 68 pool cases pass,
including 15,360 update combinations of six flag values, all 256 ages and ten
signed-Y boundaries, uniform full/empty/removal pools, init write isolation,
list tails, previous coordinates and yellow selection. Entire generated
DGROUP states are compared, with SI/DI/BP/DS/SP and IF/DF checks. Invalidation
observes arguments and box values at the real RET4 boundary, with scratch
register clobbers; tile-provider effects are not modeled. This establishes
bounded semantic evidence, not exact acceptance or historical source identity.
Report `.analysis/pointnum-lifecycle-semantic-check.json`, SHA-256
`3520f2550feaf9d251bb5a3b69e1caa7650eba60e8b295b23ab96b43ca6259dc`.

The current standalone `invalidate.cpp` now uses the DOS `_AX` pseudoregister
to stage current X before the real previous-Y/current-X Pascal call. Two
fresh native producers reproduce the complete44-byte invalidator and its
empty ordered fixup list; the compiled height8→9 negative is rejected. This
is a byte-exact natural-C++ alternative, while the accepted reviewed ASM
family remains the sole CODE owner and the C++ source is intentionally not
added to the live exact manifest. The earlier43-byte scalar candidate remains
historical evidence. See [actual scalar-source trials](invalidate.md).

The initializer body is now shared literally through `init.inl`. Published
init/update declarations and definitions use their actual no-argument near
Pascal interface, with no record-layout change. No old accepted unit consumed
this header, and the retained184-byte failure/model is historical evidence,
not a fresh build after this source factoring.
The new independent [field-domain updater](update.md) emits111 bytes, but its
raw bytes still differ and it grants no credit. No old semantic model was rerun.

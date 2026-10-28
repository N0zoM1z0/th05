# Point-popup lifecycle: semantic recovery, no exact acceptance

The three complete MAIN functions are init `[E16E,E17A)` (12 bytes),
invalidate `[E17A,E1A6)` (44), and update `[E1A6,E216)` (112).
All original ordered MZ fixup lists are empty. Init-relative 11 and
update-relative 111 are alignment NOPs, with zero potential authored credit.
No table or initialized DATA belongs to these scopes. The adjacent accepted
renderer starts at E216 and is excluded.

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
the live exact manifest. All 168 target bytes remain unknown and uncredited.

Private producer: `.analysis/unit-replays/main-pointnum-lifecycle-natural-b/`;
failed initial binder: `main-pointnum-lifecycle-natural-a/`.
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

The later standalone `invalidate.cpp` uses a signed count and canonical
scalar conversions, without a coordinate local. Its complete43-byte output
passes full-pool semantic checks but remains one byte short of the native44;
all original168 lifecycle bytes remain unknown. The old184-byte producer and
its model evidence are unchanged. See [actual scalar-source trials](invalidate.md).

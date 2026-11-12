# ZUN resident entry: isolate the removal-branch compiler mismatch

The maintained natural `src/zun/resident/initialize.cpp` now tests the
successful `-R` removal path before the missing-resident error. It has the
same runtime behavior: if the segment exists, release it, print the removal
message and return 0; otherwise print "not found" and return 1.

This source change fixes the previous **9-byte length deficit** in the
complete native tiny-model `main()` contribution. The real Turbo C++ 4.02
`-c -O -b- -3 -Z -d -DGAME=5 -mt` compiler emits **269 bytes**, the
original complete length at child COM `[04A9,05B6)`. Linked with the genuine
C0T startup, accepted config source and correct symbol-only TASM binding,
its 5,886-byte COM matches **252 of the 269 original byte positions**.
Only **17 bytes** differ, at function-relative positions `+47..+5A`.
Both copies are identical outside the single `-R` removal/error branch;
the original emits a branch to the success path followed by the failure
print, while this variant places the success body first.

Two classes of eight additional real TCC/TASM/TLINK first-producer trials
checked whether equivalent error-first `if`, `else`, `goto` and `switch`
branches naturally preserve the historical block ordering without renewed
error-tail merging. Some reproduce the 269-byte/17-difference near match;
others shrink to 260 or grow to 271 bytes. None is fully exact. Input
snapshots and linked outputs are retained privately at
`.analysis/gpt-web-zun-early-errors-*20261112/` and
`.analysis/gpt-web-zun-remove-branch-*20261112/`, with runnable variant
scripts and compact result JSON in `.analysis/`.

**Status: natural C++ candidate, not accepted exact CODE.** The strict ZUN
manifest still credits only the independently exact 322-byte `cfg_init()`
and 320-byte initialized DATA. No ASM patch, optimizer barrier, borrowed
machine code, artificial return value or target bytes were introduced.
The next specific task is a natural control-flow shape that emits the
original branch order at `+47..+5A` *while retaining* the separate error
printing sites elsewhere in the function. Do not re-try the listed
error-first rewrites without a new code-generation hypothesis.

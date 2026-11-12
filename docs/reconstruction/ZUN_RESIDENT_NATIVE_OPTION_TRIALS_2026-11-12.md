# TH05 `-S` resident entry: 14 natural option-branch compiler trials

**Status: unaccepted.** The real original embedded ZUN resident COM has a
complete near-C++ `main()` at child offsets `[04A9,05B6)` (**269 bytes**).
The maintained `src/zun/resident/initialize.cpp` still compiles to a
**260-byte** natural source contribution. This work neither changes the
accepted 322-byte `cfg_init()`, the independently accepted 320-byte
semantic initialized DATA, nor any original vendor-code owner.

The original and previously recovered `C0T.OBJ`, far/near provider
bindings, canonical 128-byte Resident, true option/error strings, and
foreign symbol addresses are shared by these experiments. All candidate
sources preserve the externally observable `-R` resident removal,
`-D` debug activation, invalid-option messages, resident-already-present
failure, allocation failure, successful initializer, and configuration
failure. No candidate contains a self-assignment, dummy call, `volatile`
optimizer barrier, synthetic state variable, instruction byte, or
assembler workaround. None edits a maintained public source file.

## Actual pinned compiler first-producer results

Each candidate was compiled with the original Turbo C++ 4.02 tiny-model
arguments `-c -I. -O -b- -3 -Z -d -DGAME=5 -mt`, in the authentic
config/entry/semantic-DATA translation-unit order. `-noopt` candidates
add the documented `#pragma option -O-` **only before `main()`**, leaving
the separate accepted config function unchanged. Every valid candidate
has a natural code/DATA OMF structure; the size below is the actual
`main()` CODE scope after the original 322-byte config function.

| Behavior-preserving source variation | Actual `main()` bytes | Raw acceptance |
| --- | ---: | --- |
| Comma-expression DOS error returns | 260 | Rejected: 9-byte size deficit |
| Comma-expression errors, `-O-` | 265 | Rejected: 4-byte deficit |
| Debug option tested before removal | 259 | Rejected: 10-byte deficit |
| Check both valid options before handling removal | 286 | Rejected: 17-byte excess |
| Explicit valid-option guard, `-O-` | 288 | Rejected: 19-byte excess |
| Local `argv[1]` pointer used by both option tests | 251 | Rejected: 18-byte deficit |
| Shared option-prefix test followed by `switch` | 265 | Rejected: 4-byte deficit |
| Prefix-then-switch, `-O-` | 271 | Rejected: 2-byte excess |
| Guard invalid prefix then test option with `if` | 240 | Rejected: 29-byte deficit |
| Invalid-prefix guard + `if`, `-O-` | 244 | Rejected: 25-byte deficit |
| Guard invalid prefix then `switch` | 267 | Rejected: 2-byte deficit |
| **Invalid-prefix guard + `switch`, `-O-`** | **269** | **Rejected: 252 mismatching byte positions** |
| Single-iteration option decision block | 260 | Rejected: 9-byte deficit |
| Single-iteration option decision, `-O-` | 262 | Rejected: 7-byte deficit |

In particular, the one genuine **269-byte** candidate was fully
assembled and linked against the real pinned C0T CRT, the accepted
source-defined config function and the original foreign symbol binder.
The resulting 5,886-byte COM is the expected native link size and has
a source-generated 269-byte entry, but the byte-for-byte comparison of
the complete original function differs at **252** positions. Equal size
alone is **not** exactness, and this candidate earns **zero** new CODE
or DATA bytes. Every other candidate failed the complete-size gate,
so a second producer/negative control would have been wasteful and
cannot be claimed to exist.

## Original compiler obstacle and retained evidence

The original entry emits separate `dos_puts2()` calls in the `-R`
missing-resident path, invalid-option branch, already-present branch
and no-memory branch. The optimized natural source moves several of
these calls into a common error-label tail and removes nine genuine
instruction bytes. Alternative source control-flow structures change
which tails are shared, but no tested natural structure both preserves
the original 269-byte source layout *and* produces all original bytes.
This is a Turbo C++ optimizer/source-layout problem, not a reason to
borrow exactness from the existing vendor ASM or to insert fake side
effects in the C++ source.

Reproducible private experiment script:
`.analysis/gpt-web-zun-resident-natural-options-20261112.py`.
Each candidate's exact source snapshot, OMF, compiler logs, and actual
measurement is retained under
`.analysis/gpt-web-zun-natural-options-20261112-<variant>/` with
`diagnostic.json`. The linked positive-size candidate also has
`units.com` and `units.map` for independent inspection.

This trial does not modify the accepted source tree or run a full cold
replay. It records a sharper, reproducible constraint for the next
natural source reconstruction attempt. Its failure is not part of
`config/exact_units.zun.toml` or the accepted progress ledger.

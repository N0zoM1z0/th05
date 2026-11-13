# Scroll coordinate: exact original ASM and raw-exact natural C++ alternative

The complete native MAIN helper DF28..DF50 contains 40 instruction bytes,
without tables, padding or MZ fixups. It is near Pascal with one signed WORD
at entry SS:SP+2, an AX result and RET2. BP/SI/DI and segment registers remain
unchanged. Scroll state is the actual byte at DS351A and signed WORD at 3516.

The source follows TH04/TH05 scroll_y_1.asm semantics and the maintained TH04
scroll owner. It arithmetic-shifts the subpixel input by four, conditionally
adds scroll_line and applies one 400-line correction. It neither normalizes
arbitrary coordinates nor adds clipping or guards. Unlike the donor's fixed-AX
algorithm, only the genuine entry-stack word transport is explicit, following
the already accepted frame_delay precedent. A normal C++ integer handles the
arithmetic and return. Canonical aliases are imported unchanged from small.hpp.

The first attempt omitted those aliases and failed compilation. The corrected
source generates 47 complete CODE bytes: the compiler moves the shifted input
to DX and later moves it back to AX, and three immediate operations are one
byte longer in DX. Those seven bytes explain the full size difference. An
ordinary inline scalar-helper form generates 51 and was reverted to 47.

The first 47-byte object initially failed linkage because the compiler's empty
SMALL_MAIN01_CONTEXT SEGDEF had no corresponding location in the binder. The
corrected binder places that actual empty member in MAIN01 before its foreign
tail. Source and object identities were checked, then the binding was assembled
and the existing 47-byte compiler object relinked, with zero new C++ invocations.
It forms a valid MZ and complete MAP contribution at DF28..DF57. Size growth
leaves DATA at 209E rather than native 209D; the raw
gate still fails and no whole-layout equality is claimed.

The restored 47-byte source, larger inline trial and relink-only lineage remain
under `.analysis/native-producers/main-scroll-coordinate-{b,inline-a,relink-b}/`.
Complete evidence is `.analysis/scroll-coordinate-native-source-review.json`.
The private proposal is outside all live manifests. No acceptance receipt,
negative, behavior model, DATA/BSS ownership or authored-byte credit is added.

## 2026-11-13: complete pure-C++ alternative in the original 40-byte extent

The maintained `coordinates.cpp` now keeps the original accumulator in the
real `_AX` DOS pseudoregister. Explicit `short` casts preserve the signed
16-bit meaning of the arithmetic right shift and both one-step wrap tests;
without those casts the pseudoregister's unsigned type changed `SAR` to `SHR`
and removed the negative correction. This is ordinary C++ expressions plus
read-only register intrinsics, with no inline ASM, emitted instructions,
compiler barrier, or target bytes.

Two independent focused Borland/TLINK producers reproduce all **40/40**
original bytes at `[DF28,DF50)`, the original near-Pascal entry/RET2 and empty
ordered relocation stream. The compiled `SCROLL_RING_HEIGHT` 400-to-399
negative is rejected. Receipt:
`.analysis/unit-replays/gpt-web-main-scroll-coordinate-natural-cxx-20261113/receipt.json`.

This is an exact source-language alternative to the independently accepted
40-byte reviewed-ASM owner, not a second ownership claim. The ASM family
remains the sole credited owner; the C++ alternative adds **zero** CODE bytes
to progress and does not change any coverage denominator. Both paths preserve
the actual one-word stack argument, `SS:[BX+2]`, `scroll_active` byte and
signed `scroll_line` word. No unrelated scroll owner or full cold replay ran.

Review SHA-256:
`b4b2c57970ced11c5348e12129e6616219c2999dff939ac491e419e1b1b4992a`.

## Exact original-register scroll converter — 2026-11-10

`coordinates.asm` now reconstructs the complete 40-byte MAIN near-Pascal
`SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1` body at `[DF28, DF50)`. The genuine
ReC98 `th04/main/scroll_y_1.asm` provides a complete original-language
reference for the register and ring semantics. The TH05 disassembly and
independent parameter/storage ABI review confirm the same one-word stack
argument, `BX=SP` and SS:BX+2 retrieval, `SAR AX,4`, optional scrolling
origin and exactly one correction against 400 VRAM lines. No external
DATA, range normalization, padding or 32-bit signed widening is introduced.

The standalone C++ owner above remains 47/40 and unaccepted; it is not
relabelled as compiler-exact. This function is instead reviewed as a real
hand-assembly algorithm. Two independent TASM32/TLINK producers pass **40/40
raw bytes**, original empty ordered relocation list, complete public/MAP/OMF
boundaries and the actual main_01/CS `AE1`, DGROUP/DS `209D`. Its compiled
ring-height control changes 400→401, retains the function extent and is
rejected. The accepted receipt is
`.analysis/gpt-web-main-scroll-coordinate-asm-a/receipt.json`.
This adds **40 reviewed ASM instruction bytes**, not C++ credit, and leaves
the unrelated scroll driver unchanged.

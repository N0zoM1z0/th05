# Scroll coordinate candidate

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

Review SHA-256:
`b4b2c57970ced11c5348e12129e6616219c2999dff939ac491e419e1b1b4992a`.

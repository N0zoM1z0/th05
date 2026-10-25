# EGC interpage rectangle copy

Two complete public procedures share one maintained semantic ASM source. Only
the public 124-byte owners are explicitly adopted; their adjacent private
64-byte setup helpers remain entirely unknown, with no authored credit or
vendor/denominator exclusion.

| Artifact | Complete public range | Actual CS | DS:width word | Foreign near setup | Foreign far EGC_OFF |
| --- | --- | --- | --- | --- | --- |
| OP | E2D8..E354 | 0D30 | 0EFE:3F1E | E354 | 0000:082C |
| MAINE | F402..F47E | 0E80 | 1011:2E86 | F47E | 0000:083A |

Each owner has RETF 8 at relative 120, followed by its sole alignment NOP at
123. The only original ordered MZ fixup is relative 116, the EGC_OFF segment
word. There are no tables, runtime placeholders, inert branches, owned DATA or
assets. No hardware-delay NOP occurs inside either original 188-byte family.
The full native family has its own complete public and private boundaries;
selecting the public procedure does not trim an instruction or hide a mismatch.

## Origin and the unadopted helpers

Candidate algorithms are pinned ReC98 b6ba5b0a,
`th05/egcrect.cpp` selecting `th04/hardware/egcrect.cpp` in GAME5. Its register
templates are not authored C++ recovery. The maintained source instead uses
semantic EGC-write and interpage-copy macros, typed arguments, hardware
constants and symbolic loops. It contains no target-byte array, codegen helper,
copied instruction listing, numeric local CODE address or private helper body.

The public procedure independently exhibits deliberate assembly-level design:
after reading all arguments it repurposes BP as row stride, BX as a signed row
counter, DI as the clipped VRAM offset, CX as word width and DX as the latched
pixel word. Explicit page-1 read/page-0 write operations drive the copy. This
native protocol supports reviewed original ASM without relying on the private
helper's provenance. No inspected public subspan has positive compiler-generated
provenance. Literal historical source, original assembler identity and possible
assembly-heavy mixed C/ASM source remain unproved.

The bounded vendor investigation searched all 653 members of the pinned
master0.23 source archive and found a material positive resemblance: the private
helper's final 34-byte register-setup sequence closely follows upstream
`EGC_START` in EGC.ASM, with the same five-register order and constants, different
AX zeroing and omitted surrounding calls. Its earlier BDA 0000:0495 convention
was not found there. This evidence is insufficient either to credit the whole
helper as original or to exclude it wholesale as vendor code. Therefore both
complete helpers, including their own terminal alignment bytes, remain unknown.
No identifier search or presumed common hardware boilerplate overrides that
decision. This is a bounded search, not exhaustive historical attribution.

## Preserved contracts and edge cases

The public API is far Pascal `(left, top, width, height)`, four word arguments
and RETF 8. It preserves BP/DI; SI/DS/SS are untouched. ES returns as A800;
AX/BX/CX/DX and arithmetic flags are working state. GAME5 does not clear DF.
The foreign setup preserves interrupt state and DF, so no CLD, PUSHF/POPF or
other invented state restoration is added to the public procedure.

Left alignment uses signed SAR BX,4, then doubles the word offset. Width uses
logical SHR AX,4 and the original extra word when left is not word-aligned.
The original rounding and row stride are preserved without adding dimension
guards. The row loop is do-while DEC BX/JNS: height zero copies one row, and
ordinary nonnegative heights copy height+1 rows. Word offset arithmetic wraps
at 16 bits, while negative or beyond-plane DI values skip individual copies.

Page selection changes only for an in-bounds word. If every word is clipped,
the public procedure performs no page-port OUT; it does not unconditionally
select page zero on exit. Each actual copy reads page 1 and writes page 0 at
the same video word. Zero widths and other original loop behavior are not
replaced by clipping or early-return fixes.

The full external width state is one 16-bit word, not a reduced object view.
The unchanged canonical OP menu, MAINE cutscene and shared ABI declarations
are pinned semantic inputs. The source exports the actual compiler alias
`@EGC_COPY_RECT_1_TO_0_16$QIIII`; MAP verification checks its demangled signature
alongside the ordinary entry and complete end labels. The alias adds no bytes
or functions.

The private setup is a genuine near EXTDEF, bound at public+124 with no body
or initialized payload. Its self-relative call retains the source's actual CS;
the symbol-only foreign tail introduces no fictitious SHARED group. The far
EGC_OFF provider and real DGROUP frame are likewise checked. Foreign reserves
use the actual complete width word or independently accepted DATA bound, with
every ORG below 64 KiB and no artificial stack.

## Exact evidence and explicit adoption

`.analysis/egc-rect-native/op-a/receipt.json` and `maine-a/receipt.json` each
contain two fresh independent deterministic TASM producers. Complete ordinary
CODE SEGDEF/LEDATA/MAP coverage, real CS/DGROUP frames and publics, all 124 raw
bytes and literal ordered relocation [116] pass. Each owner's own assembled
400-to-399 visible-row mutation changes the clipping bound and is rejected over
the same complete scope and fixup stream. No setup-helper byte is supplied by
the source or included in the compared public owner. Installed tool execution
proofs and all previous accepted owners are reused after dependency checks.

Independent reports are `.analysis/egc-rect-native-review.json`
(SHA-256 `6634adc44f0d99ff9920988be5a4fccd22626a0f229db4af07bbb748690b9829`)
and `.analysis/egc-rect-maintained-source-review.json`
(SHA-256 `9d5c04d43136479e256f2c88503ac65802b18dc47dbcc9a28e6dd964da070d82`).
Native byte/boundary proofs are pinned in `config/asm_families.toml`;
`accepted_asm_families.json` and `reviewed_asm_families.json` separately record
exact acceptance and explicit per-owner/note adoption. Totals are 248 compared,
246 reviewed ASM instruction bytes and two checked uncredited NOPs. C/C++
counters, the observation universe and the unreviewed global denominator are
unchanged. The 98% objective and whole-program reconstruction remain open.

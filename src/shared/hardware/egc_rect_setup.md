# Exact EGC rectangle-copy setup in OP and MAINE

The private `egc_rect_setup()` directly following the accepted public EGC
rectangle copier is now source-exact in both executables:

| Artifact | Complete helper | Original fixups |
| --- | --- | --- |
| OP | `E354..E393` (63 bytes) | `[]` |
| MAINE | `F47E..F4BD` (63 bytes) | `[]` |

Both implementations use the same maintained Borland C++ source, with
semantic inline assembly for the CPU flags, temporary ES=0 access and GRCG
mode/BDA byte at `0000:0495`. The remaining EGC initialization uses the
actual plane-selection and register ports `6A`, `4A0`, `4A2`, `4A8`, `4AC`,
and `4AE`. It explicitly writes zero with `SUB AX,AX`, matching the hardware
register convention. The assembler emits the native 63-byte near function;
its trailing `EVEN` NOP at OP `E393` / MAINE `F4BD` remains outside the
complete function and receives no credit.

The source follows the hardware setup in pinned ReC98
`th04/hardware/egcrect.cpp`, which retains the original mixed C++/inline-
assembly algorithm. The private function was previously left unowned because
its first part resembles Master library EGC setup code; these proofs show a
natural compiler translation and complete original byte match, not definitive
historical authorship of the hardware idiom. The preceding 124-byte public
rectangle copy and all its existing source and acceptance remain unchanged.

Two focused receipts contain independent real TCC `-S`/TASM32/TLINK builds,
complete byte and ordered relocation checks, OMF/MAP CODE ownership and a
rejected mutation changing the active-plane mask from `FFF0h` to `FFEFh`:

- `.analysis/unit-replays/gpt-web-op-egc-rect-setup-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-egc-rect-setup-a/receipt.json`

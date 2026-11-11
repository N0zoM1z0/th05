# Original GRCG mode and direct-color helpers

MAIN's three contiguous near device helpers at `C1F8..C21E` select GRCG
read-modify-write (`C0h`), tile-direct (`80h`), and convert the color nibble
in AH to four physical tile-plane bytes at port `7Eh`. OP contains the same
complete direct-color routine at `DB21..DB3B`. Each direct-color call
preserves its original `CLI`/`STI` bracket and shifts the nibble through
carry; no new clipping, palette data or device state is introduced.

The symbolic sources follow pinned ReC98
`th04/hardware/grcg_modecol.asm` and the native 16-bit I/O control flow.
The near ABI is register-based, with no compiler stack frame. MAIN's two
natural `EVEN` NOPs at `C1FD` and `C203` are compared but do not earn ASM authored-byte credit. OP's following `DB3B` zero byte and MAIN's preceding `C1F7` NOP are outside the new source scopes and remain uncredited. Each CODE owner
has an independent source-free actual CS/DGROUP binder.

Focused native receipts:

- MAIN `.analysis/asm-replays/gpt-web-main-grcg-mode-direct-b/receipt.json`: 38/38 bytes, two uncredited `EVEN` NOPs, 36 authored instructions; empty fixups
- OP `.analysis/asm-replays/gpt-web-op-grcg-mode-direct-d/receipt.json`: 26/26 bytes, no internal padding, 26 authored instructions; empty fixups

Both receipts contain independent actual TASM32/TLINK producers and a
rejected same-size semantic mutation. OP's foreign-only initialized-DATA
reserve keeps the isolated MZ's original DOS stack range valid without
providing byte values. The original instruction and source-origin reviews
are `.analysis/gpt-web-{main,op}-grcg-mode-direct-review.json`.

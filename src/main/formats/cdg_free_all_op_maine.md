# `cdg_free_all()` in OP and MAINE

OP and MAINE contain the same 14-byte `cdg_free_all()` as MAIN, assembled
from the unchanged `cdg_free_all.asm` (see [cdg_free_all.md](cdg_free_all.md)).
Only the addresses differ:

| Binary | Function | `cdg_free()` | CS / DS |
| --- | --- | --- | --- |
| OP | `E2CA..E2D8` | `E294` | `D30` / `EFE` |
| MAINE | `F3F4..F402` | `F3BE` | `E80` / `1011` |

The OP link scaffold also declares the CDG slot array at DS `3A96` as
uninitialized data. Without it, the linked test executable was too small
for its own `SS:SP` and failed MZ validation.

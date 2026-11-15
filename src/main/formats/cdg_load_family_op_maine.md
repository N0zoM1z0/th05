# CDG loaders in OP and MAINE

OP and MAINE contain the same 342-byte CDG loader family as MAIN, assembled
from the unchanged `cdg_load_family.asm` (see
[cdg_load_family.md](cdg_load_family.md)). Only the addresses differ:

| Binary | Code | CS / DS | `cdg_noalpha` | `cdg_slots` | `cdg_images_to_load` |
| --- | --- | --- | --- | --- | --- |
| OP | `E174..E2CA` | `D30` / `EFE` | `AB4` | `3A96` | `3E96` |
| MAINE | `F29E..F3F4` | `E80` / `1011` | `72E` | `29FE` | `2DFE` |

Each binary has 14 far relocations in this range and the same five NOPs.

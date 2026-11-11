# OP and MAINE far-Pascal CDG bank release

The unchanged source-backed `src/main/formats/cdg_free_all.asm` also
reconstructs the complete original `CDG_FREE_ALL` code in OP and MAINE,
with authentic 64-slot bank count, saved SI, descending slot iteration,
genuine same-CS near `CDG_FREE` call and original FAR return. Each is a
separate real source-owner of exactly 14 bytes with no NOPs, tables or
MZ relocation. Both use original SHARED code, separate master library
and DGROUP frames. The source does not supply any CDG resource data,
foreign CDG_FREE implementation or invented code padding.

## 2026-11-11: exact original 14-byte source adoption

| Artifact | Complete native bounds | Native provider in SHARED | CS / DS |
| --- | --- | --- | --- |
| OP | `E2CA..E2D8` | `CDG_FREE` at `E294` | `D30` / `EFE` |
| MAINE | `F3F4..F402` | `CDG_FREE` at `F3BE` | `E80` / `1011` |

Both producer pairs assemble the unchanged source-backed `cdg_free_all.asm`
and link into their own original SHARED code groups. The function has exactly
nine original instructions: saved SI, 64→0 descending slot walk, Pascal
stack argument, real same-CS `PUSH CS`/near `CDG_FREE` call, and FAR return.
Each 14-byte function has **no original relocations, CODE tables or NOPs**.
Two independent actual TASM32/TLINK producers match all **14/14 original
bytes** and exact MAP/public bounds in each executable. Separate compiled
negatives change original 64 slots to 63; both fail raw comparison. Neither
foreign helper implementation nor any game-state DATA is source-owned.

The first OP diagnostic produced a small isolated MZ load image ending at
`E2D8` and was rejected by the strict verifier because DOS minimum allocation
plus load image failed to cover the `SS:SP` requirement. The corrected
source-free OP binder anchors the *actual* original CDG bank at DS:`3A96`
as foreign uninitialized DATA. This adds no source bytes, code or initialized
values, preserves the physical original CS/DS and makes the independent
executable MZ valid. The MAINE binder was valid without that extension.
No validation was relaxed, no target bytes were patched and no relocation
stream was normalized.

Strict focused receipts:
`.analysis/gpt-web-op-cdg-free-all-14-b/receipt.json` and
`.analysis/gpt-web-maine-cdg-free-all-14-a/receipt.json`.
The previous 342-byte CDG loader family is also independently accepted in
MAIN/OP/MAINE, so the contiguous 356-byte loader+free sequence has verified
separate complete source owners in each game executable. Only **28 new
reviewed instruction bytes** are credited here, not duplicate loader
or MAIN CDG_FREE_ALL credit.

# OP and MAINE complete CDG loader source recovery

The same maintained `src/main/formats/cdg_load_family.asm` reconstructs
identical original CDG single/batch/alpha/memory-release resource semantics in
OP and MAINE as already reviewed in MAIN. This source is backed by the pinned
ReC98 `th04/formats/cdg_load.asm`; the original code retains 16-byte CDG
records, 64 slots, independent 16-bit file and HMEM providers and five
original NOP or alignment positions. Each executable has an independent
physical SHARED code frame, master file/HMEM call offsets and DGROUP state
addresses. None of those addresses are inferred from a different binary.

## 2026-11-11: two independently accepted full-family replays

| Artifact | Native complete CODE scope | CS / DS frames | Original ordered far relocations |
| --- | --- | --- | --- |
| OP | `E174..E2CA` (342) | `D30` / `EFE` | 14, all original |
| MAINE | `F29E..F3F4` (342) | `E80` / `1011` | 14, all original |

Both source-free binders resolve the correct master functions and mutable
CDG records, including separate original OP and MAINE state addresses:
OP `cdg_noalpha=AB4`, `cdg_slots=3A96`, `cdg_images_to_load=3E96`;
MAINE `cdg_noalpha=72E`, `cdg_slots=29FE`,
`cdg_images_to_load=2DFE`. All file and HMEM callbacks resolve to genuine
artifact-specific FAR providers, and both binders preserve the true ungrouped
SHARED code frame and original data frame. The following CDG_FREE_ALL routine
remains external and independently owned. The source never emits foreign
resource data, code, arbitrary bytes or altered record storage.

The pinned native reviews independently decode each original 342-byte scope,
including real single/noalpha/batch entrypoints, internal near reader, CDG
single-slot cleanup, all 14 ordered far-call sites, and the five original
NOP/EVEN positions `[5,15,101,195,341]`. Two fresh TASM32/TLINK producers
per artifact match **342/342 raw bytes**, original literal ordered MZ
relocations, public entry/exit offsets and complete source LEDATA. For each
artifact, a compiled mutation changes the original three-DWORD metadata copy
to two DWORDs; both negatives are rejected. No fixups are reordered or
normalized, and there is no target-byte insertion.

OP receipt: `.analysis/gpt-web-op-cdg-load-family-342-a/receipt.json`.
MAINE receipt: `.analysis/gpt-web-maine-cdg-load-family-342-a/receipt.json`.
Only **337 instruction bytes per artifact** are credited. The five NOPs
participate in all checks but carry zero authorship credit; the existing
337-byte MAIN owner is not counted again. Across MAIN/OP/MAINE, this one
maintained semantic source reconstructs **1,011 independently reviewed
instruction bytes**, without claiming historical handwritten authorship.

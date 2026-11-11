# Alice and Yumeko backdrop color-fill callbacks

MAIN `[C41E,C43A)` contains the two complete near original-register
callbacks `alice_backdrop_colorfill()` (14 bytes) and
`yumeko_backdrop_colorfill()` (14 bytes). Both preserve DI, set ES to the
actual PC-98 GRAM window and DI to the last background row, then invoke the
separately accepted `grcg_fill_playfield_rows` near worker at MAIN `10600`.
Alice starts in window `A850` at offset `3FC4`; Yumeko uses `AC10:36B4`.
Neither callback has local DATA, BSS, padding, switch tables or MZ fixups.

The source follows the original register/ES:DI raster algorithm in pinned
ReC98 `th05_main.asm`, using named video geometry instead of target bytes.
The near worker's preserved register interface and explicit `PUSH DI`/
`POP DI` source control provide the separately reviewed original-ASM
classification. The analogous separately accepted Sara, Mai/Yuki and Shinki
color-fill families are independent owners, not an excuse to duplicate their
CODE. Literal historical source spelling and whole-executable linkage are
not established by the family match.

## Focused native acceptance

`.analysis/asm-replays/gpt-web-main-boss-backdrop-ay-a/receipt.json`
records two independent TASM32/TLINK producers, complete 28-byte raw
identity, exact MAP/OMF and an empty ordered MZ relocation list. The negative
changes Alice's last-row VRAM offset by one and is assembled and rejected.
Native instruction and function-boundary evidence is preserved in
`.analysis/gpt-web-boss-backdrop-ay-native-review.json`.
Explicit original-register ASM adoption credits all **28 instruction bytes**,
with no NOP or table-credit adjustment.

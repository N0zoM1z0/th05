# OP character-effects overlay nibble masks

TH05's OP load module stores the complete 32-byte character-overlay
coverage bank at decoded `[0F99E,0F9BE)`, DS `0EFE:09BE`. This is the
same **semantic four-phase nibble mask progression** separately present
in MAINE, but it is a distinct physical C DATA contribution in another
binary. Each of the four stages holds four original 16-bit scanline masks
formed from repeating the source-level pixel nibbles 8/0/2/0,
8/4/2/1, A/4/A/1 and A/5/A/5. The original `grppsafx` glyph effect
renderer selects these stages through its real separate pointer table.
They are not an image, font pixel payload, compiler switch table or
stored instruction stream.

The OP owner is `src/op/hardware/glyph_coverage_data.c`, which includes
the same source-level nibble construction header used by the separately
accepted MAINE owner. That header contains no runtime storage, and the OP
module compiles an independent local `GLYPH_OVERLAY_MASKS[4][4]` array.
Its symbol-only binder preserves the true OP code/group frames `0A390`,
`0D300`, DATA `0EFE:09BE` and provides no candidate DATA bytes.

The first native attempt built the correct 32-byte MAP/LEDATA but its
*truncated scaffold* failed the MZ initial SS:SP minimum-allocation
check. The revised binder reserves the actual accepted foreign OP DATA
suffix to DS `2817` entirely **after** the complete C contribution,
matching the established OP sound-priority scaffold. This is outside-only
linkage context; it contributes no authored glyph bytes or fake stack.
The fresh scoped receipt
`.analysis/unit-replays/gpt-web-op-glyph-coverage-b/receipt.json`
passes two independent original-size Borland C compiles, full 32-byte
raw/OMF/MAP equality, empty original ordered fixups, and a compiled
semantic negative changing nibble `5` to `4` that is rejected.
No unrelated OP or MAINE unit was cold replayed.

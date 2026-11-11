# Original Master BFNT entry: 322 complete MAIN CODE bytes

Two formerly unknown complete functions from the authentic Master 0.23
`BFTENTRY.ASM` author source now relink to the original TH05 MAIN CODE:

| Complete original function | Original load interval | Raw CODE | Actual OMF fixups |
| --- | --- | ---: | ---: |
| `BFTENTRY_INVAL` (author's `INVAL`) | `0272..0286` | 20 | 1 |
| `BFNT_ENTRY_PAT` | `0286..03B4` | 302 | 10 |

The maintained native TASM input `libs/master.lib/bfnt_entry_pat.asm` is a
source-derived GAME=5 adaptation, *not* the untouched original archive file.
The error helper renames its `INVAL` / `FAULT` local labels. The complete font
entry function renames two short fault branches and expands two original
conditional branches beyond their short displacement range: `JC INVAL` becomes
`JNB next_pattern_1; JMP BFTENTRY_INVAL`, and `JNE INVAL` becomes
`JZ next_pattern_2; JMP BFTENTRY_INVAL`. The source retains an explicit
`IF LDATA` arm for the first expansion. After exactly these changes, both
complete original author ASM procedure bodies match the actual frozen TASM
source line-for-line under strictly limited whitespace/local-label
normalization. No additional instruction, register operand, implicit branch,
DATA initializer or source slice is tolerated.

Both real complete CODE contributions were read from the authentic saved
Master TASM OMF with all **11 genuine fixup actions** and full ordinary
LEDATA coverage. The original and calibration MZ scopes agree for every
byte, with identical original ordered segment relocations. Both functions
are uniquely located in the original MAIN image at their genuine source
listing boundaries. The initial `0000..0272` remains unknown; this review
does not adopt the entire startup prefix or any neighboring unrelated data.

Proof: [`main_bfnt_entry_ownership.json`](../../config/main_bfnt_entry_ownership.json).
Separate explicit adoption:
[`reviewed_main_bfnt_entry.json`](../../config/reviewed_main_bfnt_entry.json).
Actual native evidence is verified with `python3 scripts/review_main_bfnt_entry.py
--check`; public CI uses its structural check only. All **322 bytes are
third-party Master code**, with zero credited game C++ or authored ASM.
No full executable or full cold replay was attempted.

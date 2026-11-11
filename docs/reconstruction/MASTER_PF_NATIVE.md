# Original MAIN PF archive interception

The TH05-specific Master 0.23-derived TASM sources reconstruct **805
previously unknown CODE bytes** around the large DOS INT 21h file hook.

| Original scope | Source-written bytes | Real OMF FIXUPP |
| --- | ---: | ---: |
| `PFSTART` `4288..4328` | 160 | 10 |
| `PFEND` `4328..4360` | 56 | 8 |
| `pfint21` `4360..43C4` | 100 | 18 |
| `pfint21` `43C6..44BF` | 249 | 16 |
| `PFOPEN` `44C0..45B0` | 240 | 4 |

All these complete **source-written intervals** reproduce the original
and calibrated MAIN bytes via the pinned TASM OMF and ordered fixups.
The first part of `pfint21` has the original ordered MZ relocation
at offset +19. `PFSTART`, `PFEND` and `PFOPEN` are complete function
extents; the full `pfint21` procedure spans `4360..44BF`.

The two excluded bytes `43C4..43C6` are the original source's
`default dw ?, _Thru` dispatch-table entry: they are intentionally
not present in CODE LEDATA and are written at runtime. The separate
`44BF` assembler alignment byte also remains unknown. The review
does not claim either as source-written instructions.

The compiler input is the TH05 `GAME=5` adaptation of the original
Master `PFINT21.ASM` and `PFOPEN.ASM` procedures, not the literal
unmodified Master 0.23 source. The source and original archive identities
are recorded alongside the actual assembled object and both linked
targets. See [scoped verifier](../../scripts/review_master_pf.py),
[evidence](../../config/master_pf_ownership.json) and
[ownership decision](../../config/reviewed_master_pf.json).

```sh
python3 scripts/review_master_pf.py --check
python3 scripts/ownership.py --check
```

These are Master-derived assembly CODE bytes, not new game-authored C++.

# Original Master SUPERPA pattern storage: 6,144 verified unwritten bytes

Each of the three TH05 executables preserves two complete, contiguous
1,024-byte Master 0.23 sprite-pattern arrays: `super_patdata[512]` and
`super_patsize[512]`. The archived author `SUPERPA.ASM` and `SUPER.INC`
explicitly define both as `DW MAXPAT dup (?)` in `.DATA?`, with `MAXPAT=512`.
The retained ReC98 `superpa[bss].asm` source has the same two declarations,
compiled to `_BSS` (class `BSS`), not initialized DATA.

| Original EXE | `super_patdata` 1,024 B | `super_patsize` 1,024 B |
| --- | --- | --- |
| MAIN | `2305C..2345C` | `2345C..2385C` |
| OP | `11E40..12240` | `12240..12640` |
| MAINE | `11EEC..122EC` | `122EC..126EC` |

The original MAPs identify `super_patdata`/`_super_patdata` and
`super_patsize`/`_super_patsize` at the corresponding genuine DGROUP offsets.
The complete native TASM object contains one actual `_BSS` segment per
program; the exact local PUBDEF offsets of both arrays were verified against
its SEGDEF size and there are **zero initialized LEDATA/LIDATA records in
that segment**. The linked calibration MZ images correctly end before the
BSS arrays, whereas all three original decoded target views materialize the
full two arrays as zero bytes without loader fixups.

Run `python3 scripts/review_master_superpa_reservations.py --check` for the
archived author, native TASM object, source, MAP, BSS and original-image
proof. The evidence is in `config/reviewed_master_superpa_reservations.json`.
The narrowly validated `reviewed-uninitialized-vendor-storage` inventory
accounts for exactly **6,144 previously unknown bytes**, with **zero
source-authored initialized DATA, CODE, instruction or compiler credit**.
No broader tail BSS, neighboring data or unrelated zeros are adopted. The
separate initialized `super_buffer`, `super_patnum` and `super_charfree`
remain owned by their earlier six-byte-per-program source proof.

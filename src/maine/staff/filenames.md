This accepted initialized-DATA reconstruction owns the complete contiguous
staff filename bank `[0x11862, 0x118EA)`, DS:1752..17DA: one six-byte BGM
basename and thirteen ten-byte CDG/BFNT filenames, including their NULs.
All 136 bytes belong to fourteen complete readable ASCII objects. There are
no gaps, padding, or MZ relocations. The source owns filenames only, not any
music, image, or font resource contents.

The original staff controller pushes each filename as a complete DS:offset
far argument. `staff` goes to `snd_load` at E80:0566 with song operation
0600h; `stf00.cdg` through `stf10.cdg` go to `cdg_load_all_noalpha` at
E80:0B5C with slots 0 through 10; `stf01.bft` and `stf00.bft` go to
`super_entry_bfnt` at 0000:2894. All fourteen references identify the exact
NUL object starts. The new header repeats the full existing mutable array
declarations from `controller.hpp` without changing that header or its users.
The historical original C declaration/TU is not claimed.

Pinned ReC98 revision `b6ba5b0a529edbb31efdf8c0e939263804f8ee47`,
`th05_maine.asm` lines 6105..6118, corroborates all fourteen literals as
disassembly evidence. Immediately before the bank is the complete second
image-phase cover string; immediately after it is the C runtime's separate
`Abnormal program termination` diagnostic. Neither neighbor is owned. The
other pending verdict DATA owner ends at load1184A, before this bank. Native
review finds no accepted overlap and the entire proposed range is unknown
in the ownership snapshot.

Each array extent follows directly from its readable literal plus the NUL;
no zero filler or alignment option is supplied. The binder gives only the
real outside DATA frame and prefix. The meaningful negative changes the BGM
basename `staff` to `stafg`. The `maine-staff-filenames-data-a` replay passes two independent fresh
producers, complete136-byte compiler DATA coverage, full raw comparison,
original empty relocation streams and the own compiled filename negative.
The ledger credits136 initialized semantic DATA bytes, separately from the
source-present controller whose ordered fixups remain unaccepted. Native evidence and the proposal are retained under
`.analysis/staff-filenames-*`.

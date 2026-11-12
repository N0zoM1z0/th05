# MAINE All Cast PI background filename bank

The original decoded MAINE interval `[109FE,10B16)` contains **28 independent,
10-byte ASCII filename arrays**, organized into four seven-slide background
programs. Their literal names range across `EXED01.pi` through `EXED16.pi`;
several names repeat at different physical addresses by design. The source's
mutable `char allcast_background_filenames[4][7][10]` preserves all those
separate allocations rather than allowing the Borland compiler to merge
identical constant string objects. Each string is nine printed bytes plus
its natural NUL terminator. These are filenames, not decoded PI artwork.

The original source listing `_reference/ReC98/th05_maine.asm` supplies
all 28 individual `aExed*.pi` declarations and the preceding `_BG_FN`
index of four eight-entry far-pointer rows: seven filenames followed by
a genuine null pointer in each row. This packet owns only the **280
filename bytes**, without retroactively claiming that preceding pointer
table, the four unknown preceding zero bytes at `109FA..109FE`, or the
already accepted All Cast text starting at `10B16`.

The actual MAINE frame is group_01 `A540`, shared `E800`, and DATA
`10110:08EE`. The outside-only binder provides no initialized values,
CODE, BSS, target-derived payload or relocations. The native receipt
`.analysis/unit-replays/gpt-web-maine-allcast-background-files-a/receipt.json`
passes two independent Borland C producers with the complete 280-byte
DATA SEGDEF/LEDATA, correct MAP position, all raw bytes and the empty
ordered relocation sequence. Replacing the third filename in the first
program with another valid PI name is a real compiled negative that is
rejected. No unrelated All Cast units were replayed.

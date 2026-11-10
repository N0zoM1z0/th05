# Exact MAIN scroll tile-ring state machine

The real `scroll_tile_ring_update()` is a complete **204-byte** source-owned
C++ hardware-register callback at `[C43A,C506)`. Its original control flow
is independently decoded in ReC98 `th05_main.asm` (`sub_BD20`) with actual
STD/tile record semantics corroborated by preserved TH04/TH05 source. It is
not an opcode transcript: the maintained `ring_update.cpp` expresses the
state machine and 24-word map copy in C++, with only genuine 16-bit register,
flag and segment-copy instructions in Turbo C++ inline ASM.

The function checks both current and previous scrolling advances and the
STD scroll speed, then compares the tile row (`scroll_line / 16`) to its last
source row at DS3512. A changed row decrements the signed row-in-section
counter at DS575C, wrapping it to four and incrementing the genuine STD
map-section pointer DS575A and speed-table pointer DS575E when needed.
The speed byte comes from the actual foreign STD segment; zero terminates the
scroll and clears both advances. For live rows, the source tile section index
is a **byte offset into the WORD table** at DS0F0A, not a C++ array index:
its WORD value and the tile-row offset select 24 words in the foreign MAP
segment. The real DS→ES `REP MOVSW` fills the tile-ring row at DS511A.

After the optional tile fetch the function transfers the old and new advance
bytes, then uses the real stage-5/scroll-active gating before calling the
foreign EGC setup and existing 182-byte strip copy. The far EGC shutdown is
the original `0000:085E` call at relative +198; no segment, data, sprite or
map-file content belongs to this unit. The two other helpers and all mutable
state remain external.

A first complete C++ producer generated 210 bytes: it expanded the signed
row-counter decrement to five instructions, shifted the map-section offset
by a word index, and reversed the two STD pointer labels in the binder.
Restoring the **real** pointer ownership, `DEC`/`JNS` flag dependence, raw
byte-offset table access and actual register transfer directions caused
Borland to produce **204/204 raw bytes** and the original ordered far fixup.
No semantic guard, artificial state mutation, byte list, NOP or post-link
relocation rewriting was added.

The final source-free `scroll_ring_update_bindings.asm` uses the tested
**before/after compiler** linkage: only real main_01 predecessors are bound
before the compiler object, while the original foreign MAIN01 tail, ungrouped
SHARED frame, MAIN03 body and DGROUP are placed afterward. Its MAP proves
`CS=0AE1`, `SHARED=14AB`, `MAIN03=1527`, `DS=209D`, matching the game.
A standalone first-binder attempt incorrectly grouped the foreign MAIN03
range into main_01 and overflowed the 64-KiB group; that failure is preserved
as diagnostic evidence, not hidden or credited.

**Acceptance:**
`.analysis/unit-replays/gpt-web-main-scroll-tile-ring-204-20261111/receipt.json`
contains two independently linked Turbo C++ producers, exact complete raw
bytes and literal ordered fixup `[198]`. Its compiled negative changes the
real row-in-section wrap from four to three and is rejected. All 204 bytes
are original authored code; no padding or compiler table exists in this
function. This is C++ with a few authentic hardware-register primitives,
not claimed as pure high-level C++.

The following accepted `scroll_driver()` `[C506,C579)` is an independent
115-byte C++ owner. Together they restore 319 contiguous bytes of the entire
TH05 scrolling state machine, without duplicate credit or cold replay of
unrelated functions.

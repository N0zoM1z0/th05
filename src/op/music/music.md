TH05 Music Room candidate
=========================

Current preparation uses the single canonical frontend described in
[full_context.md](full_context.md). The split-producer boundaries and results
below record the previous accepted source context; the new source has not yet
run its focused replacement replay. Its intrinsic DS-copy helper remains
entirely unaccepted.

Natural-source provenance is nmlgc/ReC98 at
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`: `th05/op_music.cpp`
selects `th02/op/m_music.cpp`, with `GAME=5` and `BINARY='O'`.
The owner selects those branches, keeps the real natural algorithms, and uses
canonical resident, menu, and geometry definitions without changing them.
`titles.hpp` preserves the readable Japanese text and significant spacing of
`th05/shiftjis/music.hpp` and the TH02 through TH05 song-title definitions.
Canonical source is UTF-8; this producer requires explicit CP932 staging.

The source intentionally excludes `nopoly_B_put()`. Its GAME5 branch actively
pushes DS, switches DS to the saved-plane segment, invokes `__memcpy__`, and
restores DS. It is not a branch compiled out for TH05. The original complete
30-byte near-cdecl function at load offsets `[0xBFF6,0xC014)` remains foreign,
with symbol `@nopoly_B_put$qv` at real frame `0xA39:0x1C66`. The candidate has
only its declaration and real call sites, with no replacement body, emitted
instructions, register-code transcription, or authored credit for that gap.
This also leaves standalone executable reconstruction open.

Original decoded OP boundaries, independently checked through the terminal
return of each function, are:

| Function | Load start | Size | Source-owned segment |
|---|---:|---:|---|
| track_unput_or_put | BE79 | 212 | OP_MUSIC_PREFIX_TEXT |
| tracklist_put | BF4D | 106 | OP_MUSIC_PREFIX_TEXT |
| nopoly_B_snap | BFB7 | 49 | OP_MUSIC_PREFIX_TEXT |
| nopoly_B_free | BFE8 | 14 | OP_MUSIC_PREFIX_TEXT |
| nopoly_B_put | BFF6 | 30 | foreign, uncredited |
| polygon_build | C014 | 137 | OP_MUSIC_SUFFIX_TEXT |
| polygons_update_and_render | C09D | 502 | OP_MUSIC_SUFFIX_TEXT |
| music_update_render_and_flip | C293 | 60 | OP_MUSIC_SUFFIX_TEXT |
| cmt_load | C2CF | 94 | OP_MUSIC_SUFFIX_TEXT |
| cmt_put | C32D | 73 | OP_MUSIC_SUFFIX_TEXT |
| cmt_fadein_both_animate | C376 | 49 | OP_MUSIC_SUFFIX_TEXT |
| cmt_unput_both_animate | C3A7 | 82 | OP_MUSIC_SUFFIX_TEXT |
| cmt_load_unput_and_put_both_animate | C3F9 | 72 | OP_MUSIC_SUFFIX_TEXT |
| tracklist_unput_and_put_both_animate | C441 | 79 | OP_MUSIC_SUFFIX_TEXT |
| musicroom_menu | C490 | 837 | OP_MUSIC_SUFFIX_TEXT |

The two complete owned extents are `[0xBE79,0xBFF6)` (381 bytes, four
functions, 12 original segment relocations) and `[0xC014,0xC7D5)` (1985 bytes,
ten functions, 62 relocations). They share the actual `op_01` frame at load
`0xA390`. All 2366 owned bytes decode as instructions; there are no semantic
switch tables or alignment bytes in these extents. Direct branch destinations
were checked against original instruction boundaries. Cached baseline byte
equality is routing evidence only. This packet performs no reconstruction
build or acceptance.

`music.hpp` retains the real four-byte screen point, two-byte changing-space
union, four-byte polygon point, 16-byte planar pointer structure, 40-byte
comment line, byte color and page types, and two-byte `__seg*` allocation
handle. The saved plane is a segment handle rather than a four-byte far
pointer. Polygon arrays keep all 16 slots even though only 14 are rendered;
the point scratch array has ten entries. The comment block is ten 40-byte
lines. File functions, master.lib graphics, and polar use far-Pascal ABIs;
piano functions use far-cdecl. The original near helper and all own near
functions retain the shared original near frame.

One producer owns initialized DATA at DS `[0x0FCE,0x2817)`, 6217 bytes and
227 original segment relocations: eight label pointers, `MUSIC_CHOICES[5][30]`,
`MUSIC_FILES[5][30]`, a word game selector, five word track counts, a byte
initialization flag, and the readable string pool. Full matrix bounds and the
81 implicit null-pointer entries are meaningful aggregate initialization.
Every one of the 227 non-null pointer entries was checked against its readable
source text at the original pointer destination. This is semantic/data
observation, not a producer raw-exact claim or code credit. `TRACK_COUNT`
retains its actual internal C++ const linkage.

The same producer owns 732 bytes of BSS at DS `[0x4D84,0x5060)`, including
the genuine unused 104-byte array, full polygon state, selection state,
saved-plane handle, unused planar background pointer structure, comment
buffer, and three word track counters. There is no invented padding.
These logical BSS addresses are beyond the stored decoded payload; referenced
state is anchored by original operands, while the identity/order of the
unreferenced objects is a natural-source and calibration-layout inference.
No stored BSS-byte comparison is claimed. A context must not add `.stack` or
duplicate this producer's DATA/BSS.

Private integration packet: `.analysis/op-music-boundary-review.json` and
`.analysis/op_music_bindings.asm`. The latter contains only external labels,
original address extents, and group context. It orders prefix, the foreign
30-byte helper slot, and suffix as separate real CODE contributions in
`op_01`; it supplies no helper body. Compare the two owned source segments
separately, while checking their common producer's DATA/BSS once. Use the
accepted GAME5 OP large-model compiler flags, without the GAME2 `-2` override.
The source controls first declarations and segment switches itself.
Only the initial owner option pragma precedes all includes. Later selectors
use `#pragma codeseg SEG op_01`, since TCC rejects late `-zC`/`-zP` option
pragmas. The header first declares `musicroom_menu` under the explicit suffix
selector before including the canonical menu header, so its near declaration
does not capture a distinct default segment with an identical name. Prefix,
foreign-helper, and suffix prototypes each use their explicit selector; the
header restores the default selector at its end. No accepted header is edited.

Natural negative controls are the prefix's background rectangle width
`bgimage_put_rect_16(0, (CURSOR_TOP + top), 320, GLYPH_H)` changed from 320
to 304, or the suffix's held-input threshold
`frame_since_last_input >= 24` changed to 25. Neither changes an ABI or layout.

`music.pi`, `music.dat`, `_MUSIC0.TXT`, the game archive, and song/script
contents remain external resources; only their meaningful names occur in
source. Two fresh focused builds, complete raw-byte comparisons, ordered
fixup agreement, and normal oracle controls are still required before either
owned extent can be accepted.

## Focused replay results

`op-music-prefix-b` accepts the complete 381-byte prefix / four functions,
including both cold producers, all 12 ordered fixups and the compiled rectangle
mutation. `op-music-suffix-b` retains a failed aggregate and a passing compiled
input-threshold negative; its complete function scopes need separate review.
The foreign helper receives no source credit.

`op-music-functions-a` subsequently accepts eight whole suffix functions /
646 bytes with both fresh producers and a new compiled comment-loader control
(`sizeof(cmt)` to `sizeof(cmt)-1`). The previous menu negative affected an
unaccepted function, so it was not reused to claim these scopes. Both the
502-byte polygon update and 837-byte music menu remain unaccepted: their raw
code matches, but original ordered fixups differ. All MAP ends include the
actual immediate neighbor, even when it is one of those excluded functions.

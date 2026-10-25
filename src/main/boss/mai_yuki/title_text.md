# Mai/Yuki survivor titles and filenames

The proposed complete DATA owner occupies original MAIN `[222E6,22334)`,
78 bytes, or DS `209D:1916..1964`. It contains four complete readable objects:
Yuki's `_DM09.TX2` dialog filename and 30-byte BGM title, followed by Mai's
`_DM08.TX2` filename and 28-byte BGM title. Natural NUL terminators are included.
No music, script, font, image or glyph-index content is reproduced.

The canonical existing external names and types from the frozen shared-update
header are preserved: const character filename arrays and mutable unsigned
Shift-JIS-byte title arrays. The new header is independent and edits no
accepted declaration. Source stays readable UTF-8; explicit CP932 compiler
staging must preserve the actual consumed byte identities.

Native original instructions independently pin all four starts. At `1833F`
and `18368`, the shared callback pushes DS offsets `1916` and `193E` for the
two dialog filenames. At `1834B` and `18374`, it stores the title offsets
`1920` and `1948` into the actual far BGM-title pointer's offset word at
DS `4AD0`; the accompanying segment stores retain DS. That callback's natural
C++ itself remains unaccepted. Its failed producer grants no CODE acceptance
or DATA credit; this proof reads the original instruction operands directly.

All four complete objects are contiguous, with zero padding and zero original
MZ relocations. The binder supplies only actual MAIN code-frame context and a
DATA prefix ending at `1916`. The source must emit all 78 bytes as one complete
compiler `_DATA` contribution. It defines no CODE, BSS, pointer table or stack.

The own negative changes the readable Mai title from `裏切りの少女` to
`裏切りの魔女`, preserving CP932 encoded length. Actual complete gapless OMF
LEDATA, MAP extent, two fresh raw-exact producers, original ordered fixups,
inputs/tools/dependencies and this compiled DATA mutation remain required.
The `main-mai-yuki-title-text-a` replay retained two identical complete
78-byte producers and its compiled own negative, but raw comparison failed.
The actual compiler placed mutable Yuki/Mai titles first at offsets 0/30,
then const Yuki/Mai filenames at 58/68. All four individual CP932 payloads
are correct; the category reordering differs from the original alternating
layout. Both empty original/candidate relocation streams agree. Actual
staged input and mutation identities were independently verified. This
candidate remains unaccepted; its failed receipt is preserved unchanged.

Private `.analysis/mai-yuki-title-text-boundary-review.json` pins text,
boundaries, original use-site instruction bytes and source hashes; the adjacent
unit-proposal JSON gives the independent initialized-DATA entry and control.
Run `python3 .analysis/mai-yuki-title-text-review.py` to repeat its bounded
native checks without executing a compiler or game.

The superseded standalone C++ source/header and its unused binder were moved
verbatim to private `.analysis/failed-semantic-banks/files/`, with original
paths, sizes and hashes in that directory's parent manifest. All actual
producer snapshots remain unchanged. Native replay reads the consumed
canonical snapshots, rather than requiring removed live draft files. The
accepted replacement is the C semantic model documented in `title_bank.md`.

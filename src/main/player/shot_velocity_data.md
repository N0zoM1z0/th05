# Fixed-speed shot velocity DATA

The complete accepted table occupies original MAIN `[21942,21D42)`, 1,024
bytes, at DS `209D:0F72..1372`. It holds 256 full velocity points, one per
unsigned eight-bit angle. Each point is two signed 16-bit Q12.4 subpixel
coordinates, X then Y. The C representation asserts the two-byte integer,
four-byte complete point, both field offsets and total table size. No
accepted consumer header or helper prototype is changed.

All 512 original components independently match this mathematical definition:

```text
q8sin(a) = nearest_integer(256 * sin(2*pi*a/256))
q8cos(a) = q8sin((a + 64) mod 256)
velocity(a) = (floor(192*q8cos(a)/256), floor(192*q8sin(a)/256))
```

The speed is twelve pixels per frame in the game's sixteen-subpixels-per-pixel
units. Negative components use floor division: angle 65 has X = -5, rather
than truncating toward zero to -4. The maintained C initializer explicitly
implements this signed floor with 32-bit long arithmetic, avoiding a 16-bit
multiply overflow or an implementation-defined negative right shift.

`scripts/generate_shot_velocity_table.py` uses an 80-digit Decimal sine series,
fixed pi, explicit nearest rounding and exact cardinal directions. It reads
no target, game, reference file or asset. The generated include contains
dimensionless Q8 cosine/sine arguments; the maintained C macro specializes
them to the game's speed. It is not a copied array of target bytes or target
velocity literals. `--check` compares the generated text without writing.
The declared `generated_sources` closure includes the actual generator and
requires the output to be a genuine compiler-consumed include, with bounded
frozen freshness checks and input identities during replay/import.

Independent primary provenance is the author's cached
[Master 0.23 source archive](https://www.koizuka.jp/~koizuka/master.lib/MTSRC023.LZH).
Its pinned stored `SIN8.ASM` member names A. Koizuka, explicitly states public
domain for that file, and defines Q8 sine/cosine semantics. All 320 primary
table values agree with the independent mathematical generator. This is not
a blanket license assertion for the archive. The original vendor sine table
remains separate and receives no authored credit from this game-specific
192-subpixel specialization.

The primary `ROTTBL.ASM` is a different 1,024-byte `.CODE` table for spreading
four-bit VRAM pixel bits. Its entries begin `0, 1, 100h, 101h`; it represents
neither angles nor velocities. This packet neither reproduces nor claims
that vendor table. No pixel bitmap, glyph bitmap or opaque asset initializer
is involved in the velocity table.

The actual original consumer at `E3C4..E3E2` zero-extends its angle byte,
multiplies the index by four and loads a whole dword from DS `0F72` at `E3D6`.
It stores that packed X/Y velocity through the real near pointer, also stores
the shot angle at velocity-relative offset seven, and returns through RET4.
Accepted Reimu, Mima and Yuuka source calls use this genuine setter. These
observations prove the complete table's access role and layout; no consumer
CODE is accepted by this DATA unit.

The maintained C model is a full typed point array, not a claim about the
historical source language or generator. Its outside-only binder supplies the
authentic MAIN frame layout and DATA prefix ending at `0F72`. No CODE, BSS,
internal hole, padding or compensating work is emitted. Original ordered MZ
fixups are empty, and every one of the 1,024 bytes must compare normally.

The focused `main-shot-velocity-data-a` replay passes two fresh actual C
compilations, a complete gapless compiler DATA SEGDEF, a complete MAP
contribution, all raw bytes, original ordered fixups, tool/dependency/input
and generator freshness checks. Its own meaningful DATA mutation changes the
fixed speed from 192 to 193 subpixels per frame and is rejected. The accepted
source snapshots include the generator itself. All 1,024 bytes receive authored
C initialized DATA credit; no CODE or function credit is added.

Private `.analysis/shot-velocity-data-boundary-review.json` pins original
bytes, consumer instructions, mathematical evidence, independently verified
primary archive/member hashes and source identities. Run
`python3 .analysis/shot-velocity-data-review.py` for the bounded native review,
and `python3 scripts/generate_shot_velocity_table.py --check` for public
generator freshness without game or tool files.

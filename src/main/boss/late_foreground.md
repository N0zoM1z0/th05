# Yumeko and Shinki foreground callbacks

Both independent natural C++ owners are accepted against locally attested MAIN
SHA256 `c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Coordinates are original unrelocated load-module offsets, frame `AE1`, DS `209D`.

| Owner | Complete extent | Bytes | Instructions | Original ordered MZ offsets |
| --- | --- | ---: | ---: | --- |
| Yumeko | `14422..144C3` | 161 | 63 | `[144,126,85,43]` |
| Shinki | `13066..13106` | 160 | 60 | `[130,94,76,44]` |

These are 321 authored instruction bytes in two complete functions. There are
no padding bytes, switch tables, initialized DATA or BSS contributions.
The actual callback pointers in accepted stage setup independently anchor both
entries. Every original instruction and complete near RET boundary was checked.

The shared `late_foreground.hpp` imports the frozen complete 24-byte Boss from
`movement.hpp`, retaining full motion, sprite, phase and damage fields. Yumeko
also uses the full second Boss at DS `5AD2`. No shortened view or modified
accepted header supplies those records.

Yumeko's HP-fill phase is **0**. It draws entrance pattern 192 using Boss2's
position through the real `super_put_rect` API, then draws the animated main
sprite. Shinki selects the four 64-pixel pieces of a 256-pixel wing image,
centers them around the Boss, and chooses the corresponding four hit-pattern
pieces when damaged. The wing loop carries a real pixel coordinate across
sprite calls. Its ordinary `register int left` declaration follows a maintained
TH04 foreground idiom; no physical register macro, ABI substitution or
instruction template was imported.

Both callbacks use genuine far Pascal master graphics APIs, including the
five-argument one-plane function with pattern plane zero and put-plane mask
`FFC0`. Rectangle and 8-pixel-aligned sprite APIs retain three word arguments.
The large-explosion path uses the real large sprite renderer. Both real small
and big explosion updaters execute afterward as near calls in frame `AE1`.
Each normal drawing path consumes the Boss damage flag; the large-explosion
path preserves the original behavior.

`main-yumeko-foreground-a/receipt.json` passed two fresh full 161-byte producers,
raw bytes and the original ordered fixups. Its own compiled negative changes
the animation divisor from four to five and was rejected.
`main-shinki-foreground-a/receipt.json` independently passed two fresh full
160-byte producers and original ordered fixups. Its own compiled negative
changes the wing-pattern threshold from 184 to 185 and was rejected. Both
receipts are under private `.analysis/unit-replays/`, and both units were
imported by the root agent.

The symbol-only binders supply only real foreign symbols and origin holes
outside the complete compiled contributions. They contain no instructions,
owned bytes, initialized DATA or stack allocation. Native boundary reports and
candidate provenance remain in `.analysis/{yumeko,shinki}-foreground-*.json`.
The two CPP files, shared header and their binders are now frozen accepted
dependencies. TH04 donor acceptance was not transferred to these owners.

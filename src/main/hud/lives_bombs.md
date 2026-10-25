# Lives and bombs HUD candidate

The complete original pair is `[D035,D1A2)` in MAIN's unrelocated MZ
program image, 365 instruction bytes: `hud_lives_put`180 and
`hud_bombs_put`185. Both are genuine far C++ cdecl no-argument functions
ending in RETF. They contain no switch tables, NOPs or padding. Their ten
ordered original segment fixups are
`[360,325,291,253,222,175,140,106,74,43]`.

Natural source comes from maintained TH04 `src/main/hud/hud.cpp`, with the
donor's initial `-G` option retained before all C++ tokens. Actual TH05
globals replace TH04's resident fields: unsigned lives at DS4AD4 and
canonical signed bombs at4AD5. The new independent header includes only the
frozen basic ABI declarations and changes no accepted/shared type or owner.
The adjacent HUD indicators are a separate owner and header.

The original code assigns lives minus one to a signed byte local, uses signed
byte loop bounds, and formats larger values with signed division/remainder.
Bombs first uses the unsigned byte count comparison `CMP [4AD5],5 / JA`,
then the same signed local formatting. An ordinary unsigned-byte cast on that
one comparison preserves the native count domain while retaining gameplay's
canonical signed storage declaration. It creates no alias, fake object,
register hint or physical-register algorithm. Both actual stack frames hold
two signed-byte locals; the running text column uses the donor's ordinary
register-qualified integer, not a named machine register.

Gaiji and text calls retain the true MASTER far Pascal interfaces already
declared by accepted `overlay.hpp`: unsigned word coordinates, glyph and
attribute, with an actual far string pointer for text. The real callees are
0000:1D7A and0000:2598. Main code frame is AE1, DS frame209D. The distinct
11-byte formatting strings at DS13F0/13FB remain external real arrays; no
strings, gaiji assets, state, DATA or BSS are imported or defined. Glyph
constants are semantic values corroborated by pinned ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th04/gaiji/gaiji.h`.

All original branches and complete returns were checked in supplied locally
attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
The source is uncompiled and unaccepted. The first producer must establish
the entire365-byte contribution and both180/185-byte function boundaries in
actual MAP/OMF. Two fresh deterministic full raw comparisons, original ordered
fixups and a compiled negative remain necessary; donor acceptance does not
transfer.

The single meaningful control changes the lives icon/text cutover from6 to7.
It belongs to the whole pair and supplies no independent bombs-only control
claim. Private integration metadata, source hashes, native instructions and
outside-only binder are in `.analysis/hud-lives-bombs/`. The binder contains
no owned instructions, string bytes, state values, synthetic callee body or
artificial stack.

## Accepted result

`main-hud-lives-bombs-a` passes both fresh deterministic producers for all365
instruction bytes and all ten original ordered fixups. The actual MAP/OMF
boundaries are180 and185 bytes, with no owned DATA, tables or padding. The
compiled lives threshold6-to7 control was rejected. This accepts the two
complete functions as one owner; it does not claim an independent bombs-only
negative. Source, header and maintained binder are frozen accepted inputs.

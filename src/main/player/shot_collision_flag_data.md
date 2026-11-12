# Original shot-to-Boss hit-test arbitration flag

The byte at MAIN load offset `22790` (DS:`1DC0`) is the actual mutable
`shots_hittest_against_boss` flag. The retained ReC98 source
`th04/main/player/shots_hittest[data].asm` initializes that named byte to
zero. In the accepted TH05 Boss collision code it is set to true before
calling the shot intersection routine and reset to false afterward; the
accepted Mai/Yuki midboss hit routine uses the same byte. Both complete shot
collision consumers independently read DS:`1DC0` to choose the real Boss
collision behavior. This is not an inferred identity from zero bytes alone.

The maintained C++ initializes the canonical 1-byte `bool` through the
existing resident ABI typedef, producing **one complete original DATA byte**
at `[22790,22791)`, and no CODE or BSS. Its focused replay under
`.analysis/unit-replays/gpt-web-main-shot-boss-flag-a/receipt.json` proves
two genuine Borland C++/TLINK producer copies, exact MAP/OMF/bytes, original
empty ordered MZ fixups, and a rejected compiled `false` to `true` negative.
The following original byte `[22791,22792)` is **not** included: it remains
unreviewed alignment/foreign state instead of being silently counted as a
second boolean. Existing larger Boss and shot functions retain their separate
exact accepted ownership, without a full cold replay or duplicate credit.

# Mai/Yuki late-wave source factoring

The complete ten-pattern, 939-byte C++ contribution now names its shared
Yuki muzzle position through `MY_YUKI_MUZZLE()`. Seven independent red-ball,
ring and spread functions use that same *real* second-Boss X coordinate and
positive Y muzzle offset. Their separate projectile settings, calls and
pattern timers are unchanged. Mai's independent first-Boss muzzle is not
rewritten. Both late-game Cheeto functions also share the original
`MY_FIRE_AIMED_CHEETO()` sequence (aim from each character's own chosen
position, enqueue the Cheeto and play the attack sound), while their side
selection and return values stay distinct.

The common body lives in `remaining_patterns.inl`, which is also compiled as
preceding authentic context for the large paired-Boss updater. Therefore both
affected *complete* original owners were replayed, not merely an isolated
function:

| Owner | Full native CODE bytes | Original ordered MZ relocations |
| --- | ---: | --- |
| `main-mai-yuki-remaining-patterns` | 939 | `[920,833,462,136]` |
| `main-mai-yuki-update-context` | 1,018 | `[942,931,915,898,874,723,312,171,123]` |

Two independent Borland/TLINK producers passed every complete original
extent, OMF/MAP link and ordered relocation check. The accepted compiled
negative for the shared patterns was rejected. The scoped evidence is
`.analysis/unit-replays/gpt-web-maiyuki-remaining-seven-muzzle-20261112-a/receipt.json`.
This improves the shared natural source but does not increase already
accepted authored CODE credit. No unrelated full cold replay was run.

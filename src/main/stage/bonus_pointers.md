# Stage-bonus near-pointer DATA

The proposed complete initialized-DATA owner is `[22434,2245E)`, 42 bytes,
at DS `209D:1A64..1A8E`. It contains the eleven-entry description lookup and
ten actual mutable label-pointer variables used by the accepted bonus
functions. Every entry is a genuine two-byte near pointer. The full descriptor
bank therefore occupies 22 bytes, matching the frozen helper declaration.

The source initializes these objects using semantic names of the 21 complete
readable UI text arrays maintained in `bonus_strings.cpp`. No numeric offset,
copied pointer byte array, image, font or replacement text is defined. Native
review independently resolves all 21 original words to the exact starts of
those accepted text objects, preserving timeout/credits/continues/difficulty
ordering and the ten actual label roles. All original loader relocations are
absent because the pointers contain near DGROUP offsets; compiler OMF fixups
still require full producer validation.

The source preserves the existing descriptor's const-pointer declaration and
the label variables' mutable-pointer declarations without changing any
accepted header. It defines no state, CODE, BSS, text payload or padding.
All 42 bytes must compare normally.

The symbol-only binder supplies a DATA prefix ending at `1A64`. The compiler
must then own the whole 42-byte `_DATA` contribution ending at `1A8E`. A
separate foreign DATA tail supplies real symbolic text-object labels, starting
after the complete owner. Its initial nineteen-byte outside gap skips the
unclaimed gaiji strings. Neither their bytes nor the already accepted text
payload are emitted by the binder. It contains no internal hole, stack or
dummy instruction.

The own negative makes the Easy modifier select the real Normal description
instead. This is a meaningful near-pointer DATA change. Complete gapless
compiler LEDATA, actual MAP extent, two fresh producers, full raw/original
ordered relocation comparison, input/tool identities and that compiled
mutation were verified by `main-stage-bonus-ui-pointers-a`: both fresh
42-byte producers passed raw bytes and the empty original relocation stream,
with complete OMF/MAP/dependency/tool checks. The own compiled Easy-to-Normal
description-pointer mutation was rejected. All 42 bytes were imported as
semantic authored DATA and committed in `d07521f`.

Private review and proposal files are
`.analysis/stage-bonus-pointers-boundary-review.json` and
`.analysis/stage-bonus-pointers-unit-proposal.json`. The bounded native audit
is `python3 .analysis/stage-bonus-pointers-review.py`; it records all original
targets, semantic field roles, provider addresses and source hashes.

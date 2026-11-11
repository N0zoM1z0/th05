# Exact original ZUN.COM inner command dispatcher and catalog

The ZUN.COM command dispatcher is a small executable in its own right: it
prints the supported `-O`, `-I`, `-S`, `-G`, `-M` commands, matches DOS FCB1's
8-byte program name to its table, copies FCB2 to FCB1, removes the selected
option from the PSP command tail, and transfers execution into the matching
embedded child. It also uses a final, original 8-byte `REP MOVSB`/`RETN`
helper to move the selected child back to COM runtime `0100` before running.

This exact retained semantic source is [dispatcher.asm](dispatcher.asm),
corroborated by the original build procedure in pinned ReC98
`Pipeline/{zun_stub.asm,zungen.c}`. It defines the five real child names,
uses named child *lengths*, and builds the 33-entry transfer catalog with
ordinary TASM label arithmetic. **It does not contain any child payload
instructions or assets.** There are source-only `ORG` reservations for their
real program sizes; all such holes must be zero in the proof-local COM.

## Full native physical ranges (ZUN.COM file)

| Original file range | Description | Compared bytes | Credit class |
| --- | --- | ---: | --- |
| `012F..020E` | Native dispatcher: two-byte jump, 2-byte scratch, 19-byte diagnostic text, and remaining 200 instruction bytes | **223** | 202 CODE + 21 initialized scratch/message |
| `020E..0355` | Five-entry count, 32 names, 33 destination offsets, final near CALL | **327** | 3 CODE + 324 semantic catalog bytes |
| `0355..4678` | Five independently bounded embedded programs | **17,187** | **Foreign placeholders, zero credit and no bytes supplied** |
| `4678..4680` | Native `REP MOVSB; POP AX; MOV AX,100h; PUSH AX; RETN` transfer helper | **8** | 8 CODE |
| **Total new source-owned compared bytes** | **Two discontiguous original scopes** | **558** | **213 CODE + 345 data** |

The code above starts at runtime `0100`; the catalog begins at `01DF`. The
first child begins at runtime `0326`. Subsequent runtime entries `06C4`,
`0AB5`, `2459`, `4512` are derived from the five original child lengths
(926, 1009, 6,564, 8,377, 311). The final transfer helper starts at `4649`.
The separate outer COMCSTM header/usage/wrapper does not belong to this
source, and neither does the unaccepted resident `-S` child.

## Strict focused acceptance and origin limit

The native focused evidence lives at
`.analysis/zun-dispatcher/gpt-web-dispatcher-clean-b/receipt.json`. Two independent
TASM32/TLINK producers both match **550/550** prefix+catalog bytes and **8/8**
transfer bytes against the original ZUN.COM, with exactly the actual label
addresses in MAP and stable normalized OMF. A source mutation copying only
15 instead of 16 bytes of the second DOS FCB is assembled and rejected by
the complete instruction comparison; the catalog, transfer helper and all
foreign child holes must remain unchanged.

The source's unfilled foreign spans are not a new reconstructed COM image.
They are proof-only address reservations outside the 558 source-owned bytes.
The original **17,187 child bytes are not copied, rebuilt, credited or
replayed** by this unit. The pinned build reference strongly supports the
source family, but literal historical source identity and inclusion in the
global authored numerator remain unreviewed, independently of exactness.

Acceptance manifest:
[`config/zun_dispatcher_acceptance.json`](../../../config/zun_dispatcher_acceptance.json).
A source-current check runs without loading Wine, the original game or
compiling the five children:

```sh
python3 scripts/replay_zun_dispatcher.py --check
```

To replay **only the dispatcher, catalog and helper** from the original native
TASM/TLINK tools, then explicitly adopt its receipt:

```sh
python3 scripts/replay_zun_dispatcher.py --output .analysis/zun-dispatcher/NEW
python3 scripts/replay_zun_dispatcher.py --accept .analysis/zun-dispatcher/NEW/receipt.json
```

# Render all score places: exact C++

MAINE `BCD3..BCED` is one complete 26-byte near Pascal function, with an int
character argument and RET2. Its 14 instructions iterate places 0..4 and call
the real two-int near Pascal row renderer at `BBEF`. SI/BP are preserved.
CS is `A54` / GROUP_01 and DS `1011`; there is no padding, table, DATA, BSS
or MZ fixup in this scope. No character validation or return value is invented.

The ordinary register-local loop follows maintained TH04's
`maine/score/places_put.inl`, with TH05's canonical five-place score layout/count
imported unchanged. ReC98 `th05_maine.asm` `sub_BCD3` and the pinned decoded
original establish the actual boundary, row-provider address and word arguments.
The row renderer remains foreign; donor acceptance does not transfer.

Two fresh direct C++ producers pass valid ordinary OMF, complete MAP scope,
all raw bytes and original empty fixups. The compiled five-to-four-place
negative is rejected. No accepted source/header or producer tool changed, so no
old unit was rebuilt.

Receipt: `.analysis/unit-replays/maine-registration-places-a/receipt.json`,
SHA-256 `2cb43901fe3dd7fee72f1635e74b44b4aceb68d5dff9f6c625cc1db7c7260bc5`.
Native/source/ABI review: `.analysis/registration-places-native-review.json`,
SHA-256 `a1497e74636200d7709095be04b8a665891d834fc7d7471041c62a3fb9bca60b`.
New credit is one function and 26 C++ instruction bytes. Target provenance is
candidate-local-attested; decoded acceptance makes no packed-file claim.

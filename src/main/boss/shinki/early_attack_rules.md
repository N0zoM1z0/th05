# Shinki's first two waves: blue ring, dual-speed and kunai/stack protocol

The genuine early Boss callback functions after `b6balls_update()` now
share `early_attack_rules.hpp` with the full **959-byte** original Shinki
Boss controller. The actual code and all near callbacks still live in
the accepted `shinki.cpp` translation unit. The header supplies only
compile-time gameplay values; no BSS, fabricated sprite, video memory,
new callback array, or compiler barrier is introduced.

**The first curved-ring pattern** sets a sixteen-bullet blue outline
ring at speed two pixels/frame, chooses a signed +2/-2 angular turn
with one random bit, and fires every four frames. Each volley advances
the existing speed by 0.5 pixel/frame while applying the same signed
byte angle to the template. It completes exactly 28 frames after the
original 32-frame setup milestone. The companion dual-speed ring
also has sixteen shots but selects a genuine rank-dependent firing
interval **16/12/8/4** (easy/normal/hard/lunatic), chooses a random
32-pixel origin radius, fires a two-pixel ring followed by a four-pixel
ring shifted eight angular units, and completes 64 frames after setup.

**Preparation and second wave.** The helper initializes the real
charge/gather geometry 16 frames before the 32-frame attack setup,
with colors 7 and 6 and the original frame-2 copied red-ring template.
The latter is intentionally not used as a live first-wave firing
sequence; no speculative new bullets are introduced. The directional
kunai callback thereafter uses the original random-angle three-shot
template at 1.75 pixels/frame, and fires its two mirrored blue bullet
patterns every second frame from quarter-wing horizontal offsets.
The dense aimed blue stack callback uses a two-bullet angular spread
of four units, and the exact rank-specific stack count and step
`(5,0.75)`, `(6,0.75)`, `(6,0.8125)`, `(7,0.8125)`.
It fires every fourth frame. Both callbacks preserve the original
32-frame flystep-relative lead and their real `boss_statebyte[15]`
state, without changing branch polarity or randomized call order.

The **complete far-Pascal Shinki controller** now gives its original
16-pattern first-two-wave timeout the same source definition as the
first-pattern sources. The maintained distinct 3,000-frame later wing
threshold remains in the original 16-bit local enumeration: it is not
removed or moved to an all-byte enum, which would change Borland's
DX versus DL parity masking and break original code identity.

The affected eleven accepted source scopes were all recompiled under
two independent native Borland producers, including the complete
**271-byte two-function ring group**, **94-byte kunai**, **96-byte blue
stack**, **959-byte Boss update** with its original 26-byte switch
table and checked alignment, and the neighboring accepted ball/rain/
wing/spiral/float functions. Full literal original bytes, public/MAP
boundaries and ordered MZ fixups are identical, and the actual compiled
ring-completion 28→32 mutation is rejected:
`.analysis/unit-replays/gpt-web-shinki-early-boss-patterns-a/receipt.json`.
No already accepted CODE bytes are counted a second time and no
all-main cold replay is performed.

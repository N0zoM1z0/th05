# Yumeko mobile-fight bounce, mirrored sword fan and red ring

The original 435-byte three-function C++ contribution contains three
distinct real algorithms: `yumeko_flystep_bounce`, `yumeko_pattern_sword_fan`,
and `yumeko_pattern_red_ring`. They now share one source-level
`mobile_attack_rules.hpp` rather than unlabeled numeric operations.
None of these constants introduces BSS, a new scratch byte, a graphics
asset, or a code-generation barrier.

The bounce mover seeds its original velocity and movement sprite on phase
frame one. It moves both signed subpixel coordinates before reflecting
at the **inclusive X rectangle [48,336] and Y rectangle [48,128]**.
Each signed velocity component is negated independently at the associated
edge; the return to the idle sprite and true completion still occur only
at the caller's exact `end_frame`. The full 884-byte Yumeko Boss update
uses this mover twice with its original **2-pixel speed and 64-frame
movement window**. The attack callbacks are selected using the original
one-bit `patterns_seen & 1` index in their respective two independent
four-slot near-callback tables. Both the mover and the actual full
Boss controller now name that same existing protocol.

The sword fan charges at frame 16 with twirl time 48, speed five pixels
per frame, initial angle 0x70, and one random mirror-side bit. Shots
begin only after frame 32, firing on even frames at a 48-pixel origin
radius. The reflected side uses 0x80 minus its original angle before
and after creation, while each volley decreases the source angle by
six. The original terminal angle comparison is **≤ 0x0C** and returns
to the existing reposition mode; no turn count or mirror state changed.
The red-ring attack charges for 32 frames using colors 7 and 6,
initial speed 60 subpixels, a 16-shot ring and sound 8 at frame 16.
It then fires every four frames from a random 32-pixel radius and
repositions exactly at frame 80, keeping the original sound 3.

The two source owners `patterns.cpp` and `update.cpp` were changed
and `patterns.cpp` is also included in the authentic nine-function
compiler context used by two independently accepted attack callbacks.
Therefore **four affected complete original scopes** were selectively
replayed in one native batch, with two Borland producers, complete raw
bytes, original ordered relocation sites, and a compiled right-edge
336→335 mutation rejected:
`.analysis/unit-replays/gpt-web-yumeko-mobile-attack-rules-a/receipt.json`.
The four byte-exact owned extents are 435, 884 (including the checked
zero and its 22-byte compiler switch table), 354 and 428. The 283-byte
`swords_update()` now has a raw-exact hybrid C++/inline-ASM context provider;
its interval remains credited only to the separate reviewed-ASM owner. No
new or borrowed CODE credit is claimed. No whole cold replay or machine-code
patch was performed.

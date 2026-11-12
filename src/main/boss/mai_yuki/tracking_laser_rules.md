# Mai tracking laser: native angle-follow and charge timing

The original MAIN callback `mai_pattern_tracking_laser()` is one complete
**186-byte** near C++ function, independently owned by
`main-mai-yuki-tracking-laser-compilerasm`. The source now uses
`tracking_laser_rules.hpp` to name its physical laser events:
frame **48** aims from the Boss to the player's then-position and
spawns fixed laser slot **0**, width **8** and color **8**; frame **80**
starts its growth. The beam retargets every **fourth frame** between
frames 80 and 143, but only every eighth frame outside that interval.
At frame **160**, it stops the same laser and returns true, ending
the attack. There is no invented target prediction, attack slot or
phase timer.

The genuine signed-byte angular difference is computed from the same
`iatan2` return and the live `lasers[0].coords.angle` using the original
AL byte register. The one authentic inline `asm { sub angle_delta,al; }`
expression and the original `++_AL` / `_AL += -1` byte writebacks are
**left untouched**, rather than replacing their exact compiler-required
register path with a fake arithmetic equivalent. Only compile-time
names for already existing comparisons, color/width, laser index and
lifecycle calls were added. Neither additional runtime state nor
instructions from the target binary are introduced.

The original source TU uses a pinned **TCC -S → TASM32** natural C++
producer to preserve the original `[38,130]` near/segment relocation
order. The bounded receipt
`.analysis/unit-replays/gpt-web-mai-tracking-clock-a/receipt.json`
passes two independent original-size compiler/assembler/linker chains,
all **186/186 raw bytes**, original OMF/MAP scope and literal ordered
MZ relocations. The compiled, meaningful stop-frame mutation 160→161
is rejected. The independently accepted Mai/Yuki 1,018-byte Boss
controller and other attack functions remain unchanged and earn no
second CODE credit. No complete executable or full cold replay was run.

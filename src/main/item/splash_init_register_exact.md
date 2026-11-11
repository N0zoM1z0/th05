# Exact item splash pool initialization

The complete near `item_splashes_init()` function at MAIN `[16362,1637C)`
clears all eight 10-byte splash records (80 bytes) and resets the one-byte
ring index. Its natural Borland C++ source uses the existing canonical pool,
sets the word count in CX, selects the caller's DS as the ES destination, and
executes the original `REP STOSW` through Turbo C++'s register interface.

A previous high-level `memset` producer generated 24 bytes, and a first
register-aware producer generated the correct 26-byte layout but selected
`33 C0` instead of the original `31 C0`. The semantic inline
`XOR AX,AX` permits the original instruction encoding with no emitted opcode
array, object patch, or changed pool contents. The original `main_03` CS
and DGROUP placement and the empty relocation stream are retained.

Focused acceptance:
`.analysis/unit-replays/gpt-web-main-item-splash-init-register-exact-a/receipt.json`.
Two fresh Turbo C++/TLINK producers match all 26 bytes, the original empty
ordered fixups, and complete OMF/MAP ownership. Decreasing the native
40-word clear by one word compiles and is rejected. The earlier `memset`
source remains a documented semantic alternative, not a second accepted owner.

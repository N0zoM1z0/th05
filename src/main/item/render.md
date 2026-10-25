# Complete item and spawn-splash renderers

Two natural high-level TH04 donor bodies now recover their separate complete
TH05 functions. Only GAME5's already canonical counts and layouts are used;
no donor acceptance transfers.

| Whole C++ CODE contribution | Native MAIN scope | Instructions | Ordered fixups |
| --- | --- | ---: | --- |
| `items_render()` | `138E4..1392B` | 71 bytes /32 instructions | `[]` |
| `item_splashes_render()` | `DCA7..DD2A` | 131 bytes /48 instructions | `[50]` |

Both functions use C Pascal near linkage, have complete near RET boundaries,
and contain no instruction NOPs, tables, padding or owned DATA/BSS. Every local
branch reaches an instruction start. Both bodies are literal maintained TH04
`items_render.cpp` / `splashes_render.cpp` bodies. Full canonical item20/splash10
records and pools40/8 are reused; pinned ReC98 explicitly gives GAME5's32 dots
rather than GAME4's64.

Items establishes ES=A800, renders spawn splashes, then draws only alive items
with Y greater than -128 subpixels. It keeps the original absence of upper/X
clipping. Splash rendering uses current radius,32 evenly spaced angles and
native playfield clipping before the dot write. The real color helper receives
AH=15, preserves the incoming GRCG mode, and reenables interrupts. No additional
RMW selection, graphics-off call, CLD or ES assignment is inserted.

The dot helper is the existing near fastcall `@item_splash_dot_render` atE152,
receiving AX=x/DX=VRAM Y, writing through the incoming ES and returning without
stack cleanup. The tiny sprite helper atC07C receives AX/DX and one Pascal
pattern word, RET2. DOS register intrinsics only transport those genuine API
arguments and the GRCG color; no compiler arithmetic template is supplied.
The foreign vector provider remains far Pascal14AB:03B0, and signed scroll
conversion remains the existing near Pascal entry atDF28. Their code and image
resources receive no credit.

Each immutable symbol-only binder has before/after views with exact ordinary
16-bit segments, groups and endpoints. The prefix declares foreign gaps and
SHARED before the compiler can introduce its empty SHARED SEGDEF. This preserves
SHARED at14AB and the empty ITEM_SPLASH_TEXT/main_03 context at1527. No helper
body, initialized value, entry, stack, owned gap, byte normalization or relocation
sorting is used. The unmangled C exports use complete actual CODE contributions,
not the demangled C++ function-public lane.

Only these receipts supply acceptance:

- `.analysis/unit-replays/main-item-render-c/receipt.json`, SHA-256
  `474f76b2926465c7a37e714ecc50b221bc0e00decdc0f253d8bafee9be345445`.
- `.analysis/unit-replays/main-item-splash-render-c/receipt.json`, SHA-256
  `6f59779f016de2b0836ce3169faa5d08a69054efdb3dc20c747e0622eecef4d5`.

Each has two fresh deterministic complete producers and its own compiled
negative: items changes the exact lower-Y boundary, and splashes changes color15
to14. Each changes actual output while retaining its whole extent and ordered
fixups and is rejected. Installed execution probes and old accepted objects are
reused. All older source/header/acceptance identities remain unchanged.

Attempt-a stopped before a C++ object on duplicate declarations already supplied
by canonical headers. The new header now reuses their PlayfieldPoint drawpoint,
plane constant and color macro. Attempt-b's splash algorithm was identical except
its vector selector: the first-seen empty SHARED SEGDEF preceded the intended gap.
Correcting actual segment ordering repairs those three operand bytes. Item71-b
already matched, but final-c also corrects its otherwise unused foreign contexts.
Only final-c is imported; earlier snapshots and verdicts remain unchanged.

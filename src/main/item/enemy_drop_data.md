# Automatic enemy drop schedule

The complete immutable `unsigned char ENEMY_DROPS[64]` definition owns original
MAIN `[22792,227D2)`, DS `209D:1DC2`. It uses the unchanged full item header
and its canonical item-kind constants. These are gameplay choices, not sprite
indices or asset bytes.

The accepted `items_add` consumer increments the byte drop counter, returns
for odd requests, then reads `(counter / 2) % 64`. Original instructions use
the literal divisor64 and byte load `[bx+1DC2]`; the complete declaration and
consumer independently establish all64 cells. Ordinary power/point entries
and the final big-power entry express the deterministic gameplay schedule.
The pinned ReC98 `th05/main/item/enemy_drops[data].asm` provides semantic names;
its acceptance does not transfer. Native matching finds the whole table once,
with no intersecting accepted owner, relocation, padding or trailing terminator.

`main-item-enemy-drop-data-b` proves all64 compiler DATA bytes in two fresh
deterministic producers, the complete OMF/PUBDEF/MAP extent and the original
empty ordered-fixup list. The compiled first-drop power-to-point mutation is
rejected. No accepted caller or shared header changed.

The first attempt stopped at linking: the full unchanged item header declares
an empty `HUD_OVRL_TEXT` segment in `MAIN_01`; leaving it to the end exceeded
the real64KiB group window. The binder now places that empty foreign segment
inside its original group, as the accepted spawn binder does. It emits no HUD
body or table values and reserves only outside addresses. Failed attempt a
and successful b remain separate private evidence.

The private native review is `.analysis/main-item-enemy-drop-data-native.json`.
Comparison uses the pinned original unrelocated image and relocation stream;
no decoder or original game is executed and packed-file equality is unclaimed.

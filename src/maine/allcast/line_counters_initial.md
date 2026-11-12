# MAINE all-cast line indices: source-exact semantic DATA

The original MAINE `[109FA,109FE)` (DGROUP `1011:08EA..08EE`) contains two
adjacent zero-valued 16-bit line cursors. The retained all-cast source names
`line_id_total` and `line_id_on_screen`, and the accepted native
`screen_line_next_animate()` reads, increments and resets both of them.
The actual retained MAP exposes `_line_id_on_screen` at calibration
`1010:08EC`; the preceding word corresponds to `line_id_total` through
its original native consumers. Together they occupy the complete four-byte
gap after the 202-byte line-pointer/count table and before the independently
accepted cast background filename strings.

`line_counters_initial.cpp` is a *semantic reconstruction* of both mutable
counters as initialized 16-bit C++ scalars. The original ReC98 C++ has a
tentative global definition for `line_id_total` and an extern declaration
for `line_id_on_screen`; it does **not** prove that these two historical
variables were emitted as a standalone initialized translation unit.
The maintained source's complete genuine Borland `_DATA` LEDATA, byte
values, MAP scope and empty ordered relocations match the four target
bytes in **two independent original-compiler/linker producers**. An
independently compiled `line_id_total = 1` mutation is rejected.

Evidence: `.analysis/unit-replays/gpt-web-maine-allcast-line-counters-first-a/receipt.json`.
The ledger accepts **four source-authored C++ semantic DATA bytes**, not a
claim about the exact historical C++/BSS translation-unit arrangement.
No neighboring byte or previously accepted all-cast function is recredited.

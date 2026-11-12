# MAINE All Cast's one-byte double-buffer displayed-page latch

The decoded original MAINE `[1086E,1086F)` is the complete mutable
near DATA public `_page_shown`, exactly one byte initialized to zero
at original DGROUP `10110:075E`. The original
`_reference/ReC98/th05_maine.asm` declares this byte immediately
after the cutscene Shift-JIS glyph buffer and before `evendata` and
the accepted All Cast background pointer bank. Its real accepted
**611-byte All Cast controller** reads the same `page_shown` byte in
`wait_flip_and_check_measure_target()`: it first sets the PC-98
*access* page to the previous shown page, then changes the byte by
`(1 - page_shown)` and sets the *displayed* page through the
actual hardware port. The 1-byte type is the genuine C++ `page_t`,
whose original source alias is `unsigned char`.

The maintained native C source defines `unsigned char near page_shown =
0`, with an actual one-byte compile-time width proof. Its original
`10110:075E` prefix is supplied by the external-only linker binder,
which also declares the exact MAINE group_01 and SHARED CODE frames.
No candidate byte, false code instruction or extra relocation is copied
into the binder.

The preceding alignment byte `[1086D,1086E)` and following
alignment byte `[1086F,10870)` remain **UNKNOWN**; the already
accepted three-byte cutscene Kanji buffer and 192-byte All Cast
background pointer/quarter index remain independent DATA owners.

The focused two independent native Borland C/TLINK producers and their
actual compiled page-initializer negative 0→1 pass full original raw,
OMF/LEDATA/MAP initialized-DATA extent and empty ordered MZ fixups:
`.analysis/unit-replays/gpt-web-maine-allcast-original-page-latch-a/receipt.json`.
This is **one** newly authored initialized DATA byte; all prior CODE
remains unchanged. The complete 611-byte controller will be recompiled
with its source-current C linkage separately. No all-game cold replay
was run.

## Source-current 611-byte All Cast controller and exact page flip (2026-11-12)

The real page toggle is now imported through `page_shown.h` as a native
C public rather than a loose C++ `extern page_t` declaration. The C
source and complete All Cast renderer share the original near one-byte
name, with the actual `page_t` still defined as `unsigned char`.
The two target pages sum to one; naming that constant preserves the
original `graph_accesspage(page_shown)` followed by
`graph_showpage(page_shown = (1 - page_shown))` call order. The logic
still runs from the genuine `wait_flip_and_check_measure_target()`
function, not a replacement double-buffer helper or new state byte.

The complete native **611-byte three-function** All Cast controller
and the independently accepted 190-byte line renderer were recompiled
in two fresh pinned Borland C++ rounds. All original CODE bytes,
OMF/MAP scopes, ordered MZ fixups and the compiled meaningful
negative remain exact. The separate one-byte C source was also rebuilt
twice with the compiled page 0→1 mutation rejected:

- `.analysis/unit-replays/gpt-web-maine-allcast-page-controller-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-allcast-page-c-public-b/receipt.json`

This closes a genuine C-to-C++ interface without recrediting existing
CODE or the one already accepted DATA byte. The original extra
background pointer/quarter arrays remain independent initialized
contributions. No full MAINE cold replay was run.

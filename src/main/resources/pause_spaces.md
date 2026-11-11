# Original pause-screen blank texts: 15 initialized DATA bytes

The original MAIN `20BDD..20BEC` has three independent five-byte text
resources used by the pause-screen eraser. Each holds four ASCII spaces
followed by `\0`. The original retained `th04/main/pause[data].asm` identifies
three distinct strings, and the TH05 load module preserves their independent
contiguous storage immediately before `DEMO0.REC` at `20BEC`.

`pause_spaces.c` uses a natural C aggregate containing three separate
five-character fields and a semantic blank-text constant. Compile-time
size and offset assertions protect the real 15-byte layout. The separate
symbol-only binder locates the odd-address source extent at DGROUP:020D
without placing any padding, foreign initialized data or executable bytes.

Two independent pinned Borland/TLINK producers match all 15 original bytes
and the empty ordered relocation list. Changing the blank-text source
constant to an exclamation mark fails the actual-byte comparison.
Receipt: `.analysis/unit-replays/gpt-web-main-pause-text-20261111/receipt.json`.
The struct grouping is a maintained semantic model, not a claim about the
exact historical source declaration.

# Original TH05 Extra dialog sequence initial state

MAIN byte `[2293D,2293E)` at DS `209D:1F6D` is the original signed
`dialog_sequence_id`, explicitly initialized by `_dialog_sequence_id db 0`
in pinned `th05_main.asm`. The accepted `dialog_animate()` and dialog tail
routines read the signed byte to distinguish first Extra-demo continuation
from the subsequent exit, and increment it after starting the demo replay.
Its one-byte type is declared in the existing `tail.hpp` ABI.

`sequence_initial.cpp` defines exactly this mutable C++ scalar as zero.
Two independent Borland/TLINK producers matched the complete one-byte
`_DATA` extent at its original MAP position and empty loader relocations;
the compiled `0`→`1` negative failed as intended. Focused receipt:
`.analysis/unit-replays/gpt-web-main-dialog-sequence-20261112-a/receipt.json`.
The neighboring dialog resource strings and Sara attack schedules retain
their separate already accepted owners.

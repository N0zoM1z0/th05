# TH05 STD stage/script file loading: exact C++

MAIN `std_load()` now matches its complete 184-byte near-C++ body at
`[C742,C7FA)`, with original ordered MZ fixups `[43,173]`. It frees the
previous STD segment, changes the filename stage digit, opens the new file
with DOS INT 21h, reads its two-byte length, allocates a real-mode segment,
then reads the entire payload through the native DOS file interface. It
preserves the game's unchecked file/allocator behavior, original SI/DI and
DS save/restore, and leaves ES pointing to the allocated segment.

The parser records three far pointers to NUL-terminated titles using a
shared `ES:DI` cursor and a single `CX=FFFFh` register value across three
`REPNE SCASB` scans. It reads the map-section and scroll-speed counts
through 386 `MOVZX` semantic inline assembly, preserving the byte-count
quirk that initializes `scroll_speed` from the chunk's length byte. It
stores 32 possible enemy-script near offsets in their real DS table at
`362A`, advancing by length-prefixed scripts without overflow checks, and
finally stores the far STD instruction pointer and original `std_run`
callback location at `main_03:1906`.

## Native compiler context

The regular Turbo C++ 4.02 `-c` assembler cannot parse all 386 `MOVZX`
spellings. The maintained C++ instead passes through the existing *genuine*
TCC `-S` → TASM32 → TLINK pipeline, without rewriting generated assembly.
The original script-count loop uses `DEC DL; JNE script_next`; expressing it
as a C++ `while(_DL != 0)` caused an unnecessary `OR DL,DL` and emitted
186 bytes. The semantic assembler branch restores the complete 184-byte
body with unchanged runtime behavior. The original `main_03` callback is
bound symbolically through `SEG MAIN_03` and `OFFSET MAIN_03:std_run`, not
through hard-coded addresses. This restores the far-pointer relocation and
avoids the cross-group 16-bit fixup overflow seen in diagnostic trials.

The complete C++ source declares actual external segment and near/far pointer
roles and supplies no initialized data or loader/file byte arrays. The
address-only binding preserves `main_01` CS `AE1`, DGROUP `209D`, the genuine
near `std_free` provider at `C7FA`, the real `std_run` entry at `16B76`,
and the allocator at `_TEXT:281A`.

Focused acceptance:
`.analysis/unit-replays/gpt-web-main-std-load-tcc-s-near-a/receipt.json`.
Two independent TCC/TASM32/TLINK producers reproduce all 184 original bytes,
the literal ordered `[43,173]` relocation list and full OMF/MAP public
boundaries. A compiled stage-filename mutation (`'0'` to `'1'`) is rejected.
The earlier origin review remains useful for the separate MAP loader, but its
old classification of STD as unowned is superseded by this exact natural
C++ acceptance. No full cold replay was run.

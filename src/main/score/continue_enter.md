# CONTINUE score entry: exact C++

MAIN `C998..C9A3` is the complete 11-byte near C++ void/no-argument entry.
CS is `AE1` / `main_01`, DS `209D`. It reads the byte `turbo_mode` at DS
`5776` and calls the foreign insertion routine at `C8F0` only when nonzero.
The RET at `C9A2` completes the function; the following `C9A3` NOP is outside.
There is no padding, table, DATA, BSS or MZ fixup in this scope.

The natural condition follows maintained TH04's `main/score/ranking.cpp`,
with TH05's actual omission of the score-file load call. The canonical caller
already declares this near C++ interface. No file I/O, validation, defensive
condition or score-state mutation is added. Insertion and the accepted ASM
codec remain separate owners; their acceptance does not transfer.

Two fresh direct C++ producers match valid ordinary OMF, the complete MAP
contribution and all original raw bytes/empty fixups. The normal guard-inversion
compiled negative is rejected. No accepted dependency or build tool changed.

Receipt: `.analysis/unit-replays/main-score-continue-entry-b/receipt.json`,
SHA-256 `20345b78bff26f7fb51164d242ce76d43b390c35e9d5bd127f2c78ceacf0120e`.
Native/source/ABI review: `.analysis/score-continue-entry-native-review.json`,
SHA-256 `e8e58d723c7f709924594eb27b9eee9ca183f2d8811a384af6890dcc42ec4969`.
Target provenance is candidate-local-attested. New credit is one complete
function and 11 C++ instruction bytes, with no whole-game claim.

## 2026-11-11 raw high-score insertion investigation

The original complete `hiscore_continue_enter_raw()` at MAIN
`[C8F0,C998)` is a 168-byte, no-relocation, near return function whose
register protocol is distinct from the accepted 11-byte caller and 22-byte
high-score display loader. The native scan compares eight unsigned gaiji
digits; the first lower rank makes space by moving complete names, scores
and stage bytes. It inserts the fixed CONTINUE gaiji name, copies the current
eight-digit score, re-encodes those digits with the `0xA0` gaiji base,
normalizes the extra-stage identifier and saves through the existing DOS
score writer at `C8B9`. The procedure uses `BX`/`CX`/`DX` for candidate
ranking and `SI`/`DI` with `ES=DS` for overlapped string moves; it must
preserve SI/DI and the original early-return behavior.

A full typed source attempt with exact foreign state addresses and a
zero-payload linker binder was compiled against Borland 4.02. The first two
attempts failed parsing the 386-only `MOVSD` string instruction as inline
assembly; writing `movs dword ptr` also failed at the same complete-source
location. There is no accepted result, no second deterministic producer, and
no compiled negative. Its proposed source, binder and unit proposal remain
under `.analysis/gpt-web-score-continue-raw-proposal/`, with preserved
first-producer logs under `.analysis/unit-replays/gpt-web-main-score-continue-raw-{a,b,c}/`.
The next useful investigation is an authentic source-language treatment of
the 386 string-copy primitive and compiler allocation, not copying target
bytes, normalizing output or claiming a passing score insertion function.

## 2026-11-11: resolved by real TCC `-S` and TASM32

The earlier direct-`-c` assembler problem above is now resolved. A complete
source with semantic 386 `MOVSD` mnemonics is accepted as
[168-byte exact C++](continue_raw.md); using the native TCC `-S` output
through TASM32 preserves both original bytes and fixups. The historical
failed experiments remain compiler-language diagnostics, not current blockers.

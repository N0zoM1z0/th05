# Current score file: exact C++ save and load

MAIN `C8B9..C8F0` is the complete 55-byte `scoredat_save_cur` function:
22 instructions, near C++ void/no arguments, RET0, CS AE1 / main_01, DS 209D.
There are no MZ relocations, NOPs, tables, padding, initialized DATA or BSS.
All original instructions and calls to the separately accepted near-Pascal
codecs at C849/C812 are reviewed. Codec acceptance does not transfer here.

The real DOS INT 21h protocol is expressed through Borland's hardware register
bindings and `geninterrupt`: encode, open read/write, seek, write the complete
96-byte section, close, decode the in-memory section. The original unchecked
open result remains unchecked. AX open/service, BX handle, CX:DX seek, and
DS:DX/CX transfer parameters are actual DOS interfaces. No local algorithm is
replaced by a physical-register template. The inline seek preserves the original
byte rank addition and its wrap, rather than widening that operation.

Complete score92/section96, resident and character/rank definitions are reused
unchanged. The foreign near filename at DS F5E is `GENSOU.SCR` including its NUL;
`hi` is DS 366E, rank 576F and the byte character 5773. The binder supplies only
actual foreign symbols and outside extents, with no string or score payload.

Pinned ReC98 `th05/main/hiscore.cpp` and maintained TH04
`src/main/score/ranking.cpp` were consulted. The normal C++ DOS save is retained;
reference barrier/register-driven score sorting and LOOP/copy algorithms are not
imported. TH04's checked general file API is not substituted for TH05's behavior.

Two fresh direct TCC/OMF/MAP/TLINK producers match all 55 bytes and the original
empty relocation order. The shared inline seek-origin zero-to-one DOS mutation
is rejected. Receipt:
`.analysis/unit-replays/main-score-current-save-a/receipt.json`, SHA-256
`91939289af4e319dff58f82691de58d59c6f2a33dbb6adc36a6a41398d0cfc14`.
Native/source/ABI review: `.analysis/score-current-native-review.json`, SHA-256
`57cd46f7bd4afa27fcf31a0634f72fdb2e16beb5c8b82938bd47f862ee12f716`.
New credit is one complete function / 55 C++ instruction bytes. All old accepted
records and dependencies remain unchanged, so no old owner is rebuilt.

The adjacent original loader `C882..C8B9` is 55 bytes / 23 instructions. Both
ordinary early-return and explicit if/else C++ spellings emit 54: TCC merges its
failure RET with the final RET, changing native `JNC / RET` into a jump to the
end. The remaining DOS body matches after that shift.
No artificial barrier, filler, second positive or negative is added for those
known failed profiles. `current.cpp` retains the complete natural two-function
context; its combined 109-byte producer remains unaccepted. Shared canonical
`.inl` bodies avoid copied implementations.

## Exact standalone load

The failure is caused by jump folding. `current_load.cpp` uses the pinned
compiler's source `-O-` pragma with the ordinary early-return body. This emits
the native `JNC / RET` and final RET naturally, recovering all 55 bytes / 23
instructions without changing the DOS algorithm or types. Original historical
compiler options remain unknown; this is an actual exact reconstruction profile,
not proof of those original options. There are no padding, table, DATA, BSS or
MZ relocations. The genuine no-argument near ABI remains unchanged.

Two fresh direct TCC/OMF/MAP/TLINK producers pass the complete load scope and
original empty relocation order. The 96-to-95-byte read-count negative is
rejected, retaining the original extent and empty fixups. Receipt:
`.analysis/unit-replays/main-score-current-load-a/receipt.json`, SHA-256
`10564f87144548f90952b0596312e1856830d879ae2e6ca011e91c5ae53c3605`.
Native/source/profile review: `.analysis/score-current-load-native-review.json`,
SHA-256 `6d337f8c4bc3efd73187a87529fde9d54a636f9c7c22a172b18185a2e7e4d13f`.
New credit is one function / 55 C++ instruction bytes. The earlier save body,
header, seek helper, acceptance record and all other accepted dependencies are
unchanged; no old owner is rebuilt. Together the two independently accepted
functions cover all 110 original bytes, with their own genuine source profiles.

Target provenance remains candidate-local-attested; no packed-file or whole-game
claim follows. No producer tool or behavior model changes.

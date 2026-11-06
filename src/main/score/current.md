# Current score file: exact C++ save, pending load

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
end. The remaining DOS body matches after that shift. These first diagnostics
are retained in `.analysis/native-producers/main-score-current-a/` and `-b/`.
No artificial barrier, filler, second positive or negative is added for that
known failure. `current.cpp` retains the complete natural two-function context;
only `current_save.cpp` is accepted. Shared canonical `.inl` bodies avoid copied
implementations. The loader remains unaccepted, with zero authored credit.

Target provenance remains candidate-local-attested; no packed-file or whole-game
claim follows. No producer tool or behavior model changes.

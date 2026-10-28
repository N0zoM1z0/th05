# Complete shared Mai/Yuki update: accepted final-pattern context

MAIN `[17FDB,183D5)` is one complete 1,018-byte far Pascal callback:
993 instruction bytes, one checked zero at relative 993, and two compiler
switch tables totaling 24 bytes at relative 994. Native review rereads all
282 instructions, complete returns, direct branches and the six case values
and destinations. The values are 0/1/2/253/254/255. No instruction NOP exists.
Original ordered MZ fixups are `[942,931,915,898,874,723,312,171,123]`.

The standalone source's earlier 1,017-byte failure remains archived.
`update_context.cpp` retains its callback body byte-for-byte, preceded by the
ten genuine adjacent final-pattern bodies from the unchanged canonical
`remaining_patterns.inl`. Those 939 bytes were already accepted separately.
The resulting complete compiler contribution is `[17C30,183D5)`, 1,957 bytes.
It naturally emits the original zero and keeps all nine updater segment
fixups inside its second LEDATA record. This establishes an exact maintained
source context; the literal historical translation-unit boundary is unproved.

The updater preserves both Boss objects, shared homing and movement, pattern
selection, HP gates, damage/timeout defeat selection, explosion and shake
phases, survivor dialog/BGM loading and the actual far survivor-update
pointers. Canonical Boss24, Laser24, custom26, gather14, bullet and dialog
types and the near callback arrays remain unchanged. Storage, assets and
foreign implementations receive no credit. The first real MAIN01 callback
declarations still precede transitively included stage declarations.

The symbol-only binder retains MAIN03=1527, MAIN01=AE1, SHARED=14AB and
DS=209D. Even empty foreign compiler segments stay in their real groups.
Every hole lies outside the entire 1,957-byte source contribution; the
independent paragraph tail begins at 183E0. There is no emitted helper code,
inside hole, initialized storage, stack, source padding, opcode body or
supplied switch-table payload.

Both fresh producers emit ordinary CRC-valid OMF with LEDATA ranges
0..1020 and 1020..1957. Their normalized object identities, whole scaffold
MZ files and MAPs agree. The entire contribution also matches native raw
CODE, but only the complete updater receives new acceptance. Its raw hash
is `501bb630b4a814971feaa87dc117aa86c9f2c3acc151ac62c2b30786f26d5384`.
The own compiled negative changes the combined-HP gate 5500 to 5501,
differs only at relative 509 and is rejected with extent, zero, tables and
ordered fixups unchanged. Actual source snapshots, compiler arguments,
link response, logs, OMF and MAP/frame evidence were reread before import.

Receipt `.analysis/unit-replays/main-mai-yuki-update-context-a/receipt.json`,
SHA-256 `7266d6778d95b7448f1be6fe8d9cb4cbc545967b443d086868fe8523080b4b14`.
Native review `.analysis/mai-yuki-update-context-native-review.json`;
actual producer/source review `.analysis/mai-yuki-update-context-root-review.json`,
SHA-256 `0c7abe509a8a9e26a85b602028a1e1e59ce5f0be4f33a9484b84db8caf9f424b`.

New credit is one complete function and 1,017 authored CODE bytes:
993 instructions plus 24 compiler-table bytes. The zero gets none and the
939-byte prefix is not counted twice. All earlier accepted records, source,
headers and controls stay unchanged; installed execution probes and accepted
objects were reused after dependency checks. No DATA, ASM, packed-container
or whole-game equality is claimed.

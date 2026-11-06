# Exact BB text-mask lifecycle

The two complete MAIN procedures at `E4B6..E519` are load 76 and release 23:
99 instruction bytes / 37 instructions, with no padding, table, initialized
DATA or BSS. The following NOP at E519 is foreign and receives no credit.
CS is main_01/0AE1, DS 209D; original ordered MZ fixups are `[6,90]`.

The source follows maintained TH04 `src/main/formats/bb_txt.cpp` loading flow,
with TH05's independently reviewed direct DOS operations. TH04 uses two
separate const filenames; TH05 mutates one real filename between the reads. A 3072-byte segment
receives 2048 bytes from the current filename at offset 0, then 1024 bytes from
the second file at offset 2048. The mutable filename's fourth byte is assigned
'2' between reads; it is not reset for repeated calls. The old allocation is
not freed before a new load. All I/O and allocation results remain unchecked.
Release preserves the original segment test, real far free and zero store.

Allocation, field updates, capacities and release are ordinary C++. The real
DOS DS:DX interface uses Borland register intrinsics plus PUSH/POP DS transport;
there is no register arithmetic kernel, emitted opcode or ASM function body.
The allocator is the actual far Pascal WORD-size API at 0000:281A, returning
a two-byte segmented pointer; free is at 0000:291E. Both callers are near Pascal,
no-argument void functions. The 8-byte filename at DS 18C0 and segment handle at
DS 19B0 remain foreign. No file content, filename initializer or asset is copied.

The first direct-object diagnostic reproduces all 99 raw bytes but emits fixups
`[90,6]`. The explicit `tcc-s-tasm32` recipe compiles unchanged C++, then
assembles the unedited compiler output. It recovers the original `[6,90]`.
The empty foreign CODE-context wrapper contains no instructions or data.
Two fresh deterministic chains pass complete ordinary OMF/MAP, all raw bytes,
original order and the normal second-filename 2-to-3 compiled negative. The
recipe and all accepted dependencies are unchanged, so no old unit is replayed.
This accepts 99 authored C++ instruction bytes and two function occurrences,
without a claim about literal historical source or whole EXE placement.

Native boundary/source/ABI review:
`.analysis/bb-text-lifecycle-native-source-review.json`, SHA-256
`71db99e969e790dcf1854382df6ad18f741debdbf6920ff914ce8fabfd38e7df`.
Receipt: `.analysis/unit-replays/main-bb-text-lifecycle-compiler-assembly-b/receipt.json`,
SHA-256 `33bb73826ce3fcd35602da0013d3736667d1bfba8cae547b425578a28e99f5ba`.
The earlier direct diagnostic is `.analysis/native-producers/main-bb-text-lifecycle-a/`.
No CPU model, exhaustive input sweep or whole-game test is required or run.

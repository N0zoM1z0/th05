# MAP loader

The complete compiler contribution at MAIN E5C2..E606 contains 68 instruction
bytes, ending at RET E605. It has no table, padding, owned DATA or BSS. Its
single original ordered MZ fixup is relative 41, at the far allocation call.
The following accepted 23-byte `map_free()` remains an external provider.

The maintained TH04 `src/main/formats/map.cpp` supplies the MAP format and
loading flow, corroborated by ReC98 b6ba5b0a th04/formats/map.hpp. TH05 frees
the old segment first, selects the filename with its byte stage ID, and uses
direct DOS open/read/close operations. It reads the complete eight-byte header,
allocates the header's unsigned byte size, then reads that many bytes into the
allocated segment. All DOS/allocation results remain unchecked.

The canonical MAP header and full 320-byte section type are imported unchanged
from map_free.hpp. The foreign filename is the nine-byte mutable `st00.map`
buffer at DS18C8; header DS41EA, segment handle DS4AD8 and stage ID DS576E are
also external. No filename bytes, header storage or sections are supplied by
this producer. Near C++ `map_load()` takes no arguments and preserves SI;
the DOS destination segment switch saves and restores DS explicitly.

The actual far Pascal allocator at 0000:281A takes one unsigned WORD and
returns its two-byte segment result in AX. The source stores that full result
in the canonical segment pointer, then consumes the still-live AX through the
DOS intrinsic interface. Intervening BX/CX argument setup does not modify AX.
No return type, pointer width or declaration is changed to obtain the bytes.

The initial single-producer diagnostic emitted 70 bytes because assigning DS
from stored `map_seg` reloaded memory instead of using the actual AX result.
That failed diagnostic remains at
`.analysis/native-producers/main-map-load-a/native-diagnostic.json`.
The corrected ordinary source passes two fresh normal replay producers, valid
OMF/MAP placement at CS AE1 and DS209D, all 68 raw bytes and ordered fixup `[41]`.
The compiled filename-character mutation is rejected. Unchanged accepted
dependencies and installed tool probes are reused after identity checks;
no additional behavior model, full CI or whole accepted-set replay was run.

Native boundary/ABI review: `.analysis/map-load-native-review.json`, SHA-256
`6fa03ef64c08b5948b636b344f1449f7da87e8edba4e63b0ac0fdd513c2f4474`.
Extent SHA-256:
`9ac68bd35e2a1f758c1cff9bf8a9ba339361787f86b2543d1ae7c88609ab9b3c`.
Receipt: `.analysis/unit-replays/main-map-load-exact/receipt.json`, SHA-256
`022497f138a594b02c8e3d2349be0be32b1b44da5289c8048d7c10c5359ab307`.

Acceptance adds one complete C++ function and 68 instruction bytes only.
Literal historical source and whole-executable exactness remain unproved.

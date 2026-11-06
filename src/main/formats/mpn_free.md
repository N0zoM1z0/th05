# MPN release: exact C++

MAIN `420E..4225` is the complete 23-byte far Pascal, parameterless release
function in ungrouped `_TEXT`, CS `0000`, DS `209D`. It tests the actual
two-byte segment handle at DS `3068`, passes it to far Pascal `HMEM_FREE`
at `0000:291E`, clears the handle and returns with RETF. The full image type
contains four 16-row word planes (128 bytes), rather than an opaque shortened
record or a four-byte far-pointer substitute.

The natural guard/release/clear flow follows maintained TH04's MPN release
source, with TH05's single bank replacing TH04's slot selection. Initial `-k-`
expresses the native frameless contract. Keeping the allocator in the actual
same `_TEXT` segment lets TLINK perform its ordinary far-call relaxation:
the NOP at offset 11 is compared and earns zero authored credit. There are no
MZ fixups. The independent NOP at `4225` remains outside the function.

Two fresh direct C++ producers match valid ordinary OMF, the whole MAP
contribution, all 23 raw bytes and the original empty relocation stream.
The normal replay shares the BB loader's compiled read-length negative.
Credit is one complete function and 22 authored instruction bytes. No DATA,
BSS, neighboring loader/renderer or whole-executable claim is added.

Receipt: `.analysis/unit-replays/main-bb-cheeto-and-mpn-free-a/receipt.json`,
SHA-256 `4b6107cabf53d354a6ee588dd6d74bcdc745ac199395902b732d0c8b80d9dda3`.
Complete boundary/source/ABI review:
`.analysis/bb-cheeto-and-mpn-free-native-review.json`, SHA-256
`ff50ba17c8e0e829d56d6760df50a7c541ae3a08f979238364f42281629abd9d`.
No existing accepted dependency or build tool changed. The 92-byte raw-DOS
MPN loader and 69-byte upload function remain unaccepted; this release result
does not resolve either one's source or producer context.

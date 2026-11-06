# Curved-bullet bitmap load: exact C++

The complete near Pascal function at MAIN `DE58..DE71` is 25 instruction
bytes, with no padding, tables or MZ fixups. The following `DE71` NOP and
the independent renderer beginning at `DE72` remain outside this owner.
CS is `AE1` / `main_01`; DS is `209D`. The foreign eight-byte `LS00.BB`
filename is at DS `149B`, and the resident 2048-byte mask bank at DS `378A`.
Neither resource receives DATA or BSS credit.

Ordinary Borland interrupt intrinsics express the same unchecked DOS
open/read/close flow as the accepted text-mask loader. The real DOS register
interface needs no inline assembly here. Full .BB size and segment types come
from the unchanged shared header. ReC98 `th05/formats/bb_cheeto.asm` supplies
candidate semantics; its listing is not copied as authored assembly.

Two fresh direct C++ producers match the complete 25-byte OMF/MAP contribution,
all raw bytes and original empty fixup stream. Their shared compiled control
changes the read length from 2048 to 2047 and is rejected. The diagnostic's
initial DOS wrapper name exceeded 8.3 and failed before compilation; correcting
only that filename allowed the first actual producer to match.

Receipt: `.analysis/unit-replays/main-bb-cheeto-and-mpn-free-a/receipt.json`,
SHA-256 `4b6107cabf53d354a6ee588dd6d74bcdc745ac199395902b732d0c8b80d9dda3`.
Complete boundary/source/ABI review:
`.analysis/bb-cheeto-and-mpn-free-native-review.json`, SHA-256
`ff50ba17c8e0e829d56d6760df50a7c541ae3a08f979238364f42281629abd9d`.
Target provenance remains candidate-local-attested. No existing accepted
dependency, compiler recipe or execution probe changed or required replay.

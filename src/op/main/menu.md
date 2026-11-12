# OP startup and menu reconstruction

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/op/start.cpp`,
`th04/op/start.hpp` and `th04/op/m_main.cpp` with GAME=5. The owner keeps the
TH05 character/demo behavior, all menu branches and semantic switches, sound
reload behavior and original hardware wrappers. The complete existing 128-byte
TH05 resident declaration is reused; no alternate resident type is introduced.

Canonical files are **UTF-8**. Build this owner with explicit
**`source_encoding = 'cp932'`** staging, including `strings.hpp`. Its readable
Japanese descriptions, error text and archive filename must become CP932 bytes
for the pinned compiler. All 26 description strings independently match the
original CP932-decoded text, including fullwidth and ASCII spacing. No opaque
byte arrays, target-derived strings, ASM, emit, fake linker symbols or barriers
are supplied. Large-model `execl` variadic terminators retain the original
four-byte `0UL` sentinel.

## Artifact and complete code boundaries

Packed OP target SHA-256:
`c94efc071a4b1adf8ce6e2c5a7eefb9eb47c26f8bab61b2e58e736dda8130abb`.
This owner uses the independently observed DIET payload, **77,798 bytes**,
SHA-256 `7c112a4a7dc4231e9be2d0f69555f0736f69165c80621a3fcd67324dad77ec47`.
Addresses below are offsets in that decoded load module. They are not offsets
in the packed EXE, and this work makes no packed-container reconstruction claim.

The full original contribution is **`[A39C,B077)`**, **3291 bytes**.

| Function | Half-open decoded span | Instructions | CODE-data | Padding |
| --- | --- | ---: | ---: | ---: |
| `start_game` | `A39C..A447` | 171 | 0 | 0 |
| `start_extra` | `A447..A4CF` | 136 | 0 | 0 |
| `start_demo` | `A4CF..A5F6` | 285 | 10 | 0 |
| `main_unput_and_put` | `A5F6..A717` | 277 | 12 | 0 |
| `option_unput_and_put` | `A717..A968` | 576 | 16 | 1 |
| `menu_sel_update_and_render` | `A968..A9D6` | 110 | 0 | 0 |
| `main_update_and_render` | `A9D6..ABCF` | 493 | 12 | 0 |
| `option_update_and_render` | `ABCF..AF49` | 866 | 24 | 0 |
| `main` | `AF49..B077` | 302 | 0 | 0 |

Each original function decodes contiguously through its true return. There are
**3216 instruction bytes +74 semantic switch-table bytes +1 zero alignment
byte**. Potential authored code credit is **3290**, subject to full cold replay.
All 133 local branch destinations are instruction starts.

| Switch owner | Original table span | Unit-relative span | Entries |
| --- | --- | --- | ---: |
| `start_demo` | `A5EC..A5F6` | `250..25A` | 5 |
| `main_unput_and_put` | `A70B..A717` | `36F..37B` | 6 |
| `option_unput_and_put` | `A958..A968` | `5BC..5CC` | 8 |
| `main_update_and_render` | `ABC3..ABCF` | `827..833` | 6 |
| `option_update_and_render`, left | `AF31..AF3D` | `B95..BA1` | 6 |
| `option_update_and_render`, right | `AF3D..AF49` | `BA1..BAD` | 6 |

All **37** address words land on instruction starts in their own function.
The source contains only the semantic switches. The zero alignment byte at
`A957`, unit-relative `5BB`, remains in full comparison but receives no credit.
The code has **99 ordered original MZ segment fixups** from the decoded view;
none may be normalized or masked.

## Real ABI, owned state and bindings

Wrapper `th05/op_main.cpp` should include `src/op/main/menu.cpp`. Use the OP
build context (`BINARY='O'`), `OP_MAIN_TEXT` / `op_01`, and the retained source
`-a2` at its original point after the three startup functions. Original op_01
frame is **`0A39`**, load base **`A390`**, contribution group offset **`000C`**;
DGROUP frame is **`0EFE`**. This frame also owns menu callback near pointers.

The menu callback is a genuine two-byte near Pascal pointer with two word
arguments. `menu_sel` and navigation arguments preserve the original `int8_t`
alias **char**, including its Borland mangling. Rank, CDG slot, text-effect and
SE mode enums retain their full original 16-bit domains; BGM mode and character
enums retain their forced 8-bit domains. The header asserts these widths and
four-byte far string pointers. Rendering/sound/system interfaces preserve
their real near/far, C/C++, Pascal/C cleanup and return types.

Initialized compiler-owned DATA is **DGROUP `[0090,04D1)`**, **1089 bytes**,
SHA-256 `8db0fc0a3afb106f39af6b6fb6ce56d049c904a0e32b50531b8f99ea5fb3cb17`:
six real initialized flag bytes, 26 real far description pointers (**104
bytes**) and 33 natural terminated Japanese/filename/error strings (**979
bytes**). There is no padding in this DATA extent. Its 26 pointer segment
words have ordered original MZ fixups with frame `0EFE`.

The source owns `unused`, `menu_sel`, `quit`, `main_menu_unused_1`, `MENU_DESC`
and the two static initialized flags. Uninitialized objects occupy DGROUP
`[2DEC,2DF6)`: resident far pointer at `2DEC` (4), `in_option` at `2DF0` (1),
one alignment byte at `2DF1`, callback at `2DF2` (2), and two static input flags
at `2DF4/2DF5` (1 each). Do not duplicate these definitions in a symbol-only
scaffold. BSS and DATA ownership are separate from authored code credit.

External data is `_extra_unlocked` at `5136` (1), `_extra_playable_with` at
`513F` (4), `_key_det` at `3A92` (2), `_mem_assign_paras` at `09EC` (2),
`_graph_putsa_fx_func` at `09DE` (2) and `_PaletteTone` at `054E` (2).

Private `.analysis/op-main-boundary-review.json` contains all 12 near and 30
far external destinations, original frames and call sites, exact calibration
EXTDEF spellings, source-owned object anchors, every semantic string, complete
table targets and code/DATA fixups. Numeric positions come from original
payload operands; calibration symbols and equality are diagnostic only.

A natural negative control changes the unique `if(idle_frame >= 640)` threshold
to 639, changing actual attract-mode timing. Another can change a readable
Japanese description and must be rejected by DATA comparison. Source-current
focused cold raw/fixup replay is recorded in the acceptance section below.

## Focused acceptance

`.analysis/unit-replays/op-main-menu-b` contains two isolated producers with
actual UTF8-to-CP932 staging. All 3,291 code bytes and 99 ordered code fixups
match; the compiled idle-time change from 640 to 639 is rejected. Six semantic
switch tables supply 74 bytes, reported separately from 3,216 instructions.
The one checked zero alignment byte receives no authored credit.

The complete compiler DATA contribution independently matches all 1,089 bytes
and 26 ordered fixups in both producers. This is a separate retained observation
with no additional progress credit. The 26 far string pointers and readable
Japanese text are generated by maintained C++; no target data array is supplied.
The canonical UTF8 strings header and actual CP932 compiler input have distinct
recorded digests, and acceptance reconstructs and checks the latter.

The symbol-only context omits artificial stack allocation. Adding an 80h-byte
STACK member to DGROUP would align and shift actual BSS by 84h, changing its
references throughout the code. The accepted context lets the compiler's whole
10-byte BSS contribution occupy original offsets `[2DEC,2DF6)` instead. BSS
placement is verified; uninitialized memory values are not counted as authored
file-backed data. Complete packed OP equality remains unaccepted.

## Accepted initialized semantic DATA

`op-main-data-a` now accepts the complete initialized DATA contribution
`[F070,F4B1)`: 1,089 bytes, 26 ordered segment fixups, zero functions and no
padding. Its six initialized flag bytes, 104 bytes of far description pointers
and 979 readable string bytes are generated by maintained semantic source.
The original two complete LEDATA records have no hole or overlap. Both fresh
CP932-staged producers pass; changing the actual background filename from
`op1.pi` to `op2.pi` in the canonical strings header changes DATA and is rejected.
No image content, BSS or duplicate CODE credit is included.

## Natural OP launch, Extra and attract-mode Resident contract (2026-11-12)

The full original OP main menu's **3,291-byte / nine-function** CODE
contribution now names its launch and attract-mode state in
`launch_sequence_rules.hpp`, with *no* newly allocated Resident, BSS or
DATA object. The standard start initializes stage zero, clears the demo
flag and preserves configured starting lives and bombs; the Extra start
uses its original **three lives / three bombs** and disables debug launch.
All score resets continue to zero out exactly the original eight-digit
scores in the canonical 128-byte resident, with the actual DOS `execl`
far-argument terminating word and normal debug-versus-MAIN routing.

The original Demo rotation cycles **1–4** through Reimu stage 3,
Marisa stage 1, Mima stage 2 and Yuuka stage 4. Holding Left+Right
selects the hidden **Demo 5** Extra Stage clear only when all four
original `extra_playable_with[]` unlock flags are set; otherwise it
sets demo index zero and returns before starting MAIN. The hidden
branch retains the genuine eight-unit BGM fade. None of these conditions
is simplified into a lookup table or replaced with a shorter helper.
The OP entry's attract timer is still exactly **640 frames**, and its
special key handling preserves the simultaneous Left+Right shortcut
without resetting the timer. The four other original menu modes,
selector SE1/SE11, resident setup override, unused palette allocation,
sound reload semantics and the observed first-subsceen palette bug
remain in the same source-level and compiled order.

`menu.cpp` also owns its original **1,089-byte** initialized-DATA
contribution: the 26 near-store far description pointers, all
human-readable CP932 UI strings, state bytes and file names. Therefore
the complete affected CODE **and** DATA were selectively recompiled in
the same native context with two independent pinned Borland producers.
Both whole scopes match all raw bytes, MAP/OMF contributions, 99 ordered
CODE fixups, initialized-DATA pointer fixups and the one checked uncredited
zero. The native compiled negative changes the actual attract timeout
640→639 and is rejected:
`.analysis/unit-replays/gpt-web-op-main-launch-rules-a/receipt.json`.
No existing authored bytes are credited twice; there is no complete OP
cold replay or replacement of any packed executable asset.

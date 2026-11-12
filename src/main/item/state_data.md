# Original MAIN item statistics and attraction state

The accepted native item-reward table ends at MAIN load offset `22848`.
Immediately after it, the original game stores six actual 16-bit mutable
counters and a final byte attraction flag in exactly this order:

| Original DS | Name | Width | Meaning |
| --- | --- | ---: | --- |
| `1E78` | `power_overflow` | 2 | Full-power reward overflow step |
| `1E7A` | `items_spawned` | 2 | Total spawned item objects |
| `1E7C` | `items_collected` | 2 | Total collected item objects |
| `1E7E` | `extend_point_items_collected` | 2 | Point-item extend threshold progress |
| `1E80` | `total_point_items_collected` | 2 | Persistent point-item total |
| `1E82` | `total_max_valued_point_items_collected` | 2 | Full-value point-item total |
| `1E84` | `items_pull_to_player` | 1 | Active attraction flag |

These types, names and initial zero values are explicitly present in pinned
ReC98 `th04/main/item/items[data].asm` under `GAME=5`, including its exact
`EVEN` directive after the final byte. The supplied TH05 executable's
independently accepted item collection, spawning, extend, process-handoff,
HUD and bomb control code references the same seven DS addresses. The 1-byte
alignment at `22855` is **not** included in this source or its credit, and
remains unknown; the separately accepted item-miss velocity table starts at
`22856`.

`state_data.cpp` naturally declares the six counters as real signed/unsigned
16-bit words and `items_pull_to_player` as the canonical `bool` alias
(`unsigned char`). Its `_DATA` contribution is exactly **13 bytes** at
`[22848,22855)`. The initial C++ producer could not compile `bool` without
the actual typedef; including the lightweight existing resident ABI recovered
the correct original type without importing unrelated CODE storage.

The strict receipt
`.analysis/unit-replays/gpt-web-main-item-native-state-c/receipt.json`
has two distinct Turbo C++/TLINK positive producers, complete OMF/MAP/byte
identity and the empty original ordered fixup stream. A compiled negative
changes `items_pull_to_player` from `false` to `true` and is rejected. This
adds **13 authored semantic C++ DATA bytes** and no new instructions. The
original source language of the historical initializer is not inferred; the
maintained C++ declarations are a semantic alternative to the referenced
handwritten table.

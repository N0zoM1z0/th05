# Original MAIN enemy lifetime statistics: exact C++ initialized DATA

`enemies_gone` and `enemies_killed` are consecutive 16-bit counters in the
original MAIN DGROUP. The first counts enemy objects retired by the VM and
update controller; the second records kills in the same controller. The
accepted process handoff reads both words and stores them into their verified
resident statistics fields, rather than an incidental zero-initialized buffer.

| Counter | Original DS offset | Original load-module extent | Initial value |
| --- | --- | --- | --- |
| `enemies_gone` | `14A4` | `21E74..21E76` | 0 |
| `enemies_killed` | `14A6` | `21E76..21E78` | 0 |

These are backed by the actual native `INC word ptr [14A4]` at MAIN `153B3`
(enemy VM), `16D18`/`16D1C` (enemy update), and `MOV AX,[14A4]` /
`MOV AX,[14A6]` at `CEFF`/`CF06` (handoff). The accepted `resident_t`
layout has corresponding 16-bit fields; the initial state is intentionally
separate from the resident file's later values. The preceding 1 byte at
`21E73` and following 2 bytes at `21E78..21E7A` remain unclassified.

`lifetime_totals_data.cpp` declares the actual two mutable 16-bit words as
normal C++ scalar initializers. The focused receipt
`.analysis/unit-replays/gpt-web-main-enemy-lifetime-totals-a/receipt.json`
verifies one complete 4-byte `_DATA` Borland 4.02 contribution, actual MAP
position, all original bytes and empty ordered MZ relocation stream with two
independent compiler/linker producers. An independently compiled mutation of
`enemies_killed = 0` to `1` fails exact comparison. This accepts 4 original
initialized semantic DATA bytes without reopening the accepted multi-hundred
byte enemy controller or process-handoff functions. The original historical
translation-unit boundary is not claimed.

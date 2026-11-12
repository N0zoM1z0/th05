# Initial DOS memory-assignment budget in TH05

The original `th05/mem[data].asm` defines a single initialized 16-bit word:
`_mem_assign_paras dw (320000 shr 4)`. It is **20,000 paragraphs** (`4E20h`),
representing a default 320,000-byte memory allowance before game-specific
startup code may change it. The exact word is immediately before the accepted
sound-extension bank in MAIN and MAINE, but not in OP. It is not sound DATA.

`mem_assign_initial.c` expresses the original arithmetic and original C-linkage
word type. Existing accepted MAIN entry, OP menu and MAINE entry functions
reference the mutable `mem_assign_paras` object and subsequently assign their
own budgets; no additional initializer, storage or runtime handler is proposed.

| Artifact | Original DS frame and word offset | Complete initialized DATA extent |
| --- | --- | --- |
| MAIN | `209D:0824` | `211F4..211F6` |
| OP decoded | `0EFE:09EC` | `F9CC..F9CE` |
| MAINE decoded | `1011:06CA` | `107DA..107DC` |

Focused receipts:

- `.analysis/unit-replays/gpt-web-main-mem-assign-initial-a/receipt.json`
- `.analysis/unit-replays/gpt-web-op-mem-assign-initial-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-mem-assign-initial-a/receipt.json`

Each scope independently has two actual TCC/TLINK producers, a complete
2-byte ordinary `_DATA` LEDATA, original MAP/byte/empty MZ relocation
agreement and a **rejected compiled negative** changing the allocation budget
by one paragraph to 320,016 bytes. Together they add **six game-authored C
initialized DATA bytes** and zero instructions, without double-counting memory
assignment routines or nearby foreign state. The OP gap surrounding the word
remains explicitly unknown. These are exact compiled source contributions,
not proof of historical translation-unit order or a whole-build replay.

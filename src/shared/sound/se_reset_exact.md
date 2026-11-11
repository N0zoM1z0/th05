# Exact SE reset in all three TH05 executables

`void far snd_se_reset()` resets `snd_se_frame` to zero and selects
`SE_NONE` in `snd_se_playing`. Its unchanged C++ source and two-byte globals
produce one complete 11-byte function in each decoded executable:

| Artifact | Exact function | Following uncredited alignment |
| --- | --- | --- |
| MAIN | `14CD6..14CE1` | `14CE1` |
| OP | `D5F6..D601` | `D601` |
| MAINE | `EADA..EAE5` | `EAE5` |

The function is retained as natural code in pinned ReC98
`th02/snd/se_reset.cpp`. The existing canonical [sound state types](se.hpp)
and the distinct accepted SE play/update implementations remain unchanged.
No original relocation or initialized DATA belongs to this source.

Focused receipts:

- `.analysis/unit-replays/gpt-web-main-snd-se-reset-a/receipt.json`
- `.analysis/unit-replays/gpt-web-op-snd-se-reset-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-snd-se-reset-a/receipt.json`

Each has two independent direct Borland/TLINK producers, complete byte and
empty ordered-fixup equality, and a rejected compiled mutation from `SE_NONE`
to zero. The three independent segment/DGROUP binders supply only foreign
addresses. There was no full cold replay.

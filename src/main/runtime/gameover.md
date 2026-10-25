# Game-over animation and continue menu

This natural C++ owner adapts the maintained TH04 reconstruction's
`src/main/core/gameover.cpp` to independently reviewed TH05 behavior. It is
accepted by focused replay below. The ReC98 `th05_main.asm` routines `sub_F896`,
`sub_F906`, `sub_F976` and `sub_FAA3` supply semantic corroboration; the
original pinned MAIN image determines every boundary and operand.

| Function | Original load extent | Size |
| --- | --- | ---: |
| `gameover_fade_in()` | `D77C..D7EC` | 112 |
| `gameover_fade_out()` | `D7EC..D85C` | 112 |
| `gameover_run()` | `D85C..D989` | 301 |
| `gameover_continue_menu()` | `D989..DAE1` | 344 |

All four functions are near cdecl calls with unsigned byte AL results. Each
ends at its actual RET followed immediately by the next function. The complete
869-byte cohort has no switch tables, undecoded gaps, owned initialized DATA
or BSS. Twenty-seven original relocation sites retain their actual order.

Native instruction review finds exactly four NOPs, at cohort offsets 515, 834,
839 and 844. Each belongs to an original five-byte same-CS far-call sequence:
GameExecl, shot-level update, lives display and bombs display. Their genuine
far signatures remain intact; explicit same-code-segment declarations express
the observed CS `0AE1`. These four bytes are checked padding with no authored
credit, so a future complete match could credit 865 bytes. Every byte still
undergoes ordinary raw comparison.

TH05 has no TH04 stage-five bad-ending conditional at the start of this
runner. Its continue loop calls `input_reset_sense_held()` once at the top of
each iteration. A successful continue sets `dream` to 1 and copies the full
128-byte resident's credit settings to MAIN's separate remaining-life and
bomb globals. The score's first digit and `continues_used` physically alias
at DS:`3702`; this owner declares only the observed byte access. All gaiji,
erase strings, filename data, palettes and state remain foreign definitions.

The independent symbol-only binder fixes main group `0AE1`, shared frame
`14AB`, and DS `209D`, using only holes outside the complete compiler-owned
contribution. It provides no foreign instructions, literal values or stack.
The genuine `GameExecl(const char far *)` Pascal far interface is retained,
including its four-byte argument.

Private `.analysis/gameover-boundary-review.json` records full function
boundaries, hashes, all calls/branches, NOPs, ordered fixups, actual globals,
ABI and five-file source closure. `.analysis/gameover-candidate.json` proposes
one whole contribution and a unique compiled negative changing the available
credit formula from `3 - continues_used` to `2 - continues_used`. Two fresh
focused producers and that independent negative were required for acceptance. The unchanged
existing accepted owners need no replay.

Focused receipt `main-gameover-a/receipt.json` passes both fresh producers for
the complete 869-byte contribution, including all 27 original ordered fixups.
Its independently compiled credit-formula mutation from 3 to 2 is rejected.
The root imported all four complete functions and 865 authored instruction
bytes; the four explicitly checked native NOPs receive no credit. CPP, header
and binder are frozen accepted inputs. No additional per-function negative
compilations are claimed: this is one whole-contribution control owner.

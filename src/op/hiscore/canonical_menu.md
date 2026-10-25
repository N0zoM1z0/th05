# Canonical high-score menu and filename ownership

This canonical source factor accepts the complete312-byte menu without changing
the existing shared ABI headers. Development and fresh verification took place
in an isolated worktree. The root copied the frozen source changes and imported
all three passing receipts atomically, after the affected owners were verified.

The original menu occupies decoded OP `CC5C..CD94`, near cdecl, with no native
NOPs or compiler tables. Its 26 far relocations form one descending ordered
run. Both retained 1,411-byte view producers and the reference calibration
split LEDATA at offset1,023, inside menu offset133, so that complete menu stays
strictly order-inexact despite raw equality. A standalone real 312-byte CODE
contribution can plausibly fit one record; no artificial prefix, record edit
or compiler option is used to force that outcome.

`regist_view_menu.inl` is the one maintained natural function definition,
included at the same position in the original view context and in the new
standalone `menu.cpp`. Its only semantic-reference changes replace four
filename expressions with fields of the actual resource object. All control
flow, the duplicate input test, actual near calls and true far APIs remain.
Inverse-expression mapping restores the previous body verbatim. The old view
context's menu stays unaccepted; only its seven existing complete CODE scopes
are selected there. This is bounded producer validation, with no claim that
both overlapping context objects compose a whole executable unmodified.

The menu's four filename literals originally occupy23 bytes starting at odd
DS:`2823`. A new word-aligned compiler DATA contribution cannot honestly start
there by itself. `files.cpp` instead owns the existing complete53-byte pool at
DS:`2818..284D`, using seven readable, named char-array fields with actual
lengths and offsets. The externally linked const near object contains only
filenames/song names, not game images, fonts or score payload. The two CODE
TUs reference this single real owner and emit no duplicate string pool.

The frozen `view.hpp`, OP menu header and shared string header stay unchanged;
MAINE score-end also depends on `view.hpp`. The new resource header is included
only from the actual OP CPPs. Filename and font uses in `view.cpp` reference
their named resource fields locally. The old view still owns its full actual
215-byte BSS. Symbol-only binders declare the foreign resource/BSS addresses
and leave every origin hole outside complete owned extents.

Necessary focused replay is limited to seven existing CODE records, the
existing53-byte DATA record with its new true producer, and new menu312.
Three actual TUs each require two fresh producers and their own compiled
negative: original place-padding8→7, resource filename `scnum.bft`→`scnum.bfu`,
and the menu's final key-release inequality reversed. Old seven entry hashes
are unchanged; their source/binding evidence must be replaced honestly.
The DATA unit retains its ID and byte extent, so it adds no numerator bytes.
Import all replacements atomically after all gates pass; no whole OP or
unrelated artifact replay is needed.

First-producer checks must verify original CODE extents, DATA53 with no
padding/fixups and genuine public const linkage, absent CODE-owned DATA, and
all actual BSS/group anchors. A source-factor hypothesis is not exactness.
Private `op-score-canonical-ready.json`, the inverse-factor proof and native
call/resource plan pin these expectations and confirm the main workspace was
not edited.

All three focused receipts pass and are now imported:

- `op-score-code-canonical-a/receipt.json` replaces the seven existing complete
  CODE records, totaling1,099 bytes, using two fresh view-context producers.
  Those seven scopes share one actual compiled place-padding8→7 negative owner;
  seven separate negative compilations are not claimed.
- `op-score-files-canonical-a/receipt.json` replaces the existing53-byte DATA
  record with its real complete resource producer, two fresh DATA builds and
  its own compiled `scnum.bft`→`scnum.bfu` filename negative. Its extent and
  accepted-byte total do not increase.
- `op-score-menu-canonical-a/receipt.json` accepts the new complete312-byte
  menu, two fresh producers, all26 original ordered fixups and its own compiled
  reversed key-release condition.

This family now has eight complete CODE functions:1,411 bytes, comprising1,395
instruction bytes and16 existing compiler-table bytes, plus the separate53
initialized DATA bytes. No NOP/padding or overlapping DATA gains are counted.
Only the eight affected old records and the new menu record were imported;
unrelated OP, MAIN and MAINE owners were not replayed. All source and producer
identities are current, and CPP/header/binders are frozen accepted inputs.

The original `op-hiscore-view-b` mixed receipt remains intact and failed. Its
whole1,411 raw bytes matched, but its menu relocation order did not. The new
standalone context proves that complete function independently; no fixups were
sorted or patched, and no old positive or aggregate verdict was relabelled.

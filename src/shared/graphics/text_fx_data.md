# Text-effect dispatch and state DATA

`text_fx_data.asm` supplies two complete bounded DATA contributions in each of
OP and MAINE: a 28-byte symbolic dispatch bank and two mutable word-sized
defaults (bold effect and signed pixel spacing 16). The original standalone
receipt reports **64 separate ASM DATA bytes** with inferred origin and no
global ownership credit. The subsequent [explicit native assembly review](../../../docs/reconstruction/TEXT_FX_ASM_OWNERSHIP.md)
adopts these semantic DATA scopes together with independently replayed CODE;
the receipt itself remains unchanged. C/C++ counters receive zero credit.
No historical original source file has been recovered.

| Artifact | DS frame | Dispatch extent | Excluded raster resources | State extent | Native consumer CODE, separately reviewed |
| --- | --- | --- | --- | --- | --- |
| OP | 0EFE | F982..F99E | F99E..F9BE | F9BE..F9C2 | D436..D590 |
| MAINE | 1011 | 10790..107AC | 107AC..107CC | 107CC..107D0 | E91A..EA74 |

All extents use decoded load-module offsets and exclusive ends. MAIN has no
corresponding reviewed helper or DATA owner; acceptance does not transfer there.
The candidate-local-attested packed identities and their retained decoded
proofs are checked independently for OP and MAINE.

## Semantics and origin

The first ten words are two five-entry arrays of relative CALL displacements.
Each word is `helper - (call_operand + 2)`, selecting normal, heavy, bold, black
or bold-plus-mask glyph processing. They are not near function-pointer arrays.
The final four words are DS-relative near pointers to four separate 8-byte
raster masks. The assembler source uses only symbolic expressions and resource
addresses. It contains neither a numeric copy of the dispatch payload nor the
32 resource bytes. The two state words follow those excluded resources.

Native static instruction review observes five CS writes: mask operand, both
CALL operands and both spacing immediates. The default calls both reach the
bold helper. OP uses CALL operand offsets 01F5/0247 in CS 0D30; MAINE uses
01D9/022B in CS 0E80. Separate symbol-only includes bind those native contexts.
These EQU bindings supply addresses, not initialized target bytes. The complete
346-byte consumer was reviewed in each artifact, including decoded 90h sites:

| Role | OP | MAINE | Credit in this review |
| --- | --- | --- | ---: |
| Explicit hardware I/O delay NOPs | D4E3, D53B | E9C7, EA1F | 0 |
| EVEN alignment after the renderer | D561 | EA45 | 0 |

The alignment byte is checked native padding, not an authored instruction.
Neither it nor any other consumer CODE is an accepted scope in this DATA replay.
The private native review retains the full instruction boundaries and all five
CS writes; no instruction listing has been promoted to maintained compiler code.

ReC98 at pinned commit `b6ba5b0a529edbb31efdf8c0e939263804f8ee47` supplies the
candidate semantic reference `th04/hardware/grppsafx.asm` and its effect enum.
Its reconstruction commits 75f05c8b/0b084b83 and TU-separation commit 66d83aa1
do not authenticate historical source. Self-modifying operands and their
address-difference tables support an assembly-origin inference. The pinned
273721-byte `masters.lib` (SHA-256
`6be41dbcfcf4504977165ccc44443525a29a01f85a1580e6ad0c620bf802faf6`)
has 640 structurally valid members and no GRAPH_PUTSA_FX/GRPPSAFX/GLYPH_WEIGHT
exports; its ordinary GRAPH_*_PUTS members have no DATA payload. This excludes
that specific library as a direct provider, without proving every historical
vendor origin impossible. The global ownership denominator remains unreviewed.

## Replay and retained evidence

`scripts/replay_text_fx_data.py` and `config/text_fx_data.toml` define a distinct
ASM lane. TASM 5 supplies complete 28-byte and 4-byte DATA SEGDEFs, with complete
nonoverlapping LEDATA coverage and no other initialized source contribution.
The bounded model splits dispatch, foreign raster storage and state; it does
not claim to recover the original translation-unit partition or full linkage.
The binders reserve original foreign ranges without supplying resource values.
OP also reserves the independently accepted foreign Music Room DATA end for
valid MZ allocation, without adding an artificial stack.

The accepted private directory is `.analysis/textfx-data-native/asm-c/`:
two independent fresh producers per artifact, complete raw comparisons and
empty original ordered relocation streams for both scopes. Each artifact has
its own normal-to-heavy dispatch mutation and 16-to17 spacing mutation; the
affected scope fails raw comparison while its neighbor stays exact. The pinned
toolchain execution proof was reused after installed-surface identity checks.
Import re-reads both targets, saved actual source aliases, argv and logs, OMF,
MAP, MZ, public boundaries, DGROUP frames and the complete native review.
`config/text_fx_data_acceptance.json` retains the public result; CI checks source
freshness and the separate classification without private inputs.

The first ASM attempt stopped on an overly narrow MAP module-name parser:
TASM emits `M=tfxdata.asm`, not `M=tfxdata`. It had no accepted receipt. The next
successful diagnostic is retained as `asm-b`; `asm-c` supplies fresh producers
after tightening frame, negative-control and dependency guards. Earlier C++
state-only producers in `.analysis/unit-replays/{op,maine}-text-fx-state-data-a/`
were byte-exact, but were never imported because the original assembly context
cannot justify adding them to the C/C++ origin counters. Those temporary C++
sources are preserved privately, outside the maintained source tree.

```sh
bash scripts/run_heavy.sh python3 scripts/replay_text_fx_data.py \
  --native-review .analysis/textfx-data-native/boundary-review.json \
  --output .analysis/textfx-data-native/NEW_FRESH_DIRECTORY
python3 scripts/replay_text_fx_data.py --accept PATH/receipt.json
python3 scripts/replay_text_fx_data.py --check
```

The complete renderer CODE now has its own independent assembly acceptance and
explicit ownership decision linked above. The global denominator, 98% goal,
full executable layout and packed-file exactness remain unaccepted. No accepted
C/C++ owner changed or needed replay for this work.

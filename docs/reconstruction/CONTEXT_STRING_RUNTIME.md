# Original Borland string runtime in TH05 OP and MAINE

Both OP and MAINE contain the **same six complete CL.LIB OMF CODE
contributions** for `ctor2`, `ctor3` and `strings`: `_TEXT` (96 + 207 + 587
bytes) and `_TEXTC` (233 + 540 + 2,371 bytes), totaling **4,034 bytes per
executable**. The original `strings/_TEXTC` class-method contribution is a
full **2,371-byte** source-linked object, not a snippet or a guessed range.

The real original library LEDATA and unsorted FIXUPP records reconstruct
all twelve complete linked original CODE extents and their **original
ordered MZ relocations**. The native verifier also reconstructs each from
the retained real calibration's MAP and linker frames:

| Context | Original `_TEXTC` extents | Original `_TEXT` extents | New ownership |
| --- | --- | --- | ---: |
| OP | `E394..E47D`, `E47D..E699`, `E699..EFDC` | `9C88..9CE8`, `9CE8..9DB7`, `9DB7..A002` | **3,144 B** |
| MAINE | `F4BE..F5A7`, `F5A7..F7C3`, `F7C3..10106` | `9E64..9EC4`, `9EC4..9F93`, `9F93..A1DE` | **4,034 B** |

OP's three `_TEXT` contributions (**890 bytes**) were already reviewed by
the prior gapless CL.LIB ownership decision. They are reverified but **not
double-adopted**. MAINE has no previously owned contribution among these
six. Thus the new combined coverage is **7,178 actual unknown-to-verified
vendor CODE bytes**, not 8,068.

## Original MAINE linker context

The retained MAINE calibration has three C++ string method entries six
bytes earlier than the original target and `DGROUP` at `10100h`, versus the
original `10110h`. The original method-entry offsets come from actual
linked source-bound call targets and independent matching function
prologues; the DGROUP frame is also established by original `xxas` and
`signal` OMF segment fixups.

The verifier updates real segment contribution positions, CODE public
offsets and DATA-group bindings for the original context before linking
the **unchanged original CL.LIB OMF bytes**. It does not copy target
instructions, normalize MZ relocation order, or credit the six preceding
nonmember bytes. The same source records reconstruct the calibration under
its own frame model.

## Evidence, limitations and validation

- [Native verifier](../../scripts/review_context_string_runtime.py)
- [OP original source proof](../../config/context_string_runtime.op.json)
  and [explicit OP ownership](../../config/reviewed_context_string_runtime.op.json)
- [MAINE original source proof](../../config/context_string_runtime.maine.json)
  and [explicit MAINE ownership](../../config/reviewed_context_string_runtime.maine.json)

The source-identity and linked-scope checks rerun only these six original
OMF contributions per executable. In focused negative trials, changing an
original `strings/_TEXTC` source LEDATA byte was rejected in both OP and
MAINE; changing MAINE's six-byte CODE placement or the original DGROUP frame
was also rejected. The public source-current checks do not need Wine or a
whole-game rebuild:

```sh
python3 scripts/review_context_string_runtime.py --context op --check
python3 scripts/review_context_string_runtime.py --context maine --check
python3 scripts/review_context_string_runtime.py --context op --structural-check
python3 scripts/review_context_string_runtime.py --context maine --structural-check
```

These are **third-party library CODE SEGDEF bytes**, not 7,178 proven CPU
instruction bytes and **not game-authored C++**. Any embedded compiler
metadata, alignment, initialized DATA, BSS, and the unowned surrounding
bytes keep their separate classifications. The global game-authored
denominator remains unmeasured.

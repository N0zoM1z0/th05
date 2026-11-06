# Registration creation and animation: exact C++

The complete adjacent MAINE family at `BD46..C16C` contains two functions:

| Function | Complete extent | Instructions | Compiler table | Uncredited zero |
| --- | --- | ---: | ---: | ---: |
| `glyphball_spawn` | `BD46..BE76` (304) | 295 | 8 | 1 |
| `glyphballs_update` | `BE76..C16C` (758) | 747 | 10 | 1 |

All 376 instructions, returns, direct branches and nine generated table
destinations are reviewed in the pinned decoded target. CS is `A54` / GROUP_01,
DS `1011`. The literal ordered MZ fixups for the complete 1062 bytes are
`[709,534,384,122,114,1034]`. No instruction NOP, DATA, BSS or resource is owned.
Credit is 1060 C++ CODE bytes: 1042 instructions and 18 compiler-table bytes.

Both bodies live once in `spawn.inl` / `update.inl`, used by standalone wrappers
and `motion.cpp`. The full wrapper compiles these genuine consecutive functions
with one declaration context; no prefix filler or helper body is supplied.
Ordinary word alignment occurs after all canonical types, producing both
original zeros without source byte emission. A register-qualified pointer and
place local preserve the native capture order and allocation; no local is
aliased to a hardware register. Normal enum increments/decrements preserve the
original byte operations instead of materializing arithmetic/cast temporaries.

The unchanged full glyphball28, Motion12, Point4, nine-slot252-byte pool,
score92/section96 and byte playchar domain are reused. Eight slots are updated.
Creation keeps the occupied-slot removal/wait, space conversion, signed random
remainders and per-character score-panel targets. Animation restores prior
backgrounds, draws the current name, runs cloud/flight/splash/removal phases,
bounces at screen edges, steers and changes speed, then writes arrived glyphs.
Cloud-to-flight fallthrough, the final flight sprite on arrival, delayed DONE
cleanup, unchecked cursor/pointers and stale drawing locals for invalid phases
remain intact. No defensive initialization or new error handling is added.

The true far Pascal providers are IRAND/IATAN2/SUPER_PUT_RECT in CS0000 and
VECTOR2_AT/BGIMAGE_PUT_RECT_16 in ungrouped SHARED/E80. Near frame and name
providers remain foreign in GROUP_01. The common declaration header preserves
even empty SHARED SEGDEFs in that actual context. An initial combined-header
diagnostic wrongly grouped SHARED; identical physical destinations did not make
those far frame encodings acceptable. The corrected producer retains E80.

Standalone animation matches all 758 raw bytes but has a single descending
fixup run. The real 304-byte predecessor supplies the original record context:
both fresh actual OMFs have CODE LEDATA `[0,1024)` and `[1024,1062)`, naturally
placing the final far call in the second record. Full raw bytes, literal fixup
order, valid OMF, MAP and deterministic objects/MZs pass. The shared compiled
spawn-speed bias64-to65 negative is rejected, retaining extent and fixup order.

Receipt: `.analysis/unit-replays/maine-registration-motion-c/receipt.json`,
SHA-256 `19223f798f25482d0025f71ee794e748ba3a05278db0ff9b908c11fab04e1b05`.
Native/source/ABI review: `.analysis/registration-motion-native-source-review.json`,
SHA-256 `e3b11ec2f3e3867bea319ff7081517c541242885d0062bbbc395d69acec49d89`.
ReC98 `th05/regist.cpp` and `th05_maine.asm` provide candidate types/semantics;
maintained TH04 registration supplies supporting API conventions, not acceptance.
All older accepted records and source/header identities remain unchanged, so
only this new owner is replayed. No tool change, game model, decoding, packed-file
or whole-executable claim is made. Target provenance remains candidate-local-attested.

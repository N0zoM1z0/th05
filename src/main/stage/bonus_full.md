# Complete stage-bonus source context

The natural four-function family occupies original MAIN `[1C669,1CC0E)`:
the accepted multiplier/modifier pair contributes 305 bytes, followed by
`stage_clear_bonus()` at `[1C79A,1C9CB)` (561 bytes) and
`stage_allclear_bonus()` at `[1C9CB,1CC0E)` (579 bytes). The full source includes
the unchanged maintained helper bodies through their frozen combine guard.
The two later complete functions are proposed independently, with no duplicate
credit for the accepted helper pair. The full source is currently uncompiled
and unaccepted.

The maintained TH04 stage-bonus C++ is a semantic donor. Native original TH05
review determines its actual fields, arguments, constants and control flow.
Both functions snapshot resident miss/bomb counters, tint the palette, print
the actual near-pointer UI labels and calculate 32-bit bonuses. Ordinary local
variables retain the target's arithmetic widths without register hints. The
normal bonus includes the actual performance thresholds. The all-clear bonus
uses the real current-lives byte, a 50,000-point no-miss/no-bomb reward, and the
wide total-point-item multiplier of 250. No TH04-only life formula or extra
performance work is copied.

The original stage point-item counter is a byte at DS `36F5`. Each function
zero-extends it through AL/AH and SI. Calibration reads a word instead, making
its corresponding contributions three bytes shorter (558/576). Both images
have the same seven/nine relaxed-call NOPs; the three-byte difference is the
counter's genuine type context. Other full canonical Boss/resident headers
remain unchanged. UI pointer variables and gaiji strings stay foreign; this
source defines and claims no initialized DATA, strings, assets or BSS.

The normal function has 174 decoded instructions, the all-clear function 177.
Every direct branch destination is an instruction start, and each complete
function ends at its actual near RET. The original modifier's eight-byte rank
table stays inside the preceding accepted pair; the later functions contain
no CODE data tables. Native review identifies every instruction NOP:

| Function | Relative NOP offsets |
| --- | --- |
| Normal | 280, 311, 340, 375, 416, 443, 544 |
| All-clear | 313, 344, 373, 408, 443, 478, 505, 539, 562 |

Each is literal `90` immediately before PUSH CS and a near CALL to the actual
far HUD entry at `1527:063A` or `1527:0654`. Both share the caller's true CS
and retain the real far Pascal interface with RETF8. Truthful `samecodeseg`
declarations preserve this linker context without changing their far ABI.
All sixteen bytes are checked normally and receive zero authored credit.
The maximum proposed new credit is therefore 554 + 570 = 1,124 instruction
bytes from complete extents totaling 1,140 bytes.

The exact original ordered relative fixups are:

```text
normal:   [524,491,249,230,205,180,161,142,123,104,86]
allclear: [147,128,109,86,292,273,254,229,204,185,166]
```

The all-clear order crosses an actual compiler collection boundary. The real
preceding bodies place it at full contribution offset 866; its relative sites
147 and 166 then fall on opposite sides of the first 1,024-byte emission
window. This motivates recovering the genuine adjacent source context rather
than an isolated 579-byte translation unit. It does not establish exactness:
fresh OMF, complete raw bytes and original ordered fixups must still pass.
No fixup sorting or normalization is permitted.

The independent symbol-only binder places every external helper and global
at its real frame/offset and reserves holes only outside the complete 1,445
source bytes. It emits no instructions, internal padding, source DATA, stack
or duplicate helper body. Source-owned CODE must actually end at `1CC0E`
before its fixed outside tail can place DS at `209D`.

Private `.analysis/stage-bonus-full-boundary-review.json` records native bounds,
hashes, calls, direct fields, branches, NOP classification and the unchanged
helper source identities. The replayable bounded native check is
`python3 .analysis/stage-bonus-full-review.py`. The adjacent proposal file
registers only the two later complete C++ scopes from one actual TU. Normal
stage scaling 100-to-101 and all-clear reward 50,000-to-49,900 are meaningful
separate control proposals; a grouped replay must report which control it
actually compiled. Neither a configured control nor source presence grants
acceptance.

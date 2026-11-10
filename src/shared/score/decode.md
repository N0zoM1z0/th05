# OP score decoder: exact original AL-key compiler source

The complete OP compiler function is decoded C7D5..C87E, 169 instruction bytes,
without tables, padding or original MZ fixups. Its no-argument near Pascal
interface returns a byte in AL and preserves SI/BP. The ENTER/LEAVE frame holds
the byte rotation temporary. Two foreign 96-byte records are at DS5060/50C0;
their canonical types and assertions are imported unchanged from view.hpp.
No DATA, BSS or codec-provider replacement is defined.

The decoder processes 91 payload bytes forward, using the next encrypted byte
rotated right by three and XORed with key2, then adds key1 and the current
byte modulo 256. The final payload byte adds key1 alone. It sums all 92
unsigned payload bytes and checks the signed checksum word. A bad first
section returns 1; otherwise the second section is decoded and its checksum
difference is returned through the real byte interface. No extra checks or
error handling are introduced.

Candidate semantics follow ReC98 b6ba5b0a th04/formats/scoredat/decode.cpp,
impl.hpp and th03/formats/scorecry.hpp, with the maintained TH04 scoredec.inl
also consulted. The original compiler requires an inline byte-rotate primitive;
TC4J has no corresponding intrinsic. Only that operation on a named C++ local
uses assembly here. Traversal, mixing, summation and returns remain C++.
The donor's fixed-AL key algorithm is deliberately replaced by an ordinary
byte local; TH04 acceptance does not transfer.

One direct diagnostic with the ordinary key emits 181 complete CODE bytes.
The compiler stores/reloads the key across each rotation, adding six bytes
per section against the native 169. A subsequent ordinary `register` byte
declaration emits 182; it does not resolve the allocation. The 181-byte source
is restored byte-for-byte to the first frozen input. Neither producer passes
the complete raw gate, and both ordered fixup lists remain empty. Their larger
CODE also shifts the nominal harness DATA frame, so no whole-linked semantic
claim is made. Installed tool execution evidence was reused after identity
checks; no model, second positive, negative or full CI was needed.

Current diagnostic: `.analysis/native-producers/op-score-decode-local-key-a/`.

A later ordinary inline-function rotate expression cannot compile: TC4 rejects
assembly inside inline and template functions. The attempted primitive operates
on its named byte parameter, without the fixed-AL template, but the frontend
restriction prevents a producer object.
The maintained 181-byte source is restored byte-for-byte. No out-of-line helper,
second producer, negative or acceptance follows from that failed expression.

Complete native/source review:
`.analysis/op-score-decode-native-source-review.json`.
The proposal `.analysis/op-score-decode-proposal.json` stays outside the live
exact manifest. This source adds zero accepted functions or authored bytes;
the neighboring encoder and MAIN/MAINE codecs remain untouched.

## Complete 169-byte OP decoder accepted — 2026-11-10

The original `scoredat_decode()` OP function at `[C7D5,C87E)` is now exact
natural C++ with the authentic TC4J byte-rotate inline operation. Both fresh
Borland compiler/linker producers reproduce **169/169 instruction bytes**,
the unchanged empty original MZ relocation stream and the real complete
function boundaries. Its compiled negative changes the decryption XOR to
addition, changing the complete original code and being rejected.

The old 181-byte ordinary byte-key version was exactly **12 bytes too long**:
each of its two independent score sections spilled the `key2` byte to a
stack local and reloaded it after the original `ROR [BP-1],3`. The original
assembly instead loads each section's key directly into `AL` and preserves
that register through the rotate, then executes `XOR [BP-1],AL`. This
source-level dataflow is now explicitly represented by the DOS register
interface in the single maintained decode macro:

```cpp
_AL = (section).key2;
asm { ror value, 3; }
value ^= _AL;
```

The rest is unchanged C++: both 96-byte records at DS5060/50C0, the 91-byte
forward decryption loop, direct wrapped key1 plus current-byte reconstruction,
92-byte checksum, early failure return from the first record and final
checksum difference from the second. No file-format changes, error handling,
foreign DATA, instruction templates or target-derived patches were added.
The full source is in `decode.cpp`; the original near-Pascal ABI and
`scoredat_section_t` are preserved from the shared OP header.

Focused receipt:
`.analysis/unit-replays/gpt-web-op-score-decode-original-al-169-a/receipt.json`.
The old 181/182-byte first-producer diagnostics above are historical failed
C++ variants. The function adds **169 exact OP C++ CODE bytes** and no
additional record or asset ownership. No other accepted source depends on
this file, so unrelated artifacts need no replay.

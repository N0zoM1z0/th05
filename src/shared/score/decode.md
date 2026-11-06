# Ordinary score decoder candidate

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

Actual frozen producers:

- `.analysis/native-producers/op-score-decode-local-key-a/`
- `.analysis/native-producers/op-score-decode-register-key-a/`

Complete native/source review:
`.analysis/op-score-decode-native-source-review.json`.
The proposal `.analysis/op-score-decode-proposal.json` stays outside the live
exact manifest. This source adds zero accepted functions or authored bytes;
the neighboring encoder and MAIN/MAINE codecs remain untouched.

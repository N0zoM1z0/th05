# MAINE score-file encoder/decoder: exact C++

The two complete near-Pascal source functions are now accepted on the original
MAINE score codec segment: `scoredat_decode()` `[B4D6,B52C)`, **86 bytes**,
and `scoredat_encode()` `[B52C,B590)`, **100 bytes**. Both use the authentic
96-byte score-section layout and bytewise key1/key2 rolling cipher. Decoder
rotates an ordinary byte local three bits right and checks the eight-bit
checksum difference; encoder computes the word sum, obtains two genuine
random bytes, then transforms the score payload in reverse. The AL register
holds the real bytewise key across the single original inline `ROR` primitive;
records and loop arithmetic remain ordinary C++ (not handwritten instruction
emission). The only relocation sites are the encoder's two original `IRAND`
far calls, in their exact original order.

Both functions were independently selected from the original-order
`src/maine/registration/full_context.cpp` and passed two deterministic linked
C++ builds with complete raw+fixup matching. The `value ^= _AL` / `feedback ^= _AL`
mutations change the real key-mixing semantics and were rejected. Total **186
new C++ instruction bytes**; no score DATA, filename or adjacent already
accepted display code is counted.

Receipt: `.analysis/unit-replays/gpt-web-maine-registration-codecs-full-20261110/receipt.json`.

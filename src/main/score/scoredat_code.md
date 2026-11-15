# scoredat_decode() and scoredat_encode() (scoredat_code.asm)

MAIN's own GENSOU.SCR section codec. Both are near Pascal functions without
parameters that work on the 96-byte section in `hi`: a 92-byte payload (five
9-byte names, five 8-byte scores, five stage bytes and unused bytes), two key
bytes and a word checksum. The layout matches `src/op/hiscore/view.hpp`.

- Decoding goes forward through the payload and adds
  `((next byte ROR 3) XOR key2) + key1` to each byte, using the next byte
  before it is decoded itself. The last byte only gets key 1 added. The function then sums the decoded
  bytes and returns the stored checksum minus that sum in AX; callers only
  check AL.
- Encoding stores the plaintext checksum, gets both keys from `irand()`, and
  runs backward through the payload with the previous result as feedback in DL.

ReC98 commit 8dbb4505 notes that MAIN.EXE got separate micro-optimized ASM
versions of these functions, which matches their frameless, register-packed
code. TH04's `scoredat_code.asm` has the same structure for a different
payload size.

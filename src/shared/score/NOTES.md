# Shared score: notes

- **OP score decoder.** The ENTER/LEAVE frame holds the byte-rotation
  temporary. It sums all 92 unsigned payload bytes and checks a signed
  checksum word. A `register` byte declaration (182 bytes) does not fix the
  allocation; the accepted source keys the rotation through AL.

# Shared hardware helpers: notes

- **Held input.** Both providers return a word in AX with RETF. Reset clears
  two words and falls through into sense, sharing its return; giving reset its
  own RET or a near return changes the ABI. TCC emits ordinary far calls and
  TLINK relaxes each to `NOP` / `PUSH CS` / near `CALL`.
- **Frame delay.** Borland's `peek` reads the argument from `SS:SP+4` into BX.
- **EGC rectangle copy.** The 16-dot destination word comes from a signed
  `>> 4`; the word count goes to the foreign `egcrect_w`.

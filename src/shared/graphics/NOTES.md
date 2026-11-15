# Shared graphics: notes

- **OP single-plane CDG.** Rows are copied with a 386 `REP MOVSD`, walking
  backwards until the signed DI condition ends the loop. A plain C++ signed
  shift there adds an AX temporary (78 bytes).

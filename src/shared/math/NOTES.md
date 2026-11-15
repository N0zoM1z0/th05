# Shared math: notes

- **Far vector pair (unaccepted).** Borland lowers each signed table read to
  `MOVSX EAX,[BX+table]` plus `MOV EDX,EAX` (or ECX) instead of the native
  direct `MOVSX EDX/ECX,[BX+table]`. The unsigned register-intrinsic multiply
  also produced `SHR EAX,8` where the original has `SAR EAX,8`; a signed cast
  fixes the shift but not the load shape. Tables are at DS `041C` (sine) and
  `049C` (cosine).

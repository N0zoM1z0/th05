# OP initialization

Natural GAME5 C++ follows ReC98 b6ba5b0a th03/core/initop.cpp. It preserves
DOS-memory failure handling, clearing both graphics pages, the repeated page
selection, the8192-byte packfile buffer, hardware/service startup and the
conditional archive open. Page writes use the actual Borland outportb intrinsic
for PC-98 portsA6/A4; no instruction bytes or ASM body are supplied.

The complete original function is decoded OP DF12..DF8E,124 bytes, with
SHARED frameD30 and DGROUP EFE. Every external library address and both globals
were independently checked in the original view. The no-STACK binder retains
the known real foreign music DATA extent through DS2817 and supplies no values.
`op-core-init-a` passes two independent fresh producers, complete raw bytes,
original ordered fixups and a compiled packfile-buffer mutation8192→4096.
No DATA/BSS, foreign API implementation, whole-game or packed-file credit is
claimed.

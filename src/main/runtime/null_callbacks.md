# Empty near and far callbacks

MAIN C73E and C740 are the actual one-byte no-op callback bodies, respectively
near RET and far RETF. Each complete compiler CODE contribution is one byte;
the NOPs at C73F and C741 remain foreign alignment and receive no credit.
These are intentional complete game callbacks, not missing implementations.
The near callback disables input hooks and overlays in maintained callers;
the TH04/TH05 stage and midboss reference code uses both distances to disable
optional update/render/invalidation work.

The ordinary empty C++ definitions retain the real C/Pascal linkage, no
arguments and zero cleanup. The source's frameless option avoids an unnecessary
BP frame. No instructions, opcode bytes or alignment directives are supplied
by C++; no target payload is supplied by the symbol-only binder. The two
compiler-owned segments have complete ordinary OMF contributions. Both
callbacks preserve all registers and flags. They own no DATA/BSS or fixups.
ReC98 b6ba5b0a th04/main/null.asm corroborates the native bodies and names;
its assembler filename does not grant source-language attribution or acceptance.

Two fresh deterministic producers pass valid complete ordinary OMF/CODE
contributions, native MAP scopes, both complete raw bytes and empty ordered
fixups. Both callbacks share one compiler invocation per round and the normal
compiled ABI negative: changing the near callback to far changes its return
instruction and is rejected. No per-function extra negative or behavior model
is added. Normalized objects, MAPs and complete MZs are deterministic.

Receipt: `.analysis/unit-replays/main-null-callbacks-a/receipt.json`, SHA-256
`e07e0f7e56589fd1d76bae7d33c18687596e21eb82fba97f1567bf7655301395`.
Import adds two complete functions and two C++ instruction bytes, with no
DATA, BSS or padding credit. No whole executable is newly accepted.

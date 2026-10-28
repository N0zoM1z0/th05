# Exact sword renderer

The complete MAIN function `[143E0,14422)` is66 bytes/28 instructions, with
CS0AE1 and DS209D. All branches and the final RET are reviewed. It has no
instruction NOPs, tables, padding or relocations.

Maintained C++ traverses all63 swords after the template in the canonical
64x26-byte custom pool. It keeps the real word sprite value, signed pixel-X
shift, scalar scroll call atDF28 and tiny32 call atBF62. The complete Sword26,
template25 and motion types are unchanged. AX/DX/ES access is confined to the
existing graphics ABI; there is no instruction template or helper body.

Two fresh normal producers reproduce every byte and empty relocation stream.
Their valid OMF objects each contain one complete66-byte LEDATA; MAP scopes,
source/tool inputs and actual argv are validated by normal receipt import.
Normalized object, MAP and scaffold-MZ identities are deterministic. The own
live/free predicate inversion changes only byte22 from74 to75 and is rejected.
The address-only binder supplies outside reserves and no initialized bytes.

Receipt `.analysis/unit-replays/main-yumeko-swords-render-a/receipt.json`, SHA-256
`b1bd8679efe138790eec8986c303143b5a1194a3f664f1ce7873f409882ea5e0`.
Native/producer review `.analysis/yumeko-swords-render-review.json`, SHA-256
`6d09676d40a1ab7184da3d618956bd42f53ed34c3a947e4e1dd6b8d3411f3141`.
Import adds66 C++ instruction bytes and one complete function. This is bounded
acceptance, with no whole-program placement, assets or packed-file claim.

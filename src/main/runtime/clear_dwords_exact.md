# Exact stage-pool DWORD zero-fill helper

MAIN `CF62..CF79` is the complete 23-byte near-Pascal helper
`clear_dwords(void near *dest, unsigned int count)`. It copies the caller's
DS to ES, takes its true destination and 32-bit-element count from
`SS:[SP+4]` and `SS:[SP+2]`, clears EAX, and zeroes each DWORD through
`REP STOSD`. It preserves DI and returns with `RET 4`, retaining the native
clear-direction-flag assumption rather than introducing a new `CLD`.

The source-level register interface is preserved in pinned ReC98
`th05_main.asm` as `sub_E708`, with actual near-Pascal consumers in the
accepted `stage_state_init()` implementation. This is reviewed original-
register ASM, not a claim that the earlier unaccepted register C++ experiment
produced exact bytes. The byte at `CF61` and following `CF79` NOP are outside
the function and remain unowned.

The focused receipt
`.analysis/asm-replays/gpt-web-main-clear-dwords-near-a/receipt.json`
contains two native TASM32/TLINK producers, full 23-byte identity, the true
empty ordered relocation stream, and matching MAP/OMF ownership. A compiled
source mutation that reads the destination offset in place of the DWORD
count is rejected. All 23 bytes are reviewed ASM instructions, with no
padding, jump table or initialized DATA attributed to this source.

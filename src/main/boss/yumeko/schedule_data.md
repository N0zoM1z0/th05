# Yumeko mobile-phase attack schedules

The two original near-callback banks in MAIN `[2296E,2297E)` now have
a complete 16-byte natural C++ DATA owner. They are two four-entry
`yumeko_pattern_func_t` arrays. Phase 2 selects the sword-fan and red-ring
patterns, and phase 5 selects the counterrotating and mirrored spreads.
Both banks have two genuine null slots. The accepted complete Yumeko
controller indexes each bank with `patterns_seen & 1`, so only the two
live entries are selected; the original array type and four-slot extent
are retained rather than silently shortening each bank to two entries.

These are two-byte near-cdecl function pointers under MAIN03; every
non-null callback has an independently accepted complete body at
`1EF59`, `1EFEE`, `1F1EA` or `1F324`. The symbolic binder supplies
only their original CODE publics and genuine MAIN group frames. It does
not provide binary pointer values, game instructions or initialized
DATA. The full 16-byte C++ initializer contribution starts at DATA
`209D:1F9E`. The following zero region `[2297E,2298E)` remains
unknown rather than being absorbed as artificial array padding.

The first native link revealed the actual Borland 31-character EXTDEF
truncation for `yumeko_pattern_counterrotating_spreads`; correcting only
the outside assembler public restored the source-generated relocation.
The targeted replay receipt
`.analysis/unit-replays/gpt-web-yumeko-mobile-schedules-b/receipt.json`
records two complete native C++ producers, a full 16-byte raw comparison,
original OMF/MAP size and empty ordered MZ fixups, and rejection of the
compiled first-two-pattern swap. No other units were recompiled.

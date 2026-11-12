# EX-Alice: exact repeated approach/regular continuation in the full Boss

The second, third and fourth main attack waves each perform a distinct
palette transition, then decide from their own first-approach phase whether
to enter the existing shared `approach` movement block or continue through
`regular_attack`. The real native code uses the same two-target branch
protocol in all three places. `EXALICE_RESUME_WAVE(first_approach_phase)` now
expresses that source-only control flow without a compiled helper, cached
phase or altered palette operation. Wave-specific blue, red and green
increments, charge behavior, damage and callback ordering remain separate.

The complete 1,060-byte original `main-exalice-update-full-context` source
was rebuilt with two genuine Borland/TLINK producers. Both matched the
entire original machine-code extent, three switch tables, ordered loader
relocations and the meaningful compiled HP-gate negative. Evidence:
`.analysis/unit-replays/gpt-web-exalice-waves-cfg-20261113-a/receipt.json`.
The code was already credited and gains no duplicate authored bytes.

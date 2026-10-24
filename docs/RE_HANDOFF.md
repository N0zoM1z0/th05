# TH05 current handoff

Goal: at least 98% authored bytes exact. Commit prefix: `gpt-6.1-sol:`.
Current acceptance: 8 C++ contributions, 36 functions, 6099 compared bytes and
6088 authored code bytes (5972 instructions, 116 semantic switch-table bytes),
after excluding 11 observed padding bytes.
Public acceptance lives in `config/accepted_units.json`; global percentage is
unmeasured pending complete ownership/denominator review.
Public repository: https://github.com/N0zoM1z0/th05 .

The user's supplied Japanese image is accessible through WSL. Public
`config/targets.toml` pins its identity and four KAIKI executables. The image
digest differs from TH04's outer Japanese image, while all four TH05 executable
hashes agree with its calibration corpus. Original assets remain private.

Borland tools have an independent Wine prefix and pass identity plus executable
compiler/assembler/linker/OMF/determinism probes. Ghidra 12.1.3 and Temurin
21.0.12.1+1 pass installed identity checks. MAIN's `TH05-main-loader` project
passes independent database attestation, including all bytes and relocations.
Full automatic analysis hit the 768 MiB cgroup limit; use loader-only imports
and bounded analysis. The failed project is not accepted evidence.
Imports now default to loader-only. Both first-unit ranges pass fresh-nonce,
original-file, relocated-memory and complete bounded disassembly checks in
`TH05-main-loader` (load offsets `171CC/30` and `17676/66`, load segment `1000`).
TH05 MAIN is ordinary MZ (4032-byte header, 998 relocations); OP/MAINE are
DIET-packed MZ. ZUN is plain COM.

Independent DIET observation passes at two load segments for OP/MAINE. See
`python3 scripts/unpack_targets.py`; payloads/receipts are in `.analysis/decoded`.
MAIN's first pinned-reference calibration build completes 83 serial steps but
does not match original layout or bytes. It creates no authored credit.

Player angle, bullet tuning, Boss movement and the CFG resident reader have
local C++ sources and owning declarations.
Two cold rounds plus compiled threshold-mutation control pass under explicit
target external-symbol bindings. Current replay: `.analysis/unit-replays/boss-cfg-a`.
First replay remains `.analysis/unit-replays/first-cxx-b`; its original tool
attestation was copied beside its receipt after verifying the recorded digest.
Current replays freeze tool attestation at build time. Public acceptance
re-reads both saved MZ/MAP/OMF producers, the actual target extents/fixups, source
snapshots, tool manifest and the saved compiled negative producer.

Current focused replay `.analysis/unit-replays/boss-explosion-a` compiles only
the new explosion contribution; it reuses the unchanged complete tool probe
receipt after active file/header/library identity checks. Its two raw/fixup
comparisons and compiled age-threshold mutation pass. Previous four contributions
retain their original evidence; only their dependency snapshots were narrowed
from the whole tree using saved actual OMF dependencies, without recompilation.

Next focused receipts are `.analysis/unit-replays/hud-overlay-a` and
`.analysis/unit-replays/reimu-shots-a`: 1806 and 1175 new bytes, 9 and 8 functions.
HUD keeps the original AE1:6F40 contribution, its own near callback at 711D,
and all 24 ordered fixups. Reimu keeps AE1:38EB and real Shot/SPPoint ABI,
with no MZ fixups. Both reuse unchanged installed tools and leave all preceding
producers untouched. Owner notes record their complete external bindings.

`.analysis/unit-replays/marisa-shots-a` adds eight shot functions as one focused
2134-byte producer. Semantic switches generate seven CODE tables; all 58 targets
land on original function instruction boundaries. Its five zero alignment bytes
are checked in the full comparison and excluded from credit. Original AE1:3D82
placement preserves table addresses. No old unit is recompiled.

Next: extend bounded authored units and review the complete ownership partition.
No whole-game or standalone C++ build claim is made. See the first-unit note for
numeric bindings, sizes, limitations and replay commands.

The standalone ZUN `-M` child is a separate accepted 311-byte complete COM
producer (142 code, 169 data), from maintained semantic ASM with inferred
original style. Two cold builds and a compiled threshold mutation pass in
`.analysis/zun-memory/first-b`. Public source-current acceptance is
`config/zun_memory_acceptance.json`; this is not C++ credit or outer ZUN exactness.
`inspect_launcher.py` validates all 18,116 container bytes as a physical partition.
See the ownership survey for remaining exclusions and provenance.

User steering: accelerate work and replay only necessary units. Retain accepted
unchanged objects/evidence; rerun only new or affected sources and dependencies.
Toolchain probes are reused when all relevant installed identities are
unchanged. `replay_units.py --plan` and `--units ID...` are implemented; acceptance
merges only the selected unit results. The next source investigation is the
Marisa shot contribution (2134 bytes in the reference CODE map). Boss background
rendering needs a natural replacement for an upstream fake-zero codegen helper
before it can be accepted. Masked routing
survey found 42 candidates/14,922 bytes; those are diagnostics, never credit.

TH03 has unrelated uncommitted work; do not modify it. TH04 is a read-only
reference. Use an independent Wine prefix and serialize heavy jobs.

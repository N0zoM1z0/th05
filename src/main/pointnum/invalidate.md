# Point-popup invalidation: natural scalar C++, still inexact

The complete MAIN scope `[E17A,E1A6)` has 44 instruction bytes, no
instruction NOPs and no MZ fixups. It walks all 280 complete 16-byte records,
including every nonzero flag, sets height once, then copies each active
record's full width before the actual near Pascal tile-provider call.
Arguments remain previous Y at record offset 6 and current X at offset 2;
they are not one contiguous point. All pool/list storage remains foreign BSS.

The earlier whole-lifecycle candidate used an unsigned count and emitted a
redundant zero test. The new standalone owner uses an ordinary signed count,
whose actual values remain 280..0, and the canonical `Subpixel` scalar
conversions. Neither change alters the loop's behavior, layouts or ABI.
The shared header, compiler options, full types and provider prototype are
unchanged. No physical-register alias or assembly body is supplied.

Three actual first producers were retained:

| Natural source context | Complete CODE | Observation |
| --- | ---: | --- |
| Signed count, ordinary current-X local | 52 | Two-byte stack slot, ENTER, dead local store and LEAVE |
| Same local with block scope and `register` | 52 | Identical complete CODE; storage annotation has no effect |
| Canonical scalar conversions, no local | 43 | No frame; two direct memory PUSH arguments |

The original preloads current X into AX, then pushes previous Y and AX.
The final ordinary C++ lowers the two arguments to memory PUSHes, one byte
shorter. All native bytes remain mandatory; the discrepancy is not padding.
Every replay stopped at its first complete-size gate, with no second
positive, compiled negative or receipt. The final 43-byte source is maintained
in `invalidate.cpp`; its proposal is parked outside the live exact manifest.
The original 44 bytes remain entirely unknown and uncredited. Init/update
and their two alignment NOPs remain outside this source and unaccepted.

Actual ordinary CRC-valid OMF, complete MAP extents, source snapshots and
compiler argv were reread for all three attempts. Private first producers
are `.analysis/unit-replays/main-pointnums-invalidate-{a,b,c}/`.
Review `.analysis/pointnums-invalidate-scalar-producers.json`, SHA-256
`f30e293d20a1ac0265e541ce33ed858ae4ac12a2cb6a8f597596e1d8d99333c0`.
No padding, ABI reinterpretation, fabricated callee, flag search or original
ASM attribution is inferred from the failed C++ output.

The final actual compiler output and native invalidator both pass seven
independent generated full-pool cases, covering empty/full/mixed pools,
flags 0/1/2/3/128/255, signed X boundaries, deliberately distinct current and
previous Y, full word widths, unchanged record/list tails and stale width
when the pool is empty. The checker compares all generated DGROUP bytes,
actual RET4 arguments and box values, scratch-register clobbers, preserved
SI/DI/BP/DS/SP and IF/DF. Tile-provider effects are excluded.
Report `.analysis/pointnums-invalidate-scalar-semantic-check.json`, SHA-256
`e6746fe0d4a820d18ffdedebf2b60f71bfbd4cd1154d779f9ecc27f481efbccf`.
This is bounded semantic evidence, not exact acceptance.

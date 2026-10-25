# HUD decimal renderers

This semantic ASM candidate covers MAIN 158AA..15914, two real far Pascal
entries sharing a decimal formatter and one RETF8 tail. Five-digit rendering
starts at relative zero and point rendering at 26; the common tail starts at
51. The complete family is 106 bytes, with one EVEN NOP at relative 25 and
one ordered MZ relocation at 99. There are no tables or owned DATA/BSS.
The NOP compares normally and receives zero authored credit.

The first API takes four unsigned words: left, row, value and attribute.
The second takes left and row words followed by unsigned DWORD points.
Both preserve DI/BP, queue five real far-renderer arguments and enter the
same tail with EDX=remainder, BX=divisor cursor, AX=attribute and CH:CL as
leading-zero state and digit count. Shared inter-procedure entry and this
packed 16/32-bit register protocol support inferred original handwritten
ASM. Standard BP frames or modern ASM donor syntax alone would not prove it.
Historical source, original assembler and exhaustive ancestry remain unproved.

The renderer writes character IDs only. Five-digit output uses the last five
cells of the foreign nine-byte row at DS:142C; point output writes seven
decimal digits and a forced zero in the continues-used cell. Leading zeroes
become empty glyph 02h, while the units digit always appears. The 28-byte
divisor table at DS:1406 is independently accepted mathematical C++ DATA;
this unit merely references it and receives no additional DATA credit.
No gaiji image, buffer initializer, terminator or renderer body is supplied.

Clear DF is an entry precondition, and no CLD or numeric range guard is added.
Values above seven decimal places preserve the native low-byte glyph
arithmetic rather than gaining clipping. ES is set to DS for string writes;
the external FAR renderer remains at 0000:1DBE. The CODE group frame is 1527,
and DS is 209D. No accepted C++ header or caller is changed.

Pinned ReC98 th05/main/hud/number_p.asm supplies the semantic candidate,
with no acceptance transfer. The maintained loops and symbolic stack/glyph
constants contain no target byte strings or compiler-body transcription.
The donor's local NOSMART state preserves the two explicit LEA operations;
it is declared before the first producer, without changing assembler flags.
Exact producer gates and explicit source/ownership adoption remain required;
source presence alone grants no credit.

A native-only check compares actual execution with independent Python decimal
formatting for 282 edge/generated cases. It verifies glyphs, leading blanks,
forced score zero, string-pointer/argument order, far cleanup and untouched
terminator/canaries. Five-digit cases use unsigned WORDs; point cases cover
0..9999999, without claiming full-DWORD formatting or invalid-input safety.
The foreign renderer is intercepted, not executed.
Report: `.analysis/hud-numbers-native-semantic-check.json`, SHA-256
`d675b6753d90b761a6ab38a95ab4cbb4ac367583e55fb9c2e40ee3d5bc3c3d4f`.

Independent native/source/origin review:
`.analysis/hud-numbers-independent-origin-source-review.json`, SHA-256
`18dbb5e270a8739e51fc04dd5ba525fb82162154eab1ce2aa1f3b83de1901e70`.

The first actual producer in `main-hud-numbers-a` matches all 106 native bytes
and ordered fixups `[99]`, but the wrapper stops on incorrect manifest public
spellings. The manifest initially names decorated symbols; TLINK's MAP table
uses the real demangled signatures. Only those two checker names are corrected.
The original failed workspace remains byte-identical. No assembler input,
source, type, flag, segment, ABI, instruction or relocation changes.

Continuation `.analysis/asm-replays/main-hud-numbers-b/receipt.json`, SHA-256
`9e38b0689ff4ec075a7d6f3bf78c4f2af0ccd9bb9ac6a9cca3864d375d7f4c17`,
retains that actual first producer after all source/tool/argv/log checks and
compiles only the independent second and own negative. Both complete ordinary
106-byte CODE contributions pass raw bytes, original ordered relocations,
OMF coverage and MAP/public/CS/DGROUP checks. The standard validator re-reads
all saved artifacts. The negative changes the five-digit leading count from
four to three, changes only byte 21 and is rejected without changing the scope
or fixups. All installed execution probes and old accepted owners are reused.

Private `continuation-lineage.json` in that receipt directory binds every file
of the retained original workspace, the two changed MAP-check keys and the
identical copied first artifacts, SHA-256
`cba544f1441310d5973d46929c23e584a486e1aa901edb7c789878fa718cfb48`.
There are three source assemblies, three symbol-only binding assemblies and
three links in total; the first producer is not rebuilt. The wrapper metadata
failure is preserved and does not count as byte acceptance by itself.
Explicit ownership adoption remains separate from this replay.

The separate decision in `config/reviewed_asm_families.json` adopts only this
complete family as 105 reviewed ASM instruction bytes plus one compared,
uncredited alignment NOP. It grants no C/C++, divisor DATA, foreign buffer,
glyph-image, renderer-provider or whole-executable credit.

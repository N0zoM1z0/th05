# Sound file loader

One maintained semantic ASM source independently reconstructs three complete
native loaders. Each is 184 instruction bytes, 71 instructions, no NOPs,
padding, tables, placeholders or owned DATA. Original ordered MZ fixups are
[70,78,87], the three real Beep-library far calls. RETF 6 is at relative 181.

| Artifact | Complete load range | CS | DS:filename13 / extension15 / SE byte / BGM byte |
| --- | --- | --- | --- |
| MAIN | 14EA4..14F5C | 14AB | 209D:3056 / 0826 / 0835 / 0836 |
| OP | DBBE..DC76 | 0D30 | 0EFE:383E / 0A52 / 0A61 / 0A62 |
| MAINE | ED66..EE1E | 0E80 | 1011:27A6 / 06CC / 06DB / 06DC |

All direct branches and complete boundaries were independently reviewed against
the pinned original load modules, including the native short conditional jump
with displacement 127. Calibration shapes and reference acceptance do not
establish exactness or transfer ownership between artifacts.

## Origin and source

The candidate algorithm is pinned ReC98 b6ba5b0a,
`th05/snd/load.cpp`. Its local history at commit 01c92da1 explicitly describes
the routine as ZUN-written ASM. This corroborates independent native evidence:
BP is repurposed as the load-function word after argument reads, DS/ES are
manually switched around filename and driver buffers, EAX supplies packed
extensions and DOS carry/error flow controls retry behavior. The three original
far-call fixups retain source order. No particular inspected native subspan has
positive compiler-generated provenance.

Maintained source uses semantic DOS/file/mode constants, a DOS-open macro,
typed arguments, real provider names and control-flow labels. It contains no
synthetic C++ register templates, opcode emits, numeric local CODE addresses,
copied instruction listing or opaque byte arrays. Literal historical source
and original assembler identity remain unproved; mixed-source possibilities
are not asserted away by a passing replay.

A bounded search of all 653 pinned master0.23 archive members found known
Beep/file provider definitions but no substantial copied loader body. Provider
bodies and types remain foreign, and no library ownership is transferred from
names or ordinary DOS interrupt sequences. This is not an exhaustive renamed
body or historical-ancestry investigation.

## Preserved ABI, state and packed bank

SND_LOAD is far Pascal `(filename16:16, function16)` and removes six argument
bytes. The complete function domain includes song 0600h and SE 0B00h. BGM
mode bytes retain OFF/FM26/FM86 and unsupported MIDI value 3, with the original
configured count of three; SE mode bytes retain OFF/FM/Beep. Word API values
are not narrowed to byte arguments. BP/SI/DI are saved and restored; working
AX/BX/CX/DX and flags are not promised as returns.

The source copies exactly 13 filename bytes, then searches using REPNE SCASB
with CX=FFFFh before appending a dot. Entry DF clear is required; no CLD or new
length/extension guard is inserted. Filename construction still occurs before
disabled-mode returns. ES is set to the original DATA segment without saving
incoming ES. The successful driver path restores DS through ES after read/close;
foreign Beep/driver contracts matter. No blanket incoming ES, IF or flag
preservation guarantee is invented.

The extension bank is **15 declared bytes**, not a padded four-by-four array.
Its four fields occupy 4/4/4/3 bytes. FM86's dword includes an extra 'm' after
its terminator; the MIDI dword at bank+12 overlaps the separate SE-mode byte
at bank+15. That fourth byte is still copied after the filename terminator.
The typed include preserves the full bank and its read window without supplying
initial values, padding or a false 16-byte DATA object. Filename storage and
both mode bytes likewise remain foreign. No DATA credit is claimed.

SE Beep mode writes the semantic `efs` extension, finishes the Beep subsystem,
initializes 2048 bytes and loads through BGM_READ_SDATA. The far providers use
0/2/4 argument-byte cleanup. Song mode stops the active driver through the real
SND_KAJA_INTERRUPT far Pascal procedure at 14F5C/DC76/EE1E. Its native PUSH CS
plus near CALL is retained while the source still declares a real FAR provider;
it is not relabeled as a near-returning callee. Subsequent mode indexing remains
zero-extended byte arithmetic.

DOS file-not-found falls back to `.m` without a retry bound. Missing both the
selected file and fallback can loop indefinitely. Other open errors return.
Driver-buffer selection uses MMD only for song-address requests with MIDI mode;
SE continues through PMD. DOS read still requests 65535 bytes without checking
the driver's capacity, then closes the handle. No buffer-size query, truncation
fix, timeout or new error recovery changes the original behavior.

Symbol-only binders retain actual segment/DGROUP frames, full external scalar
types and exact EXTDEF names. They supply no initialized payload, library body
or artificial stack; each ORG is below 64 KiB. The same-CS call's near relative
target resolves to the real adjacent far procedure, with no new SHARED group.

## Exact gates and incremental reuse

Receipts `.analysis/sound-load-native/{main-a,op-a,maine-a}/receipt.json` each
contain two fresh deterministic complete TASM producers, full ordinary CODE
SEGDEF/LEDATA/MAP/public/frame validation, all raw bytes and literal ordered
fixups. Each owner's own assembled read-limit mutation from FFFFh to FFFEh
changes a real DOS transfer bound and is rejected across the same complete
scope and relocation stream. Installed tool execution proofs and all prior
accepted objects are reused after dependency-identity checks, not recompiled.

Independent reports are `.analysis/sound-loader-native-review.json` (SHA-256
`f05842944010c44a159c835b13ab53ceccf2d64441d9ea1c9062a59b779b0303`)
and `.analysis/sound-loader-maintained-source-review.json` (SHA-256
`0d10fdbbcc67b1ba5898ee36ede128a68b1c4d74b10cdaeff6f0eaf8bbd5e62b`).
Descriptors pin the complete native proofs; exact records and explicit
per-owner/note adoption remain separate in the generic ASM ledgers. Total new
credit is 552 reviewed ASM instruction bytes, zero DATA or asset bytes. C/C++
counters, unknown unrelated scopes, whole-executable packing and the unreviewed
global denominator remain separate; the 98% objective is still open.

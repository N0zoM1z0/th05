# Player shot helpers

The complete consecutive MAIN family is E38C..E40E, 130 compared bytes:
allocator E38C..E3C4 (55 instructions plus one alignment NOP), angle velocity
setter E3C4..E3E2 (30 instructions), and power-level update E3E2..E40E
(43 instructions plus one TLINK far-call relaxation NOP). There are no tables
or MZ fixups. The following invalidation function is excluded.

The full 18-byte shot retains flag, age, current and previous positions,
velocity, sprite, type, damage and angle. The allocator compares the current
cursor with the 64-record pool end before advancing to the next record. That
order is preserved exactly, including a possible read at the end label; no
allocation check or bound correction is added. A free record receives alive
flag/zero age, the player's current point, velocity (0,-12 pixels), and primary
sprite20/type0. Previous coordinates, damage and angle remain untouched. It
returns the near pointer in AX and stores the following record as the cursor;
failure returns zero without writing the cursor.

The velocity setter snapshots entry SP in BX before saving SI, consumes a
WORD near point pointer and a byte angle in a WORD Pascal slot, and RET4s.
It zero-extends that byte, writes the shot angle seven bytes beyond the point,
then copies the mathematical table's four-byte velocity via EAX. The argument
must point inside a full shot, despite the nominal point-pointer signature.
No pointer check is added. Native EAX contains the copied DWORD on return;
DX is unchanged. No new DX:AX Point-return guarantee is inferred from the
existing nominal C++ declaration, and accepted callers/types are unchanged.

The far level updater zero-extends power, searches all nine unsigned WORD
bounds, stores level0..9, selects the corresponding near function from the
current character's ten-entry row, and calls the real far HUD provider at
AE1:2445 (MAIN D255). SHOT_LEVEL_UPDATE is a descriptive maintained public;
its historical spelling is unknown. The real no-argument far interface has
zero argument cleanup. The provider's own hardware effects remain foreign.
The existing C and C++ callers use SHOT_LEVEL_UPDATE and
@shot_level_update$qv for that same argumentless interface; both maintained
public names resolve to this one entry and add no function or instruction.

Independent ASM inference uses the allocator's AX/BX-only preincrement scan
and packed field initialization; the setter's entry-SP/SI, MOVZX and EAX copy
protocol; and the updater's coupled CX/BX WORD search followed by DX byte-index
conversion and a frameless far HUD call. These are whole-procedure decisions,
not attribution inherited from adjacency or failed C++ trials. Candidate
algorithms are ReC98 b6ba5b0a th05/main/player/shots_add.asm,
th04/main/player/shot_velocity.asm and th05_main.asm's sub_E4FC. The last is
disassembly reference, not recovered historical source. Historical source,
assembler identity and exhaustive vendor ancestry remain unknown.

The allocator and setter preserve BP/SI/DI/DS/ES, IF/DF; AX/BX and arithmetic
flags are scratch. Their own DX/CX remain untouched. The level body uses
AX/BX/CX/DX; further hardware/register effects belong to its real HUD call.
All fields and geometry derive from complete maintained record/table types.
The binders provide only native frames and foreign labels, never pool values,
sprite payloads or a provider body. Both existing semantic C tables, the pool,
player motion, cursor, power and function pointers receive no new DATA/BSS credit.

Two fresh deterministic producers pass complete ordinary OMF/CODE/LEDATA,
native MAP publics/CS/DGROUP, all130 raw bytes and the empty original fixup
stream. The shared normal negative changes primary sprite20 to21 and is
rejected with unchanged extent and fixup order. Normalized objects, MAPs and
whole MZ outputs are deterministic; only dependency metadata is normalized.
Explicit adoption adds128 ASM instruction bytes and two compared, uncredited
NOPs. No C/C++ function, initialized DATA/BSS, foreign HUD provider or whole
executable gains acceptance. Unchanged accepted inputs and tool execution
proofs are reused after identity checks; no whole replay, per-function extra
negative or CPU behavior model was run.

The first assembly stops in the frontend because the field-difference EQU
inherits a WORD operand type. An explicit BYTE PTR selects the actual angle
field width. It produces no accepted object; the corrected final source has
two fresh successful producers. The source uses a genuine far HUD call;
TLINK itself produces the observed NOP/PUSHCS/CALL sequence. Neither that
sequence nor a fixup is supplied or edited manually.

The intermediate b producer already matches the130 bytes. It predates the
additional real C++ public spelling used by existing callers, so it is retained
as historical evidence only. Final c source exports both compatible names at
the same entry and has two fresh producers plus the normal shared negative.
No generated instruction or relocation is edited.

Receipt: `.analysis/asm-replays/main-shot-helpers-c/receipt.json`, SHA-256
`7846bdd8be698e8f1ce5193579ca16aab1b13f23d4a7cacf2176b613bb4a243d`.
Native proof: `.analysis/shot-helpers-native-review.json`, SHA-256
`547b15bff857e1bb7d6c5300b4a413c3029c7a0e6f0530eb8b128a83447845c4`.

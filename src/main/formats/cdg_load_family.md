# CDG single/batch resource loading and single-slot release

Complete original 16-bit register-source reconstruction of the TH05 MAIN
shared CDG resource loader family at `[15118,1526E)`, including the true
`CDG_LOAD_SINGLE_NOALPHA` and `CDG_LOAD_ALL_NOALPHA` fast entrypoints,
`CDG_LOAD_SINGLE`, internal near `CDG_READ_SINGLE`, `CDG_LOAD_ALL` and
`CDG_FREE` far Pascal callbacks. ReC98 `th04/formats/cdg_load.asm` provides
the complete source-backed semantics, with 16-byte CDG records and native
master.lib file/HMEM resource APIs. No resource payload or external callee
code is copied into this source.

## 2026-11-11: complete 342-byte source-backed assembly recovery

The source `cdg_load_family.asm` reconstructs the **entire continuous native
CODE family** `[15118,1526E)` from real source-level operations in the pinned
ReC98 `th04/formats/cdg_load.asm`. The complete object has six visible
function labels/entries: `CDG_LOAD_SINGLE_NOALPHA` (+0), `CDG_LOAD_SINGLE`
(+6), the internal `CDG_READ_SINGLE` near helper (+102),
`CDG_LOAD_ALL_NOALPHA` (+190), `CDG_LOAD_ALL` (+196) and `CDG_FREE`
(+288); the last instruction/EVEN byte ends at +342. The first and fourth
labels are real five-byte toggles of the shared `cdg_noalpha` flag, followed
by original even CODE alignment. Their fallthrough entrypoint semantics are
preserved, not replaced by defensive returns or independent stubs.

The single-image loader receives genuine far filename, slot and image index
arguments, opens the original CDG resource, reads the full 16-byte CDG
header, computes the signed/unsigned image seek offset according to colors,
alpha or combined layout, and invokes the near read helper. The helper
allocates and reads the true 16-bit alpha/colors segments, respecting the
source's original `cdg_noalpha` flag and four-color-plane count. The
batch loader iterates the actual image count from each CDG header, retaining
the 12-byte `REP MOVSD` metadata copy and same-CS CDG_FREE call. The
single-slot release checks/clears the original two far data segments.
No new slot, image data, file content, allocation policy, error handling or
resource mutation is introduced.

The final source uses semantic named constants for the genuine 16-byte
record, 64-slot bank, original plane layout fields and three-DWORD metadata
copy. All master `FILE_*` and `HMEM_*` providers are external at their native
far offsets; `cdg_slots`/`cdg_noalpha`/`cdg_images_to_load` are real
DGROUP labels at DS306C/0848/346C. The source-free binder provides only
outside function addresses, the true SHARED frame `14AB`, DGROUP frame
`209D`, and reserved foreign CODE after this family. It emits no file,
resource, DATA or external function bytes.

The original contains **five NOPs** at scope-relative offsets
`[5,15,101,195,341]`. Four belong to true even CODE alignment; the fifth
(+15) is explicitly preserved in ReC98 ahead of the original same-CS CDG_FREE
call relaxation. Omitting the latter made the provisional source two bytes
short: the initial NOP was lost, which also suppressed the subsequent
EVEN NOP. Restoring the genuinely documented instruction causes native
TASM/TLINK to produce both at their authentic positions; no target-byte
padding, manual relocation edit or post-link patch is used.

The focused replay
`.analysis/gpt-web-cdg-load-family-342-b/receipt.json` contains **two fresh,
independently compiled real TASM32/TLINK producers**. Both match **342/342 raw
bytes**, all 14 native ordered relocation sites, every public boundary and
full producer LEDATA coverage. Its own compiled negative changes the
three-DWORD CDG metadata copy into two DWORDs and is correctly rejected.
That proves **337 reviewed ASM instruction bytes** plus five checked but
uncredited NOPs; no table or initialized DATA is credited. The separately
accepted CDG_FREE_ALL function at `[1526E,1527C)` remains a distinct
14-byte owner, never bundled into this receipt. Historical original authoring
language remains uncertain beyond the preserved ReC98 assembly and native
source/relocation proofs.

# TH05 reconstruction handoff — 2026-11-11

## Start here

The working branch is `main`. Read [AGENTS.md](../AGENTS.md) for the current
lightweight workflow and [ORACLES.md](ORACLES.md) for exactness criteria. The
source of truth is the **current acceptance ledger**, not older exploratory
notes or a previous agent's handoff:

- `config/accepted_units.json`, `config/accepted_units.op.json`,
  `config/accepted_units.maine.json` and `config/accepted_units.zun.json`:
  accepted natural C/C++ (and scoped initialized DATA).
- `config/accepted_asm_families.json` and
  `config/reviewed_asm_families.json`: separately reviewed ASM ownership.
- [Generated progress](PROGRESS.md) and
  [gapless ownership map](../resources/ownership.json): coverage and unknown
  ranges. The global authored-byte denominator is **not yet established**;
  do not claim a percentage from the bounded accepted totals.

Use `git status -sb` before editing, including dirty files; no other agent is
working in this repository. Preserve and integrate legitimate dirty work.
Use only targeted complete-function native replay after changing executable
inputs; **never run the full cold-replay set by default**. For documentation
alone, inspect the diff and use lightweight validation. Commit substantive
progress as `gpt-web: <description>`. Local Git checkpoints are not Git pushes.

**MAIN large `exec` / `farheap` vendor OMF records reviewed:** Complete original 933-byte `exec` and 1,115-byte `farheap` CODE segment ranges were reconstructed from pinned CL.LIB LIDATA/LEDATA, all FIXUPP and true linker context. **2,040 bytes of actual object-written vendor CODE-segment material** have explicit ownership; the two original `CS:` runtime state gaps (**2 + 6 bytes**) remain *unknown*, with no invented source bytes, no game-authored credit and no full cold replay. See [large vendor review](reconstruction/CL_VENDOR_OWNERSHIP.md) and `scripts/review_vendor_reserved.py`.

**ZUN source-built envelope integration:** Independently accepted positive producers now cover **13,250 of 18,116 physical bytes** in one nonoverlapping synthetic launcher, including 1,698 bytes inside `-S` (322 C++ `cfg_init` CODE, 320 C++ initialized DATA and 1,056 original Master vendor CODE). The remaining **4,866 bytes** stay zero-filled in four scoped gaps; these include the open **269-byte C++ `main()`**. Physical coverage includes separately reviewed assets/vendor code, so it is not an authored-code percentage or whole-COM acceptance. See [latest source-only integration](../src/zun/resident/semantic_data.md) and [original outside-`-S` proof](../src/zun/launcher/README.md).

**ZUN outer COMCSTM wrapper accepted:** 39-byte original header, 264-byte readable CP932 help and complete 68-byte vendor startup stub all match two native TASM/TLINK producers. Of **371 compared source-owned bytes**, 71 are CODE and 300 are semantic header/help text; the 17,745-byte inner COM is a foreign zero placeholder and remains outside this credit. See [outer wrapper source and focused proof](../src/zun/launcher/outer.md).

**ZUN inner dispatcher and catalog accepted:** 550 original bytes of command parser, catalog and transfer CALL, plus the original 8-byte relocation-free `REP MOVSB` transfer helper, verified by two actual TASM/TLINK producers. The discontiguous **558 compared bytes** contain **213 instruction** and **345 semantic directory/message bytes**; **17,187 foreign child bytes are explicitly excluded**, and the global authored denominator is unchanged. See [dispatcher source and focused acceptance](../src/zun/launcher/README.md).

**ZUN `-O` PMD/ADPCM RAM diagnostic accepted:** Complete **926-byte** standalone COM, including **892 CODE instruction bytes**, **34 initialized signature/status bytes**, and **42 runtime BSS bytes** (not part of the file). All ten procedure boundaries and full MZ-free COM bytes match two independent TASM/TLINK producers, with a rejected semantic timing mutation. See [ADPCM RAM diagnostic](../src/zun/adpcm/README.md); no global authored credit inferred.

**ZUN `-G` gaiji child accepted:** Complete **8,377-byte** embedded COM, including **75 instruction bytes**, **1 linker-alignment byte**, **109 semantic message bytes**, and **8,192 separately reviewed font-resource bytes**. The exact bitmap is expanded only inside private `.analysis` from a pinned reference image, never copied into public source. Focused TASM/TLINK proof and compiled negative in [ZUN gaiji installer](../src/zun/gaiji/README.md); no global authored credit inferred.

**ZUN `-I` interrupt child accepted:** One complete **1,009-byte** standalone COM reconstruction, containing **452 compared CODE bytes** (2 uncredited NOPs) and **557 initialized signature/message bytes**. See [interrupt guard](../src/zun/interrupt/README.md) and `config/zun_interrupt_acceptance.json`. Historical source-origin and global authored-code credit remain separately unresolved.

**ZUN `-S` Master file I/O and DOS services exact:** Thirteen complete routines (including **166-byte `FILE_WRITE`**, DOS error/string services, and two native aliases) now reproduce all **830 bytes** at `0698..09D6` (**823 vendor instructions + 7 checked NOPs**), superseding the prior 728-byte scope without double credit. Together with `GRAPH_CLEAR` and resident-memory search/allocation, **1,056 consecutive bytes** at `05B6..09D6` have exact Master library source. The 269-byte ZUN C++ entry remains open. See [Master file and DOS sources](../src/zun/resident/file_family_native.md).

**ZUN `-S` Master graphics and resident memory exact:** `GRAPH_CLEAR` (36 bytes), `RESDATA_EXIST` (72) and `RESDATA_CREATE` (118 including `EVEN`) now produce **226/226 original bytes** at `05B6..0698`, with a rejected native source mutation and no duplicate vendor code credit. See [graphics/memory providers](../src/zun/resident/resdata_native.md). The separate 269-byte C++ entry is still open.

**ZUN `-S` original CRT vendor startup exact:** The original C0T.OBJ now naturally relinks in its true tiny-model `_INIT_`/BSS context: the full **615-byte startup CODE region** and **110-byte initialized CRT DATA** match exactly under two native TASM/TLINK producers and a rejected source-layout negative. Only **613 CODE-segment bytes plus 110 initialized DATA bytes** are real OMF source writes; a two-byte writable `CS:` state slot remains unknown. See [C0T CRT native proof](../src/zun/resident/crt_native.md). This is vendor provenance, not authored C++ credit.

**ZUN `-S` authored initialization DATA exact:** The complete **320-byte** native C++ `_DATA` contributor at COM `16BE..17FE` now matches semantic configuration defaults, IDs, filenames, title and Japanese status messages through real TCC/TLINK/CP932; it earns DATA, **not instruction**, credit. See [ZUN resident semantic DATA](../src/zun/resident/semantic_data.md).

**ZUN resident `main()` source remains unaccepted:** Two private real TCC `-c`/TLINK producers now generate **269/269 exact `main()` bytes** under the restored original CRT layout, with an effective compiled one-byte negative. However, they require the three explicit *artificial optimization barriers* present in the ReC98 reference. Those constructs are not historical game behavior and are **not committed or accepted as authored C++**. Sixteen natural no-op-free scope variants still generate 260 bytes. See [precise compiler diagnostic and source-origin limit](../src/zun/resident/initialize.md); do not relabel exact binary diagnostics as accepted source.

## Recent accepted code: do not reopen old failure notes as active blockers

The following statuses were checked against the acceptance manifests and
ledgers as of this handoff. Each accepted owner has its own complete-scope
evidence; referenced function sizes are compared extent bytes, not
necessarily all authored bytes where padding is present.

| Area | Current accepted scope | Maintained evidence |
| --- | --- | --- |
| MAIN EMS Boss faceset | Full **154-byte** C++ function at `B9CC..BA66`; original ordered fixups `[71,24,133,114]` | [EMS review](../src/main/ems/ems.md) |
| MAIN stage session | **803-byte** initializer; genuine four-function 1,826-byte compiler context | [Stage context](../src/main/runtime/stage_session_context.md) |
| MAIN shot laser raster | **100-byte** `SHOT_LASER_PUT_RAW` at `DDF4..DE58`, 98 authored ASM bytes and two checked `EVEN` NOPs | [Laser raster source](../src/main/player/shot_laser_put.md) |
| MAIN shot collisions | **399 + 210** complete C++ functions, individual exact ordered fixups | [Shot collisions](../src/main/player/shot_runtime.md) |
| MAIN Mai/Yuki tracking | **186-byte** C++ function; TCC `-S` → TASM32 restores fixup order `[38,130]` | [Later attacks](../src/main/boss/mai_yuki/later_patterns.md) |
| MAIN performance selectors | **76-byte** complete reviewed ASM family at `CF7A..CFC6`; **74 authored instruction bytes**, two uncredited `EVEN` NOPs | [Performance/selector family](../src/main/runtime/playperf_select.md) |
| MAIN player physics | **280-byte** complete invalidation/movement native ASM at `C9BA..CAD2`; **239 instruction + 40 jump-table** bytes, original fixup `[60]` | [Player movement](../src/main/player/region_register.md) |
| MAIN stage DWORD clear | Complete **23-byte** near original-register `clear_dwords()` at `CF62..CF79`; actual SS arguments and `REP STOSD` | [Stage pool clear](../src/main/runtime/clear_dwords_exact.md) |
| MAIN motion updates | Two **32-byte** exact C++ implementations at `BE1A..BE3A` and `1527C..1529C`; real AX/DX Pascal point return | [Motion register ABI](../src/main/math/motion_register.md) |
| MAIN tile-ring setter | Full **79-byte** far-Pascal C++ setter at `BEA4..BEF3`, real tile-ring and scroll state, empty fixups | [Tile-ring setter](../src/main/scroll/ring_set.md) |
| MAIN scrolling | **204-byte** tile-ring update + **115-byte** scroll driver, independently exact | [Ring](../src/main/scroll/ring_update.md), [driver](../src/main/scroll/driver.md) |
| MAIN dialog opcode | Full **456-byte** `dialog_op()` at `13B82..13D4A`, including natural one-byte switch alignment, full 30-byte table and literal ten-site fixup order; 455 authored bytes | [Interpreter](../src/main/dialog/opcode.md) |
| MAIN dialog graphics | **88 + 56 + 74** contiguous bytes, three source-owned graphics functions | [Dialog runtime](../src/main/dialog/runtime.md) |
| MAIN EGC copy setup | **63-byte** near C++/hardware register routine at `BC2E..BC6D`, empty fixups | [EGC hardware](../src/main/tile/egc_copy_setup.md) |
| MAIN MPN image upload | **69-byte** exact C++ at `E57C..E5C1` with original fixups `[12,32,61]` through unmodified TCC `-S`/TASM32 | [MPN uploader](../src/main/formats/mpn_upload.md) |
| MAIN text bitmap painter | Full **98-byte** `bb_txt_put_8_raw` exact reviewed ASM at `E51A..E57C`; **96 authored** bytes and two checked NOPs | [Text bitmap drawing](../src/main/formats/bb_text_put.md) |
| MAIN Boss BB tile masks | Full **232-byte** two-function original-register GRCG put/invalidate ASM at `F968..FA50`, ordered fixups `[17]` | [Boss bitmap masks](../src/main/tile/bb_mask_family.md) |
| MAIN point popup digits | **58-byte** original-register decimal converter at `15870..158AA`; **57 authored** ASM bytes and one checked `EVEN` | [Digit converter](../src/main/pointnum/digits_register.md) |
| MAIN/OP GRCG hardware modes | MAIN **38-byte** three-function family (36 authored ASM); OP **26-byte** direct color helper, original I/O and zero-credit alignment | [GRCG mode/color](../src/shared/hardware/grcg_modecol_exact.md) |
| MAIN item splash initialization | Complete **26-byte** C++ pool clear at `16362..1637C`, native `REP STOSW` and one-byte XOR encoding recovered | [Splash init](../src/main/item/splash_init_register_exact.md) |
| MAIN item splash pixel | Complete **28-byte** original-register near-ASM at `E152..E16E`, exact AX/DX/ES point mask and no fixups | [Item splash dot](../src/main/item/splash_dot_exact.md) |
| MAIN Gather graphics primitives | **122-byte** original ASM family at `15312..1538C`, 120 authored bytes and two checked NOPs | [Gather raster](../src/main/gather/raster_primitives.md) |
| MAIN enemy bullet-template transfer | Complete **24-byte** natural C++ near-Pascal register copy at `16BCF..16BE7`; genuine seven-word `REP MOVSW` | [Enemy template transfer](../src/main/enemy/template_push_exact.md) |
| MAIN bullet/Gather invalidation | Full **168-byte** reviewed original ASM at `E40E..E4B6`, no alignment or relocations | [Bullet/Gather dirty tiles](../src/main/bullet/gather_invalidate.md) |
| MAIN Louise backdrop callback | **14-byte** stage-two near ASM at `14AAA..14AB8`, identified by native `stage2_setup()` pointer | [Louise fill](../src/main/boss/backdrop_fill_louise.md) |
| MAIN Alice/Yumeko backdrop fills | **28-byte** exact original ASM, two complete near callbacks `C41E..C43A` | [Alice/Yumeko graphics](../src/main/boss/backdrop_fills_alice_yumeko.md) |
| MAIN Sara/Mai-Yuki background | **108-byte** two-function GRCG family `BEF4..BF60`, **104 authored** ASM bytes and four checked `EVEN` NOPs | [Early Boss backdrop](../src/main/boss/backdrop_fills_early.md) |
| MAIN Shinki backdrop fills | **94-byte**, three-entry GRCG family at `C68A..C6E8`; 93 authored ASM bytes and one checked NOP | [Shinki backdrop](../src/main/boss/shinki/backdrop_fills.md) |
| MAIN Mima bomb drawing | **172-byte** original ASM primitives at `1045C..10508`; 171 authored bytes plus one uncredited NOP | [Mima raster primitives](../src/main/player/mima_bomb_primitives.md) |
| MAIN Mima bomb backdrop | Four-entry **226-byte** GRCG family at `1052C..1060E` exact reviewed ASM; **224 authored** bytes, two uncredited NOPs | [Mima backdrop](../src/main/player/mima_backdrop.md) |
| MAIN sparks | **98-byte** random-spawn and **106-byte** radial-spawn ASM families; distinct 22-byte C++ player wrapper | [Random](../src/main/boss/sparks_add_random.md), [circle](../src/main/boss/sparks_add_circle.md) |
| OP/MAINE .PI loader | One complete **50-byte** far-Pascal C++ file loader per binary, original far-call fixup `[42]` | [PI file load](../src/shared/graphics/pi_load_exact.md) |
| OP/MAINE rectangle-copy setup | Complete **63-byte** C++/inline-hardware helper in each artifact, directly following the accepted 124-byte public copy function | [EGC rectangle setup](../src/shared/hardware/egc_rect_setup.md) |
| OP/MAINE PI EGC setup | One complete **65-byte** C++ register setup per binary, original EGC far-call fixup `[3]` | [PI EGC setup](../src/shared/graphics/pi_mask_egc_setup.md) |
| OP CDG monochrome renderer | **74-byte** exact C++ at decoded `E114..E15E`, signed VRAM positioning and native `REP MOVSD` loop | [CDG nocolors](../src/shared/graphics/cdg_put_nocolors_exact.md) |
| OP/MAINE plain .PI draws | Four complete C++ functions; per binary **47-byte** full + **70-byte** quarter draw, excluding the original alignment NOP | [Plain PI wrappers](../src/shared/graphics/pi_plain_wrappers.md) |
| OP/MAINE masked .PI draws | Per binary, two complete C++ wrappers **50 + 73 bytes**, matching original PI-buffer and rowloop ABIs | [Masked PI wrappers](../src/shared/graphics/pi_masked_wrappers.md) |
| OP piano pressed-key top masks | **12-byte** complete semantic CODE data at `DB01..DB0D`, chromatic pitch geometry, exact TASM/OMF/negative; zero instructions | [Piano top masks](../src/op/piano/pressed_top.md) |
| OP Music Room B-plane restore | Complete **30-byte** C++ `nopoly_B_put()` at `BFF6..C014`; direct TCC `-c` preserves native XOR encoding | [Music saved plane](../src/op/music/nopoly_put_exact.md) |
| OP Music Room piano C++ | **218 + 116-byte** initializer/renderer at `D894..D9E2`, plus **30-byte** exact near note lookup at `DA12..DA30` | [Setup](../src/op/piano/setup_exact.md), [render](../src/op/piano/render_exact.md), [note](../src/op/piano/note_register.md) |
| OP/MAINE background snapshot | Per binary, complete **104-byte Snap + 53-byte Put** C++ from one real TCC translation unit, original ordered fixups `[15,26,37,48]` | [Background transfer](../src/shared/hardware/bgimage_transfer.md) |
| MAIN/OP/MAINE CDG | Per binary, **342-byte** load/read/free family + **14-byte** free-all; reviewed ASM with real local provider addresses | [Loader](../src/main/formats/cdg_load_family_op_maine.md), [free-all](../src/main/formats/cdg_free_all_op_maine.md) |
| MAIN STD script loader | **184-byte** near C++ `std_load()` at `C742..C7FA`, 386 `MOVZX` and original ordered fixups `[43,173]` via TCC `-S`/TASM32 | [STD loader](../src/main/formats/std_load.md) |
| OP score encoder | **100-byte** near C++ `scoredat_encode()` at `C87E..C8E2`, exact original direct-object fixup order `[43,35]` | [Score encoder](../src/op/hiscore/encode_exact.md) |
| MAIN high-score insertion | **168-byte** natural C++ `hiscore_continue_enter_raw()` at `C8F0..C998`, real TCC `-S`/TASM32 compilation, no fixups | [Insertion source](../src/main/score/continue_raw.md) |
| MAIN high-score display | **22-byte** `hiscore_load()` at `C9A4..C9BA` exact C++; original `BX`/`CX` digit loop | [High score loader](../src/main/score/hiscore_load.md) |
| MAIN far vector pair | **69 + 90** complete exact C++ bytes; unmodified TCC `-S` / TASM32 `MOVSX` output, original second fixup `[24]` | [Vector pair](../src/shared/math/vector_far.md) |
| MAINE cutscene script VM | **1,555-byte** full C++ `script_op()` including 64-byte switch table at `A9C3..AFD6`, exact 42-site relocation order; unified 2,848-byte CODE proof | [Cutscene VM](../src/maine/cutscene/cutscene.md) |
| MAINE cutscene EGC setup | Complete **52-byte** near C++ at `A6D1..A705` with original `EGC_ON` fixup `[6]`; the separately accepted interpreter now matches the complete unified CODE module | [EGC setup](../src/maine/cutscene/egc_setup_exact.md) |
| MAIN/OP/MAINE horizontal flip LUT | Three complete **30-byte** original-register ASM lookup generators; 90 authored bytes, empty fixups | [Bit-flip LUT](../src/shared/hardware/hflip_lut_generate.md) |
| MAIN/OP/MAINE SE reset | **11-byte** exact `snd_se_reset()` far C++ per binary; 33 new instruction bytes, three outside `EVEN` NOPs | [Sound reset](../src/shared/sound/se_reset_exact.md) |
| MAIN/OP/MAINE sound effects | Per binary, **57-byte** SE play + **76-byte** SE update exact C++; all original update fixups `[43]` | [Sound controller](../src/shared/sound/se.md) |
| MAIN/OP/MAINE input | Per binary, **262-byte** BIOS/joystick scanner reviewed ASM; **16 + 42-byte** held/input-wait functions accepted C++ | [Scanner](../src/shared/hardware/input_sense_op_maine.md), [wait](../src/shared/hardware/input_wait_context.md) |

Other previously reported blockers are **already resolved**: Shinki ball
updater **220** and wing preparation **386**, Yumeko sword updater **283**
(reviewed ASM), generic Boss defeat **414** and player collision **43**,
MAINE registration menu **1,034**, MAINE Staff controller **991** and
updater/renderer **626/861**, and OP score decoder **169**. Check the
individual accepted IDs before treating old candidate headings as current.
The 55-byte BB loader, 55-byte near vector helper and 40-byte scroll
coordinate helper are exact **reviewed ASM**, although alternative ordinary
C++ source candidates for those functions remain inexact.

## Genuine open work

**Dialog opcode resolved.** The 456-byte interpreter now has full source/
compiler evidence (new accepted row above); do not reopen the earlier missing
switch-table zero as a live blocker. Only the complete opcode extent is
accepted from the joined 1,123-byte context. Its following runner has its
own accepted standalone owner because the joined TU's runner fixup order
differs; this does not invalidate the independently accepted opcode.

**STD loader resolved:** The full 184-byte MAIN `std_load()` now has exact natural C++ at `C742..C7FA` through TCC `-S`/TASM32 and genuine `[43,173]` fixups. See [loader source and receipt](../src/main/formats/std_load.md).

**Score insertion resolved:** The full 168-byte MAIN `C8F0..C998` is now exact C++ through genuine TCC `-S`/TASM32, including original eight DWORD string copies and ordered empty fixups. See [source and focused replay](../src/main/score/continue_raw.md).

**Far vector pair resolved:** MAIN `14AB8..14B58` contains **159 newly accepted C++ instruction bytes** across two complete near-adjacent far-Pascal functions. TCC `-S`/TASM32 reproduces native 386 `MOVSX` and the original `[24]` second-function fixup; the one `14AFD` EVEN byte is outside both owners. See [complete source and receipts](../src/shared/math/vector_far.md).

**MAINE cutscene interpreter resolved:** `script_op()` now has a complete **1,555-byte C++ exact owner**, including all 42 original ordered far-call fixups and its 64-byte sparse switch. Recovering the original unified CODE group also matches the full 2,848-byte eleven-function module and all 64 ordered fixups; the nine previously accepted functions were revalidated with unchanged behavior. See [unified cutscene review](../src/maine/cutscene/cutscene.md) and [compiler-buffer evidence](../src/maine/cutscene/script_op_assembler_context.md).

**Other unknown intervals.** The [ownership map](../resources/ownership.json)
contains actual unowned code/data ranges. Examples requiring function-boundary
review include remaining original-language classification and data boundaries, not the already accepted MAIN MAP loader `E5C2..E606`. The STD loader, far vector pair, player region `C9BA..CAD2`, and Gather/point-popup raster subregions have accepted owners; the `14AFD` vector alignment byte remains uncredited. Use original
ReC98/source and native control-flow evidence before claiming ownership or
credit. Further useful natural-C++ recovery opportunities can be found in
[unaccepted candidates](reconstruction/UNACCEPTED_COHORTS.md). Do not
reinvestigate Shinki or Staff functions already accepted simply because an
old intermediate note calls them “unaccepted.”

## Practical workflow and storage

1. Inspect only the intended files and the current Git status. Prefer
   complete Boss/controller functions **and** relevant leaf functions;
   choose work by potential real source coverage, not only function size.
2. Compare the **entire** changed original function and literal relocation
   order using `scripts/replay_units.py --artifact main --units ID --output
   .analysis/unit-replays/UNIQUE_NAME`. Use `--artifact op` or `--artifact
   maine` for other binaries; reviewed original-ASM units use
   `scripts/replay_asm_family.py --unit ID --native-review FILE --output DIR`.
   Keep the meaningful compiled negative, the source inputs and original
   MAP/OMF/MZ evidence. Do not substitute “same length” for byte exactness.
3. On a genuine pass, adopt the focused receipt, update ownership/progress
   with repository scripts, run the relevant checks, commit with the requested
   `gpt-web:` prefix and leave the tree consistent. For pure prose cleanup,
   no compiler or new receipt is necessary.

The ignored `.analysis/` cache includes a private, attested Borland toolchain
and Wine prefix, target bytes/decoded views, Ghidra context and many exact
producer receipts. **Keep** those prerequisites, all accepted evidence,
meaningful unresolved compiler-context diagnostics and the tracked source /
ledgers. At the 2026-11-11 cleanup, **908 unreferenced, non-accepted `gpt-web-*`
trial folders** were removed locally, reducing `.analysis` from about
**1,503 MiB to 655 MiB** (848.6 MiB freed). Those disposable builds can be
regenerated from maintained source; do not interpret their absence as lost
acceptance. The tracked Git commit contains prose/source/ledger changes,
while ignored cache deletion is local and is not itself represented by Git.

Historical per-function notes remain valuable for source semantics and
failed hypotheses, but their older intermediate conclusions should always
be read alongside the latest accepted section and the current ledger.

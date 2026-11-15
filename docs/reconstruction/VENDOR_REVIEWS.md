# Vendor and resource ownership reviews

Index of the reviews that identify vendor bytes (master.lib 0.23, Borland's
runtime) and resources in the original executables. These bytes are compared
exactly but carry no authored credit. Each review's decision and extents
live in its `config/` file; its script re-checks them (`--check`) and is the
place to read the details. The Borland C/runtime model is described in
[CL_VENDOR_OWNERSHIP.md](CL_VENDOR_OWNERSHIP.md) and
[CL_DATA_OWNERSHIP.md](CL_DATA_OWNERSHIP.md).

## master.lib code

| Review | Check | Decision |
| --- | --- | --- |
| Circle fill from unchanged original Master source | `scripts/review_master_primary_circlefill.py` | `config/reviewed_master_primary_circlefill.json` |
| Circle outline from unchanged original Master source | `scripts/review_master_primary_circlex.py` | `config/master_primary_circlex_ownership.json` `config/reviewed_master_primary_circlex.json` |
| Four source-backed Master EGC shifts | `scripts/review_master_egc_shifts.py` | `config/master_egc_shifts_ownership.json` `config/reviewed_master_egc_shifts.json` |
| Master 0.23 procedure ownership proposal | `scripts/review_master.py` | `config/master_vendor_ownership.json` |
| Master EMS transfer wrappers: source-backed vendor review | `scripts/review_master_ems_transfers.py` | `config/reviewed_master_ems_transfers.json` |
| Master LARGE_BYTE: 16 bytes of CODE-class lookup data | `scripts/review_master_large_byte.py` | `config/reviewed_master_large_byte.json` |
| Master file, DOS and heap routines: exact original MAIN ownership | `scripts/review_master_io.py` | `config/master_io_ownership.json` `config/reviewed_master_io.json` |
| Native Master SUPER graphics source recovery — MAIN | `scripts/review_master_super.py` `scripts/review_master_super_helpers.py` | `config/master_super_helpers.json` `config/master_super_ownership.json` `config/reviewed_master_super.json` |
| Original MAIN PF archive interception | `scripts/review_master_pf.py` | `config/master_pf_ownership.json` `config/reviewed_master_pf.json` |
| Original Master 0.23 machine, VRAM, joystick and palette DATA | `scripts/review_master_machine_graphics_palette.py` | `config/reviewed_master_machine_graphics_palette.json` |
| Original Master BGM source recovery in TH05 MAIN | `scripts/review_master_bgm.py` | `config/master_bgm_ownership.json` `config/reviewed_master_bgm.json` |
| Original Master graphics and display in TH05 MAIN | `scripts/review_master_grcg.py` | `config/master_grcg_ownership.json` `config/reviewed_master_grcg.json` |
| SIN8 initialized vendor DATA proposal | `scripts/review_master_sin8.py` | `config/master_sin8_ownership.json` `config/reviewed_master_sin8.json` |
| Seventeen further complete original Master functions: 1,079 CODE bytes | `scripts/review_master_gap_functions.py` | `config/master_gap_functions_ownership.json` `config/reviewed_master_gap_functions.json` |
| Source-backed Master additions: ownership proposal | `scripts/review_master_additions.py` | `config/master_vendor_additions.json` `config/reviewed_master_additions.json` |
| Source-exact Master machine detection and buffered I/O | `scripts/review_master_machine.py` | `config/master_machine_ownership.json` `config/reviewed_master_machine.json` |
| Three original Master circle helpers: 223 complete source-written CODE bytes | `scripts/review_master_circle_helpers.py` | `config/master_circle_helpers_ownership.json` `config/reviewed_master_circle_helpers.json` |

## master.lib data and BSS reservations

| Review | Check | Decision |
| --- | --- | --- |
| Eleven original Master literal initialized-DATA scopes in MAIN | `scripts/review_main_master_literal_tables.py` | `config/main_master_literal_tables_ownership.json` `config/reviewed_main_master_literal_tables.json` |
| HFLIP LUT: three complete 256-byte game-source BSS arrays | `scripts/review_hflip_lut_reservations.py` | — |
| MAIN: original Master ATAN8 table, 256 source-written DATA bytes | `scripts/review_main_atan8_data.py` | `config/main_atan8_data_ownership.json` `config/reviewed_main_atan8_data.json` |
| Master 0.23 memory allocator's initial DATA words | `scripts/review_master_mem_initial.py` | — |
| Master 0.23 sprite/superimpose initial state in MAIN, OP and MAINE | `scripts/review_master_superpa_initial.py` | `config/reviewed_master_superpa_initial.json` |
| Master 0.23: original eight-word clipping state in three executables | `scripts/review_master_clip_data.py` | `config/reviewed_master_clip_data.json` |
| Master BFNT file signature: complete OP and MAINE initialized resources | `scripts/review_op_maine_bfnt_id.py` | — |
| Master BGM note/length tables: OP and MAINE | `scripts/review_master_bgm_literal_data.py` | `config/master_bgm_literal_op_maine_ownership.json` `config/reviewed_master_bgm_literal_op_maine.json` |
| Master PF buffer state and random seed in three TH05 MZ executables | `scripts/review_master_pf_rand_initial.py` | — |
| Master SUPERBFT: 32-byte BFNT header reserve in all three EXEs | `scripts/review_master_superbfnt_header.py` | `config/reviewed_master_superbfnt_header.json` |
| Master file handle and sharing defaults in three EXEs | `scripts/review_master_file_initial.py` | `config/reviewed_master_file_initial.json` |
| Master text-VRAM and VSYNC initialized DATA in three executables | `scripts/review_master_tx_vs.py` | `config/reviewed_master_tx_vs.json` |
| Original Master 0.23 BGM global: three complete unwritten 108-byte structures | `scripts/review_master_bgm_global_reservations.py` | — |
| Original Master ATAN8: MAINE's complete 256-byte native lookup | `scripts/review_maine_atan8_initial.py` | `config/reviewed_maine_atan8_initial.json` |
| Original Master BFNT entry: 322 complete MAIN CODE bytes | `scripts/review_main_bfnt_entry.py` | `config/main_bfnt_entry_ownership.json` `config/reviewed_main_bfnt_entry.json` |
| Original Master BGM track/effect state: 198 unwritten bytes in each EXE | `scripts/review_master_bgm_track_bss.py` | — |
| Original Master SUPERPA pattern storage: 6,144 verified unwritten bytes | `scripts/review_master_superpa_reservations.py` | `config/reviewed_master_superpa_reservations.json` |
| Original Master byte masks in OP and MAINE | `scripts/review_master_byte_mask.py` | `config/master_byte_mask_op_maine_ownership.json` `config/reviewed_master_byte_mask_op_maine.json` |
| Source-backed BGM timer divider and OP palette resource ID | `scripts/review_master_timer_and_respal.py` | — |
| Source-backed Master EDGES: 34-byte raster masks in all three EXEs | `scripts/review_master_edges_initial.py` | — |
| Source-backed Master JS/PAL/VSYNC/MEM uninitialized state in three MZs | `scripts/review_master_compact_bss.py` | `config/reviewed_master_compact_bss.json` |
| TH05 eight-slot PI image buffers: verified unwritten game storage | `scripts/review_pi_buffer_reservations.py` | — |

## Borland runtime

| Review | Check | Decision |
| --- | --- | --- |
| C0L.OBJ startup: source-backed foreign CODE in all three EXEs | `scripts/review_borland_c0_startup.py` | `config/borland_c0_startup_ownership.json` `config/reviewed_borland_c0_startup.json` |

## Vendor code inside game modules (context reviews)

| Review | Check | Decision |
| --- | --- | --- |
| Complete original Master SMEM, VSYNC and memory CODE in OP/MAINE | `scripts/review_context_memory_vsync.py` | `config/context_memory_vsync.json` `config/reviewed_context_memory_vsync.json` |
| Complete original SUPERPTR drawing procedures in OP and MAINE | `scripts/review_context_super_helpers.py` | `config/context_super_helpers.json` `config/reviewed_context_super_helpers.json` |
| Exact source-linked Master BGM timer/PSG functions in OP and MAINE | `scripts/review_context_bgm_timers.py` | `config/context_bgm_timers.json` `config/reviewed_context_bgm_timers.json` |
| Master RTC register modifier in OP and MAINE | `scripts/review_context_rtc_mod.py` | `config/reviewed_context_rtc_mod.json` |
| Native Master 0.23 functions in OP and MAINE | `scripts/review_context_master_large.py` | `config/context_master_large.json` `config/reviewed_context_master_large.json` |
| OP/MAINE original Master-derived no-Y-clip blitter: 392 CODE bytes | `scripts/review_context_graph_pack_noclip.py` | `config/context_graph_pack_noclip.json` `config/reviewed_context_graph_pack_noclip.json` |
| OP/MAINE: original Master machine-detection source, 868 bytes | `scripts/review_context_machine_detect.py` | `config/context_machine_detect.json` `config/reviewed_context_machine_detect.json` |
| OP/MAINE: original Master-derived display and archive hooks | `scripts/review_context_master_hooks.py` | `config/context_master_hooks.json` `config/reviewed_context_master_hooks.json` |
| Original Borland string runtime in TH05 OP and MAINE | `scripts/review_context_string_runtime.py` | `config/context_string_runtime.maine.json` `config/context_string_runtime.op.json` `config/reviewed_context_string_runtime.maine.json` |
| Original Master GRAPH_PI_LOAD_PACK in OP and MAINE | `scripts/review_context_pi_pack.py` | `config/context_pi_pack.json` `config/reviewed_context_pi_pack.json` |

## Resources

| Review | Check | Decision |
| --- | --- | --- |
| OP piano key masks and label font | `scripts/review_op_piano_resources.py` | `config/reviewed_op_piano_resources.json` |
| TH05 MAIN preshifted sprite resources | `scripts/review_main_sprites.py` | `config/reviewed_main_sprite_resources.json` |

## Findings without an ownership claim

| Review | Check | Decision |
| --- | --- | --- |
| CDG slots: the 1,024-byte `_cdg_slots` BSS array is not file-backed in MAIN, so it is not claimed | — | — |
| MAIN's private 32x32 cheeto worker at DE72..DF28: its register interface is known, the code is not accepted | — | — |

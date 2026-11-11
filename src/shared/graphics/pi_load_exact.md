# Exact TH05 packed .PI file loading in OP and MAINE

`pi_load(int slot, const char far *filename)` is a complete 50-byte far
Pascal C++ function at OP `DDD8..DE0A` and MAINE `EF80..EFB2`. It first frees
the old image through the original near `pi_free()` provider, keeping the
original `PUSH DI; PUSH CS; CALL` calling sequence. It then addresses the
4-byte-per-slot PI buffer pointer array and 72-byte-per-slot PI header array,
and passes the far filename and two DS-based pointers to the authentic
Master library `GRAPH_PI_LOAD_PACK` provider. Both programs' exact original
ordered MZ fixup list is `[42]`, for that far library call.

The source follows pinned ReC98 `th05/formats/pi_cpp_2.cpp`, using the real
near image slot and PI record layout. The pointer conversion from the near
SI/DI offsets to DS-based far parameters is performed by Turbo C++ 4.02,
not by supplying prepared target instruction bytes. `pi_free` and the
far library loader are foreign address-only symbols in the isolated binder.
The same-CS proof group allows the original near `pi_free` call to reach its
native address, without adding instructions or modifying the linked output.

Focused receipts:

- `.analysis/unit-replays/gpt-web-op-pi-load-exact-a/receipt.json`
- `.analysis/unit-replays/gpt-web-maine-pi-load-exact-a/receipt.json`

Each has two independent real TCC `-S`/TASM32/TLINK producers, complete
50-byte raw equality, the literal `[42]` relocation, original segment
frames/OMF scope, and a compiled negative changing the PI buffer-index
shift from two to three bits. Both negatives are rejected. Header storage,
image data and the following plain image drawing wrappers remain separate
owners; no full cold replay was run.

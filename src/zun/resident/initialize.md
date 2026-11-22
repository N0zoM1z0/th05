# ZUN resident entry (`-S`): accepted native C++ reconstruction

**Accepted: `zun-resident-main`, 269/269 bytes, two independent cold producers.**

`initialize.cpp` is the natural C++ source for the embedded resident `main()`.
The complete compiler context in `main_context.cpp` emits the original function
at outer `ZUN.COM` offsets `0x0E8D..0x0F9A`, corresponding to child COM
addresses `0x04A9..0x05B6`. Both retained producer rounds match all 269 bytes;
the original and candidate relocation lists are both empty. The compiled
`argc == 3` mutation is rejected.

The canonical unit, source inputs and receipt identity are in
`config/exact_units.zun.toml` and `config/accepted_units.zun.json`. The vendor
bytes around it are listed in the
[`-S` child ownership note](../../../docs/reconstruction/ZUN_CHILD_OWNERSHIP.md).

## Compiler context and source

`main_context.cpp` includes the actual translation-unit contributions in
original order:

1. `semantic_data.cpp` — 320 bytes of initialized semantic DATA.
2. `config.cpp` — the accepted 322-byte `cfg_init()` function.
3. `initialize.cpp` — the accepted 269-byte resident `main()` function.

The build uses the pinned Borland Turbo C++ 4.02 tiny model and native CP932
source input. Foreign CRT, DOS, resident-memory and graphics functions are
provided only as symbol bindings; the binding file supplies no implementation
or initialized target bytes. The maintained entry contains no inline assembly,
self-assignment, dummy calls or optimizer barriers.

The byte-exact control-flow detail is the `-R` removal branch:

```cpp
if(seg) goto resident_remove_success;
dos_puts2(ZUN_RESIDENT_NOT_FOUND);
return 1;
resident_remove_success:
dos_free(seg);
dos_puts2(ZUN_RESIDENT_REMOVED);
goto resident_success;
```

This natural forward branch preserves the original error-first layout while
allowing the compiler to share the final success return with normal
initialization. Earlier source rewrites either changed the shared error-call
tails or produced only a same-sized near match. The old artificial-barrier
experiment also matched bytes, but was never an acceptable game-authored
source reconstruction and is not present in the maintained source.

## Native ABI and behavior

The entry is near cdecl `int main(int argc, const unsigned char **argv)` in the
tiny model. Its argument pointers are near; the resident and DOS segment
providers retain their original segment-pointer declarations and calling
conventions. The function uses a twelve-byte local frame, saves SI/DI and
returns its status in AX.

The maintained control flow preserves the original behavior:

- Search for the nine-byte resident ID using the eight-paragraph resident
  allocation size, then print the logo and clear graphics.
- Interpret options only when `argc == 2`. The first argument must begin with
  `-` or `/`; `R`/`r` removes the resident and `D`/`d` enables debug. Trailing
  characters are not validated.
- A missing resident on removal, an unknown option, an already-installed
  resident or a failed allocation prints the original message and returns 1.
- On installation, preserve the provider-written ID area and clear bytes 10
  through 127. Byte 9 is deliberately outside the clearing loop.
- Free the allocation if `cfg_init()` fails. On success, propagate the debug
  flag to the resident debug byte and return 0.

## Related accepted ownership

- [`config.cpp`](config.cpp): exact 322-byte `cfg_init()`; its ABI and
  preserved defects are in [the directory notes](README.md).
- [`semantic_data.cpp`](semantic_data.cpp): exact 320-byte initialized DATA
  contribution.
- The original C0T startup relinks exactly: 613 source-written CODE bytes and
  110 initialized DATA bytes (`replay_zun_crt.py`). Its two-byte writable CS
  slot is a zero-credit reviewed gap.
- [Master resident memory and graphics](resdata_native.asm) (226 bytes) and
  [Master file/DOS providers](file_family_native.asm) (830 bytes) are
  reviewed ASM families.
- Borland CT.LIB and Master DATA members: see the
  [`-S` child ownership note](../../../docs/reconstruction/ZUN_CHILD_OWNERSHIP.md).

Every byte of the `-S` child is now classified in `resources/ownership.json`.

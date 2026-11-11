# Exact ZUN.COM `-S` resident C++ configuration and messages

A single natural Turbo C++ 4.02 `_DATA` contribution at COM runtime
`[16BE,17FE)` now matches **all 320 original initialized bytes**. In the
outer ZUN.COM file, this is `[20A2,21E2)`. It is not BSS, Master vendor
code, or an instruction sequence.

The maintained [C++ source](semantic_data.cpp) declares the original
`debug=0`, the complete six-byte `cfg_options_t` default, `miko.cfg`, the
nine-byte `KSOConfig` identifier, the two-line resident banner and all
seven Japanese status/error messages. The values follow the pinned ReC98
`th05/res_kso.cpp` and `th02/res_init.cpp`, with the existing exact resident
and configuration types. The readable UTF-8 source is explicitly converted
to CP932 in the isolated Borland producer, preserving the Japanese
punctuation, literal spaces and original line endings in the data segment.

The genuine TCC object has one ordinary `_DATA` OMF LEDATA, starting at
offset zero and containing **exactly 320 bytes**. In the native tiny COM
link context, C0T contributes its original `6Eh` initialized DATA bytes;
our compiler contribution therefore starts at runtime `16BE` immediately
after C0T, with all other vendor CODE and later DATA represented only by
foreign symbol/reservation addresses. No surrounding initialized bytes,
company strings, binary templates or target-derived values are supplied by
the binder.

The focused receipt is
`.analysis/unit-replays/gpt-web-zun-resident-semantic-data-d/receipt.json`.
Two independent native TCC/TLINK producers match the complete original
initializer and its MAP/OMF ownership. The compiled negative selects the
semantically different `ZUN_CFG_LIVES_MAX` instead of the default lives value;
the resulting initialized source byte is rejected by the strict oracle.

**This is 320 authored semantic DATA bytes and zero new instruction bytes.**
It is accepted separately from the previously recovered 322-byte
`cfg_init()` C++ function, the unresolved 269-byte C++ `main()`, and the
1,056-byte exact Master vendor graphics/memory/file/DOS code.

## Partial ZUN.COM source-built integration

After this DATA acceptance, the private integration of unchanged, previously
accepted original-compiler output verifies **13,250 source-built physical
bytes of the 18,116-byte ZUN.COM** without copying original target bytes.
Within `-S`, this comprises `cfg_init()` 322 C++ instruction bytes, the
1,056-byte original Master graphics/memory/file/DOS contributions, and this
320-byte semantic C++ initializer. The remaining four discontiguous native
intervals total **4,866 bytes**, including the unresolved 269-byte `main()`.
See `.analysis/gpt-web-zun-source-producer-cohort-integration-a/receipt.json`.
This is a private discontiguous source-coverage check, not a full EXE/COM
build, a byte-credit transfer from the 8,192-byte font asset, or a whole-file
acceptance.

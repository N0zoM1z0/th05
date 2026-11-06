# Cheeto mask kernel

The complete MAIN DE72..DF28 contribution is 182 bytes: 178 instruction bytes
and four EVEN NOPs at relative 41, 63, 71 and 93. All bytes compare normally;
the four alignment bytes receive zero authored credit. There are no tables,
ordered MZ fixups, owned DATA or BSS. The adjacent loader DE58..DE72 and scroll
provider beginning DF28 remain outside this reconstruction.

The public near fastcall interface takes pixel left in AX, ring top in DX and
cel in BX, with no stack arguments or callee cleanup. The accepted C++ Cheeto
renderer supplies ES=A800 and GRCG mode/color. Its clipping and ring conversion
supply valid screen positions; the kernel does not validate or clip inputs.
SI/DI, BP, DS/ES and IF/DF are preserved. AX/BX/CX/DX and arithmetic flags are
scratch; use of EAX makes no general promise about high register halves.
LODSD/STOSW/STOSB require clear DF.

The foreign DS:378A..3F8A bank holds sixteen 32x32 monochrome cels, each with
32 contiguous four-byte rows. Only its symbol and full foreign extent are
bound; no raster bytes are supplied or credited. Source SI advances through
the cel while destination DI advances by 80 bytes per row and wraps at 32000.
Even destination addresses use two word stores and an overflow byte; odd
addresses peel a byte before the two word stores. Rotate/mask/carry operations
preserve the original GRCG write behavior, including zero-valued writes.

## Source and origin decision

The two private row workers pass their remaining row count in CH and return
the DEC CH result in ZF directly to the driver's JNZ. CL, DL, BH, BL and DH
simultaneously carry bit phase, first-byte mask, word count and packed-byte
overflow. This flag-return protocol, the dword/string operations and distinct
aligned row paths support an inference of original handwritten assembly for
this complete kernel. The ordinary public fastcall ABI alone does not prove
that inference, and it does not transfer to the neighboring loader.

ReC98 th05/formats/bb_cheeto.asm provides candidate semantics. Its history
24b96cd9 relates this worker to TH04's 32x32 tiny renderer and identifies the
removed blank-row checks. The maintained source expresses shared ring and
word-shift operations as semantic macros; it does not emit opcode bytes.
The literal original source and assembler remain unproved.

A bounded comparison reuses identity-checked primary Master 0.23 sources
SUPERRPT.ASM, SUPERL1P.ASM and SUPER1PL.ASM. They contain related rotation,
mask and VRAM operations, but use stack interfaces and header/color or dynamic
plane/geometry formats, unlike this fixed 32-row dword mask kernel and private
CH/ZF helpers. This is not an exhaustive exclusion of library ancestry;
adaptation remains possible. TH04/ReC98 acceptance does not transfer here.

Native boundary, ABI, origin and pinned source review:
`.analysis/cheeto-put-native-review.json`, SHA-256
`64d2444a0655c2eb665b35380a998b6cd953eec80de03d84c6c269af7f4f3088`.

## Complete replay and adoption

The normal ASM gate passes two fresh producers and the own 31-row mutation.
Both positives match the complete 182-byte ordinary CODE contribution,
native CS/DS frames, group/public placement and empty ordered fixup list.
Normalized OMF, MAP and whole MZ output are deterministic. Normalization is
limited to dependency metadata; raw bytes and relocation order are compared
unchanged. The negative retains the full extent, publics and empty fixup list
but fails the raw comparison. No worker producer failed or continued.
Installed tool execution evidence is reused after dependency identity checks.
No new semantic model or whole accepted-set replay was needed.

Receipt: `.analysis/asm-replays/main-cheeto-put-a/receipt.json`, SHA-256
`b553f06cb24a5ffe46626598380f6e01e837af0d21ab71cb78655528272f3ae3`.

The explicit decision in config/reviewed_asm_families.json adopts only this
kernel: 178 reviewed ASM instruction bytes and four compared, uncredited
alignment bytes. C/C++ totals, the foreign bank, loader and callers receive
no additional credit. Whole-executable exactness is not claimed.

# OP / MAINE shared keyboard and joystick input source

The complete 262-byte BIOS input-scanning source in `input_sense.asm` is
shared, with native artifact-dependent CS/DS and input state labels. The code
has two real overlapping entrypoints: reset at relative +0 immediately
falls through to far sense at +8; the common far return ends at +260, followed
by one actual uncredited EVEN NOP at +261.

The pinned original ReC98 `th04/hardware/input_s.asm` preserves the full
GAME5 keyboard matrix and original low/high key bits; neither the extra
joystick callback nor any firmware/joystick implementation is source-owned.
The source language originally used to author these instructions remains
unknown, so a full semantic review plus full two-producer replay is necessary
for reviewed source-backed register-ASM ownership. The routine is not claimed
as Turbo C++ compiler-generated.

## Accepted original-register families — 2026-11-11

| Artifact | Original complete bytes | Native CS / DS | Joystick FAR provider |
| --- | --- | --- | --- |
| OP | `DF8E..E094` (262) | `D30` / `EFE` | `0000:2CBA` |
| MAINE | `F102..F208` (262) | `E80` / `1011` | `0000:2E82` |

These are distinct **original complete function-family owners**, not a
single transferred binary claim. The real input word/Shift, joystick status
and installed joystick offsets are `3A92/3A94`, `2E1A/0544` in OP and
`29FA/29FC`, `1D96/022E` in MAINE. The unchanged shared source also
reconstructs MAIN at `14FC2..150C8` with its separate binder.

For **each** artifact, two fresh TASM32/TLINK producers matched all 262
original bytes, the single native far-call fixup `[251]` and the two actual
public boundaries +0 and +8. The shift-status BIOS interrupt is represented
by `MOV AH,2` followed by `INT 18h`; mutating AH to three yields a genuinely
assembled same-scope negative which is rejected. No file contents, joystick
implementation or hardware inputs are included in any of the three owners.

All original 261 instruction bytes per artifact receive reviewed source-backed
assembly credit. The original `EVEN` NOP at +261 participates in the raw
comparison but never contributes authored credit. The original historical
authorship (C, mixed, or entirely assembly) is still not established by
these byte proofs; no compiler-exact C++ claim is made.

Focused acceptance receipts:
`.analysis/gpt-web-op-input-sense-262-a/receipt.json` and
`.analysis/gpt-web-maine-input-sense-262-a/receipt.json`.
The physical linker binders remain separate and source-free, preserving the
actual master/shared/data frames and their external public providers.

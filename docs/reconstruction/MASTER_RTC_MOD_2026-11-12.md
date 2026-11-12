# Master RTC register modifier in OP and MAINE

The 19-byte code at `[04E5,04F8)` in each executable is the complete private
`rtc_mod` near procedure from Master 0.23 `ATRTCMOD.ASM`. `rtc_int_set`
calls it to program the RTC register bank; the routine receives the register
index in AH and AND/OR masks in BH/BL, reads port `71h`, applies the masks
and writes the result back through ports `70h` and `71h`.

The original author's `rtc_mod proc near` body matches the retained TASM
source exactly. A single complete CODE LEDATA in each native OP/MAINE
calibration object covers all 19 instructions. Both original decoded targets
and calibration MZs contain exactly those bytes with **no MZ relocations**.
The independently accepted `rtc_int_set` ends at `04E5`, while the private
`RTC_INT` handler begins at `04F8`; these preexisting bounds are unchanged.

`python3 scripts/review_context_rtc_mod.py --check` replays the original
Master source, both actual TASM objects and both original executable views.
The narrow public evidence is `config/reviewed_context_rtc_mod.json`.
This closes 38 previously unknown foreign CODE bytes without attributing
them to game-authored C/C++. The older RTC review's two accepted functions
retain their independent ownership and evidence.

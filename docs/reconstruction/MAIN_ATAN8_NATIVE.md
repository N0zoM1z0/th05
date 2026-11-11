# MAIN: original Master ATAN8 table, 256 source-written DATA bytes

The real MAIN load image contains a complete **256-byte** monotonic
`AtanTable8` lookup at decoded `[20C2E,20D2E)`. It is derived exactly from
the independently archived Master 0.23 `ATAN8.ASM` written by A. Koizuka.
The original public-domain source expresses the actual arctangent-lookup
values in sixteen `DB` rows of sixteen decimal byte literals each. The
actual frozen TH05 TASM source `libs/master.lib/atan8[data].asm` has the same
complete 256 values; no compiled game code or copied bitmap is claimed.

The retained real TASM `main.obj` contains ordinary `_DATA` LEDATA at local
`01E0` of length `0102` (258 bytes): the first 256 bytes are the original
lookup table and the final **two zero bytes are not source-authored ATAN8
values**. Its real `_DATA` SEGDEF is 8000 bytes and both native MAP public
lists place `AtanTable8`/`_AtanTable8` at `209E:0270`. The corresponding
calibration load-image bytes at `20C50..20D50` and the independent original
MAIN bytes at `20C2E..20D2E` match the source literal table exactly, with
no ordered MZ relocation sites. The 256-byte sequence has a unique complete
occurrence in the original image.

**Original `[20D2E,20D30)` remains unknown**, even though it is zero-filled
in both retained images. There is no assertion that these two bytes are an
original author's table element or game-owned data. Other unknown DATA
within the containing original Master _DATA contribution remains separate.

The bounded source/native/OMF evidence is in
[`config/main_atan8_data_ownership.json`](../../config/main_atan8_data_ownership.json),
and its explicit decision is
[`config/reviewed_main_atan8_data.json`](../../config/reviewed_main_atan8_data.json).
`python3 scripts/review_main_atan8_data.py --check` revalidates the original
source, real object, pinned calibration and original target. Public CI runs
only its structural check. All **256 bytes are independently source-backed
third-party initialized DATA**, not new C/C++ game authored data, ASM
instructions or an authored-denominator increase. No full cold replay was run.

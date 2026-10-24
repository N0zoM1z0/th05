# Midboss state candidate

Natural C++ provenance: nmlgc/ReC98
`b6ba5b0a529edbb31efdf8c0e939263804f8ee47`, `th05/midboss.cpp` including
`th04/main/midboss/midboss.cpp` with GAME=5. The owner preserves reset and the
stage-frame activation condition without emissions, fake helpers or copied
instructions. It reuses the complete 22-byte canonical midboss structure and
real two-byte near/four-byte far callback types from `stage/setup.hpp`.
No accepted header is edited.

Original MAIN **`[1C4A1,1C4F6)`**, **85 bytes**, contains two complete far
functions: `midboss_reset` **35 bytes** and activation **50 bytes**. Both end
with their actual far return. There are no CODE tables or padding, and no
source-owned DATA/BSS. Original group `main_03` has frame **`1527`**, load
base **`15270`**, unit offset **`7231`**; DS has frame **`209D`**.

The callbacks are different real interfaces from the code owner: both null
callbacks and the invalidation function belong to **main_01**, frame `0AE1`.
Their first declarations are kept in that genuine group before selecting the
MIDBOSS/main_03 body. No cross-group shim is introduced.

| Callback | Actual frame:offset | ABI |
| --- | --- | --- |
| `NULLFUNC_NEAR` | `0AE1:192E` | C Pascal near |
| `NULLFUNC_FAR` | `0AE1:1930` | C Pascal far |
| `@MIDBOSS_INVALIDATE_FUNC$QV` | `0AE1:5BAD` | C++ Pascal near |

The far null pointer store has one original MZ fixup. All near offsets and the
far segment word are compared raw; nothing is normalized. The independent
symbol-only scaffold supplies labels and outside-contribution origins only.

| External state | DGROUP offset | Size |
| --- | --- | ---: |
| `stage_frame` | `5764` | 2 |
| `midboss` | `5AA4` | 22 |
| `midboss_active` | `C4AA` | 1 |
| `midboss_invalidate` | `C4AC` | 2 |
| `midboss_update` | `C4AE` | 4 |
| `midboss_render` | `C4B2` | 2 |
| `midboss_update_func` | `C4B4` | 4 |
| `midboss_render_func` | `C4B8` | 2 |

Private `.analysis/midboss-boundary-review.json` records complete original
boundaries, operand sites, exact callback frames and ordered fixup identity.
Wrapper `th05/midboss.cpp`, `MIDBOSS_TEXT/main_03`, uses the established MAIN
flags. A natural negative control changes the unique `midboss.hp = 0;` to
`midboss.hp = 1;`, changing real reset behavior. Focused cold replay remains
required before source-current exact acceptance.

## Accepted focused replay

`main-midboss-state-d` passes both independent producers, all 85 instruction
bytes / two complete functions and the original ordered far-pointer fixup.
The compiled HP-reset mutation from zero to one changes output and is rejected.
The actual OMF groups were correct; the initial scaffold left the compiler's
empty foreign MAI_TEXT in an out-of-range location. Using that actual segment
name in the main_01 scaffold fixed layout without changing game behavior.
No runtime state or context holes receive credit.

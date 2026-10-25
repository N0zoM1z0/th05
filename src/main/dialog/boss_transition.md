# Dialog-to-boss activation

The maintained C++ owner recovers two complete MAIN callbacks in the real
AE1 frame, corroborated by pinned ReC98 `th04/main/dialog/shared.cpp` as included
by `th05/main/dialog/dialog.cpp`. Reference acceptance is not transferred.

| Complete function | Load range | Compared | Authored CODE |
| --- | --- | ---: | ---: |
| `std_update_done` | 139F5..139FC | 7 | 7 |
| `std_update_frames_then_animate_dialog_and_activate_boss_if_done` | 139FC..13A3E | 66 | 65 |

The done callback returns byte false. The transition waits for zero byte scroll
speed and back page 1. It animates dialog, installs the done callback and the
real boss background/update/foreground and BGM overlay callbacks, then returns
byte true. Otherwise it increments the unsigned word STD frame counter and
returns false. The scroll value retains the full canonical `SubpixelLength8`
type; the 2-byte near cdecl STD callback, 2-byte near Pascal rendering callbacks
and 4-byte far Pascal boss update callback match existing accepted interfaces.
First near declarations capture the real MAIN01 code context.

`dialog_animate` remains far cdecl, with its actual RETF at13F0E. It originally
shares the AE1 frame and dialog TU with these callbacks. `samecodeseg` expresses
that context; the symbol-only scaffold binds the real forward provider in the
same group. The linker naturally produces `NOP / PUSH CS / CALL near` at13A0D.
The NOP is the only instruction NOP in either body: unit-relative24, checked
normally, classified as linker relaxation with zero authored credit. No padding,
call template, assembly body or forced near declaration is supplied by source.
Both original and candidate ordered relocation streams are empty.

Private native review is
`.analysis/native-leads/main-std-boss-transition-review.json`. Native decoding
fully covers both bodies and all return paths, with the preceding RET at139F4
and next helper prologue at13A3E. Both actual MAP files independently show a
single 73-byte compiler contribution and function publics at8BE5/8BEC in AE1.
The binder uses actual EXTDEF spellings, including
`@OVERLAY_BOSS_BGM_UPDATE_AND_REND$QV`. Its holes reserve only foreign extents
and receive no credit; it supplies neither source bytes nor relocations.

Receipt `.analysis/unit-replays/main-dialog-boss-transition-c/receipt.json`
passed two independent fresh builds, deterministic OMF, complete raw bytes,
boundaries, and literal ordered fixups. The real compiled negative changes the
frame-counter increment from 1 to 2 and is rejected (74 versus73 bytes, raw
mismatch). The unchanged installed-tool proof was reused. Earlier `-a` and `-b`
setup attempts failed before linking: missing assembler CS assumptions, then
the missing existing byte-bool header. No failed output was credited, no compiler
flags changed, and no existing source/header owner needed replay.

# Stage release and pause-menu candidate

This natural C++ producer owns the complete original adjacent MAIN functions
`stage_session_free` at `[0xB608,0xB637)` (47 bytes) and `pause` at
`[0xB637,0xB756)` (287 bytes). Coordinates refer to the unrelocated MZ
program image of locally attested MAIN, SHA-256
`c41f6e6b9a97b2433acc576ceaee800707c8d4ea7e498150a259663c8fa7d4f0`.
Both functions use frame `0AE1`, group `main_01`, and end in a near RET.
The complete334-byte extent contains instructions only: no tables or padding.
Every local branch targets an original instruction start. All14 original
MZ relocations must compare in their existing order:
`327,309,291,266,220,202,169,126,119,101,83,58,36,25`.

The semantic donor is the maintained TH04 reconstruction's
`src/main/stage/session_init.cpp`, specifically its natural cleanup and
pause functions. TH05's original operands and complete boundaries were
reviewed independently. ReC98 `b6ba5b0a`'s `th05_main.asm`,
`th04/main/pause.asm` and `th05/hardware/input.h` supply additional behavior
and interface evidence. Reference assembly is disassembly evidence; it does
not establish handwritten original origin. No instruction body is copied
into the natural source.

TH05 release calls the actual near BB, dialog, STD and map free functions,
cleans sprite patterns180 through255, and frees CDG slots1 through30. The
slot constants agree with the unchanged complete accepted EMS/CDG header;
this owner adds no partial record or mutable data layout. Its scalar
arguments use the original Pascal word frames.

Pause initially waits for all input to be released using the genuine
held-key sensing service at `14AB:0618`. It draws the existing gaiji
strings, toggles the resume/quit selection on UP or DOWN, and preserves
its actual text attributes. Q returns1 immediately, before the UI clearing
path. CANCEL selects resume, while SHOT and OK confirm the current choice.
Unlike TH04, the final release loop waits only for CANCEL, preserving other
held inputs. Three foreign existing space strings clear the UI. No glyph,
Japanese string, filename or other asset payload is supplied by this owner.

The TH05 input header corroborates the real far C++ `int16_t` held-input
interface and far Pascal `int16_t input_wait_for_change(int)` interface.
The latter's return is explicitly garbage and is ignored. Text/gaiji,
pattern cleanup and CDG free retain their actual far Pascal APIs. There
is no same-CS far-call rewrite, near/far cast, custom carry/register
protocol, Motion-return adaptation, hardware operation, source padding,
inline assembly or inactive optimization expression in this producer.

Private integration inputs are `.analysis/session-end-unit-proposal.json`,
`.analysis/session-end-bindings.asm`, and
`.analysis/session-end-boundary-review.json`. The outside-only binder defines
real symbols and no helper body, resource value or artificial stack. The
proposed owner-level negative changes Q's immediate return from1 to0,
changing the caller's quit decision. It is not an independent negative for
the cleanup helper. Two fresh deterministic producers, complete raw bytes,
original ordered relocations and the compiled negative remain required
before acceptance. This packet defines no initialized DATA or BSS.

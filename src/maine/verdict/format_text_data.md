# Verdict formatting text banks

Two ordinary C DATA owners recover the remaining six complete formatting
strings, preserving each physical object's identity and const element type.

| Bank | Original DS range | Decoded MAINE range | Complete objects | Bytes |
| --- | --- | --- | --- | ---: |
| verdict_punctuation | 1614..1620 | 11724..11730 | Point unit, decimal point, percent, fraction point | 12 |
| verdict_counter_units | 16BC..16C2 | 117CC..117D2 | Miss-count unit, bomb-count unit | 6 |

The four punctuation strings are `点`, `．`, `％`, `．`; both counter units
are `回`. Each is two CP932 bytes plus its own NUL. Distinct identical decimal
points and counter units are real complete objects, not padding. Native pushes
in the accepted format/main routines independently reference all six addresses.
The adjacent metric and score-label owners remain separate and unchanged.
No font/glyph bitmap, asset content, state byte, BSS, CODE or pointer table is
included. Neither complete extent has an ordered MZ fixup or padding byte.

`format_text_c.h` uses full const unsigned-character array fields with natural
offsets 0/3/6/9 or 0/3, and total sizes 12/6. All sizes/offsets are asserted.
Ordinary C static aggregate initialization preserves distinct member storage
without constructors, dummy initializers, packing flags or changed constness.
The readable UTF-8 literals pass through the existing explicit CP932 staging;
no hexadecimal byte bank or target-derived instruction data is supplied.

These banks are explicit reconstruction models, not claims about the original
struct declarations or source language. Their source APIs are
`verdict_punctuation.<field>` and `verdict_counter_units.<field>`. They do not
provide invented old global-array PUBDEF aliases. Future caller integration
must use real field expressions and replay its demonstrated affected closure.
Existing accepted caller/header declarations and CODE records are unchanged;
this DATA acceptance alone does not prove that integration or whole linkage.

The earlier uncompiled 294-byte monolithic C++ text proposal did not establish
distinct const-object identity. Its two later 156/120-byte text owners remain
accepted. The C banks here recover only the excluded 18 bytes using a real
semantic model, rather than repeating the earlier pooled-array assumption.

Each bank has two fresh deterministic complete C compiler DATA producers,
actual `.c` argv and producer identity, full SEGDEF/LEDATA/MAP/raw verification,
original empty ordered fixups, and its own compiled DATA negative. Punctuation
changes the percent sign to `＆`; the counter bank changes only the miss-count
unit to `度`. Both negatives are rejected over their complete scopes.

Receipts under `.analysis/unit-replays/` are
`maine-verdict-punctuation-data-a/receipt.json` and
`maine-verdict-counter-units-data-a/receipt.json`. All input/tool identities and
the canonical UTF-8 versus actual CP932 files are rechecked on import. Binders
contain only real external frames and the DATA prefix before each whole owner;
no initialized payload, inside gap or artificial stack is supplied. Installed
execution proof and unchanged accepted evidence are reused. C semantic DATA
credit remains separate from C++ ownership and instruction acceptance.

Independent native/source review of all six complete strings and their actual
consumer pointers is `.analysis/verdict-data-source-native-review.json`,
SHA-256 `492e3eb12cb77b94cf9bdec5c2590563bacb5390d01de3b719af7507ac60eb6d`.
Root's separate actual-producer readback is
`.analysis/verdict-state-data/root-final-native-review.json`, SHA-256
`e93c89ac086564a47e5e705b64d7a5deb48ffc2733563face3392276e11ed50a`.

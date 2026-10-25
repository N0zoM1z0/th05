# Readable stage-bonus UI DATA

The proposed owner contains 21 complete readable UI string arrays at original
MAIN `[22471,22740)`, 719 bytes, corresponding to DS `209D:1AA1..1D70`.
Eleven strings explain the score modifiers (timeout, starting lives, continues
and difficulty); ten label the stage, dream, graze, point-item, no-miss,
no-bomb, total, all-clear, lives and total-item bonus components.

The maintained source stores these Japanese strings as readable UTF-8 text.
Explicit `source_encoding = "cp932"` transcodes the actual compiler inputs;
canonical snapshots stay UTF-8. Natural string terminators are part of the
semantic DATA. Each original byte is independently checked against the
encoded text. This is text recovery, with no opaque numeric initializer or
target dump. The preceding two gaiji-index strings, font images and other
assets remain foreign and uncredited.

The original eleven near description pointers at DS `1A64` and ten near label
pointers at `1A7A` independently identify all 21 exact object starts. This
cross-check establishes actual targets without placing those pointer values
in this source. All strings are contiguous and independently terminated.
There are no MZ relocation sites and no padding bytes in this 719-byte span.
No CODE, BSS, pointer table or state object is claimed by this owner.

The symbol-only binder supplies the authentic MAIN code-frame extent, an
empty compiler CODE segment in its real `main_03` context, and a DATA prefix
ending at `1AA1`. It emits no strings, internal holes, stack or replacement
instructions. The actual compiler must supply the complete 719-byte `_DATA`
contribution with full gapless LEDATA and a matching complete MAP extent;
native text comparison alone grants no acceptance.

The proposed negative changes the readable Easy-difficulty explanation from
factor `０．５` to `０．６`, preserving its CP932 encoded length. It must alter
the actual staged DATA and be rejected by the same complete raw oracle.
The focused `main-stage-bonus-ui-text-a` replay passed two fresh producers
with actual CP932 compiler inputs, complete 719-byte raw comparison, the empty
original ordered relocation stream and full OMF/MAP/dependency checks. Its own
Easy-description factor `０．５` to `０．６` DATA mutation was compiled and
rejected. All 719 semantic UI-text bytes were imported as authored DATA; no
surrounding pointers, glyph arrays or state receive credit from this owner.

Private evidence and proposals are
`.analysis/stage-bonus-strings-boundary-review.json` and
`.analysis/stage-bonus-strings-unit-proposal.json`. Run
`python3 .analysis/stage-bonus-strings-review.py` for the bounded native audit.
It records each semantic object, literal/reference line, original offset,
encoded identity and all 21 pointer cross-checks without executing the game
or compiler. ReC98's original CP932 literals at `th05_main.asm:19660..19680`
are the candidate text reference; acceptance does not transfer from it.

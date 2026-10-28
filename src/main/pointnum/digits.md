# Point popup digit conversion: natural C++ candidate

The complete native near Pascal converter at MAIN15870..158AA occupies58 bytes,
including its final alignment NOP at relative57. It takes a near pointer to
the last of five digit bytes and an unsigned WORD number, consumes4 argument
bytes and returns pixel width in AX. It writes decimal digits in little-endian
order. Width includes an additional trailing zero drawn by the renderer;
zero therefore has width16, and65535 has width48. SI/DI/BP/DS/ES are preserved.
Ordered MZ fixups are empty. The following C++ procedure is excluded.

digits.cpp recovers this arithmetic as ordinary C++ against the existing
complete HUD five-WORD power-table declaration. That table already belongs
to the accepted38-byte HUD decimal DATA contribution; it adds no credit here.
The original native instructions use BP as the first nonzero digit position
after consuming the frame arguments. That observation alone does not prove
handwritten ASM, and this conventional public Pascal routine is not promoted
by the neighboring two-entry allocation procedure's separate origin review.

The initial pinned Borland build with the single natural frameless profile
generates96 CODE bytes against58. Actual output uses ENTER6, saves both SI/DI,
stores the first-nonzero position, remaining count and quotient in stack locals,
and computes quotient and remainder with separate DIV instructions. The first
size gate stops before a second positive or negative. The proposal is retained
privately outside the live acceptance manifest; the58 native bytes stay unknown.
No inline instruction transcription, register/volatile barrier, padding or
compiler-flag search is introduced.

The actual96-byte compiled procedure passes all65,536 WORD inputs against a
mathematical decimal model, checking all five digits, surrounding canaries,
returned width, Pascal stack cleanup and preserved registers. The complete
native provider independently passes the same full domain in the allocation
model. The CPP check uses its actual linked DS/public placement and generated
power values: the oversized contribution shifts foreign DATA, so it proves no
original standalone layout. Semantic equivalence and exact acceptance remain
separate.

First build: `.analysis/unit-replays/main-pointnum-digits-natural-a/`.
Proposal: `.analysis/pointnum-digits-natural-proposal.toml`.
Actual compiled model: `.analysis/pointnum-digits-cpp-model.json`, SHA-256
`ac90d2261b8b77248d3db1005165e7e4b41a9c3dbe77d5243f4487f753f9de0a`.

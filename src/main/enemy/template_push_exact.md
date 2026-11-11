# Exact enemy bullet-template transfer

MAIN's complete near-Pascal `enemy_bullet_template_push(const BulletTemplate&)
at `[16BCF,16BE7)` copies the source's genuine 14-byte bullet-template record
to the global current template at DS `577E`. It returns with `RET 2`, has
no padding, no initialized DATA and no original MZ relocation sites.

The maintained C++ keeps the canonical `BulletTemplate` with its real field
layout. It uses the original Borland register interface: CX gets the number
of 16-bit words, SI points at the near reference, DI at the live template,
ES copies DS, then one semantic `REP MOVSW` transfers seven complete words.
There is no byte array or synthetic target instruction stream.

A normal structure assignment invokes Borland's `F_SCOPY@` helper instead of
copying inline. The genuine `__memcpy__` intrinsic generates the correct
24-byte length but schedules SI/DI/CX differently. Preparing the three
registers in C++ source order reproduces the actual near ABI, register
allocation and all 24 original bytes through the real direct TCC `-c`
compiler. The neighboring accepted enemy allocation, stage runner and
576-byte updater remain unchanged.

Focused receipt:
`.analysis/unit-replays/gpt-web-main-enemy-template-push-a/receipt.json`.
Two independent Turbo C++/TLINK builds match 24/24 raw bytes and the empty
ordered fixup stream. The compiled negative reduces the seven-word count by
one, and the strict oracle rejects it. No full cold replay was used.

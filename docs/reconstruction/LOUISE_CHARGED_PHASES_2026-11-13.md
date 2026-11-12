# Louise: exact common end-state and cloud settings across late attacks

The two Louise charged-weapon attacks restore the identical Boss state
when finished: return to movement mode, zero the phase frame and select
the still sprite, in that order. The turning-ring stack and aimed-pellet
attack independently initialize the same forward, nondecelerating cloud
spawn type. The original-order source now expresses both operations as
`LOUISE_CHARGED_RETURN_TO_STILL()` and
`LOUISE_FORWARD_NONDECEL_CLOUD()` without adding runtime calls. The two
laser directions, rotating rings and spread shots keep their individual
angles, projectile counts, sounds and branch timing.

The complete four-function, 603-byte original CODE owner passes two genuine
Borland/TLINK builds, full raw bytes, ordered MZ relocations and a rejected
compiled semantic negative. Receipt:
`.analysis/unit-replays/gpt-web-louise-shared-charged-later-20261113-a/receipt.json`.
No previously accepted CODE receives duplicate credit.

# Mai/Yuki: paired charge and four initial Mai attack muzzles

The six complete initial Boss callbacks in
`src/main/boss/mai_yuki/initial_patterns.cpp` now express the shared paired
charge dust through `MY_PAIRED_CHARGE_DUST(fighter)` and the common
8-pixel-above-Mai bullet origin through `MY_MAI_BULLET_MUZZLE()`.
Mai's and Yuki's charge paths still use their own full Boss positions,
separate sprite changes and the genuine Mai-only charge sound; the four Mai
patterns keep distinct frame gates, spread setups, shots and returns.

Two actual Turbo C++/TLINK producers matched all **543 original CODE bytes**
and ordered relocations `[525,433,324,233,51]`. The original compiled
first-stack-size mutation was rejected.
Evidence: `.analysis/unit-replays/gpt-web-maiyuki-charge-muzzle-20261112-a/receipt.json`.
This refreshes natural source for an existing accepted six-function Boss
owner and does not duplicate source-authored CODE credit.

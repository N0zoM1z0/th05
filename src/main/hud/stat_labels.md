# MAIN HUD small-gaiji text labels

The original MAIN `[21D6C,21D9E)` holds ten five-byte strings for the
score/HISCORE caption, the REIGEKI/REIMU/REIRYOKU names and BOMB, PLAYER,
POWER, ENEMY and SUIKEI labels. Each contains source-level small-gaiji
selectors followed by zero terminators; no selector represents copied
bitmap pixels. The original source reference is
`_reference/ReC98/th04/gaiji/hud[data].asm`, which is included by the
TH05-specific disassembly with the extra `gsSUIKEI` string immediately
afterward. The already accepted HUD score consumer passes these words to
the real `GAIJI_PUTSA` function.

`src/main/hud/stat_labels.c` reconstructs all ten rows with named glyph
roles and a five-byte C row stride. The true DATA prefix is supplied
outside the candidate by `main_stat_labels_bindings.asm`. The 50-byte
contribution contains no padding, instructions or ordered relocations;
its following byte at `21D9E` remains unassigned. This record is separate
from the five larger difficulty words at `21D44..21D6C`.

The targeted receipt at
`.analysis/unit-replays/gpt-web-main-stat-labels-a/receipt.json`
reports two original-size, raw-byte and OMF/MAP-exact C producers and
an independently compiled negative that changes the last ENEMY glyph.
Other accepted HUD code or data was not rebuilt.

# Mai/Yuki ten late-pattern callbacks and shared-fight dispatch

The original complete **939-byte** near-C++ late-pattern contribution
contains ten separately formed procedures: Mai's reversing blue rings,
Yuki's random aimed fan, rings, small-ball stacks, ball fan, big-ball
stacks, random pellets and reversing red rings, plus Yuki and Mai's
opposite Cheeto bursts. `paired_attack_rules.hpp` defines the actual
source-visible clocks, counts, directions, randomized ranges, colors,
shot types and rank-independent speeds as **compile-time-only** values.
It introduces no scratch storage, new callback table, runtime helper,
copy of a sprite asset or replacement for the real bullet template.

The original shared ring protocol uses phase frame **48** to arm both
Bosses and every-four-frame firing with four bullets per ring at
speed **2.375 pixels/frame**. Mai stores its initial blue-ring angle
0x20 and negative signed angular step -4 in original state bytes
15/12; Yuki stores angle zero and positive step 4 in bytes 14/13.
Every 16 frames the source adds random mask-7 jitter and reverses
the step. Mai's pattern completes at frame **256**, whereas Yuki's
reversing ring continues until the caller changes phases.

Yuki's smaller attacks retain independent **16/8/2-frame** firing
cadences and their original sound asymmetry, red bullet patnums,
8-pixel upward bullet origin, exact linear or regular add calls,
separate stack sizes, and random starting angle and speed ranges.
Yuki's aimed spread is seven shots with angle step five and a 6-bit
random angular bias; its red circular volley fires 32 shots at
2.5 pixels/frame. The eight-shot small-ball fan has angle 0x40 and
step 12; the eight-shot big-ball stack has speed step 0.375. The
random-pellet variant fires two shots every second frame.

Both Cheeto callbacks fire at phase frames **48** and **96**, retain
colors **9** (Mai) and **11** (Yuki), speed two, the ±0x40 aimed
angular offsets selected from the *actual relative positions* of the
two Bosses, and the real Cheeto-add/SE15 interfaces. Mai's callback
completes at frame 128, while Yuki's returns false. The 1,018-byte
shared Boss controller indexes its original independent four-slot
near callback schedules by `patterns_seen & 3`, now sourced from the
same `MYR_CALLBACK_VARIANT_MASK` as the combat protocol. Both
maintained complete updater variants still have identical code bodies.

The *entire two-unit accepted closure*, including ten complete attack
functions and the true 1,018-byte far-Pascal Boss update with its
24-byte switch table and checked zero, passed two independent pinned
Borland producer rounds, all original raw bytes, MAP/OMF extents and
literal ordered MZ fixups. A compiled mutation of Mai's original
0x20 ring start angle to 0x21 was rejected. Focused receipt:
`.analysis/unit-replays/gpt-web-maiyuki-paired-attacks-a/receipt.json`.
The earlier accepted 111-byte combined hit leaf and stand-alone solo
Boss routines were not changed or recredited; no full cold replay
was executed.

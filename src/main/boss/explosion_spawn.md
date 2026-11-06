# Boss explosion creation

The maintained C++ recovers MAIN `[176CE,177F0)`: five complete functions,
290 authored bytes (282 instructions and eight compiler switch-table bytes).
There are no NOPs, alignment bytes, owned DATA or BSS.

| Function | Start | Bytes |
| --- | ---: | ---: |
| `explosions_small_reset()` | `176CE` | 15 |
| `boss_explode_small(explosion_type_t)` | `176DD` | 128 |
| `boss2_explode_small(unsigned int)` | `1775D` | 46 |
| `boss_explode_big_circle()` | `1778B` | 60 |
| `boss2_explode_big_circle()` | `177C7` | 41 |

TH04's explosion family and pinned ReC98 `b6ba5b0a` supply semantic references;
their assembly listings do not supply source bytes or acceptance. The ordinary
C++ pointer, field initialization, enum switch and saved coordinates reproduce
the complete compiler-shaped routines. Existing complete Explosion and Boss
types are reused without changing accepted headers. The small allocator keeps
the original unchecked choice of the second slot when the first is alive.
The second Boss temporarily replaces the full current point, then restores
the separately saved X and Y values.

The real CODE group is `main_03`, frame `1527`; DGROUP is `209D`. Sound retains
far Pascal frame `14AB:0232`. Reset returns far, small creation uses word-sized
Pascal parameters, and the other functions return near. The four generated
switch destinations are `17727/1772D/17733/1773F`; the table occupies
`17755..1775D`. Symbol-only bindings supply external addresses and no bodies.

`main-boss-explosion-spawn-a` passes two deterministic producers, valid OMF,
all 290 raw bytes and original ordered relative fixups `[244,128]`. Its shared
compiled sound-effect mutation is rejected. Receipt:
`.analysis/unit-replays/main-boss-explosion-spawn-a/receipt.json`, SHA-256
`38a436ec0c398793b5a62d364e205cb59b711fc56e5674d81b1bab605013274f`.
Complete native boundary review:
`.analysis/boss-explosion-spawn-boundary-review.json`.

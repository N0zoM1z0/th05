# Master PF buffer state and random seed in three TH05 MZ executables

The original Master author `PF.ASM` explicitly initializes a 16-bit
`bbufsiz=512`, 16-bit `pferrno=0` and one-byte `pfkey=0`. `RAND.ASM`
independently initializes the 32-bit `random_seed=1`. The actual retained
native TASM source puts an additional zero byte between the two source
contributions for alignment; this byte is **not** initialized in the
archived author `PF.ASM` and is deliberately **not credited**.

| Program | Source PF 5 bytes | Unknown alignment 1 byte | Source RAND 4 bytes |
| --- | --- | --- | --- |
| MAIN | `20DE2..20DE7` | `20DE7` | `20DE8..20DEC` |
| OP | `F566..F56B` | `F56B` | `F56C..F570` |
| MAINE | `10380..10385` | `10385` | `10386..1038A` |

`python3 scripts/review_master_pf_rand_initial.py --check` verifies the
archived source declarations and `PF.INC` constants, matching retained
native TASM sources, explicit complete `_DATA` LEDATA records, real `bbufsiz`
and `random_seed` MAP publics, original/calibration payload bytes and empty
MZ relocation streams. Exactly **27 bytes** now belong to third-party
Master initialized DATA, with **zero game-authored C++ credit**. The original
unknown alignment bytes stay unknown rather than being promoted from
mere observed zeroes.

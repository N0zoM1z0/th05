# TH05 ZUN -S natural resident-entry control-flow experiments

Three new, behavior-preserving **real TCC 4.02 `-c` and TLINK** trials
targeted the authentic **269-byte** `-S` resident `main()` at COM
`04A9..05B6`, with the independently accepted 322-byte `cfg_init()` and
320-byte native initialized DATA, real C0T CRT, and the previously
restored binding segment/initializer topology.

| Natural source rewrite | Linked `main()` CODE | Original complete match |
| --- | ---: | --- |
| Two independent `-R` / `-D` option tests (`-R` always returns) | 260 B | No |
| Negated invalid-`-D` guard with a success path | 258 B | No |
| Only create a resident when the existing segment is absent | 260 B | No |

Each trial used **the maintained natural `initialize.cpp`**, not the
three ReC98 self-assignment/empty-function optimizer barriers. They
preserve the original error messages, exit results, resident lifecycle
and option effects but do not reproduce the original compiler tail
layout. The first trial has 151 mismatching positional bytes; the
second has 162 and the third has 150, before accounting for the nine-
or eleven-byte size shortfall.

Private reproducible native input snapshots and raw COM outputs are at
`.analysis/gpt-web-zun-natural-flow4-*/`, with the targeted build script
`.analysis/gpt-web-zun-natural-flow4.py`. The main program remains
unaccepted; the existing exact config, resident DATA and CRT owners are
unchanged. No new complete `-S` child or game-authored C++ byte claim
follows from these experiments.

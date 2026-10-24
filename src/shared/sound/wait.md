# BGM measure wait candidate

Natural C++ follows ReC98 b6ba5b0a `th05/snd/delaymea.cpp`. Original decoded
OP E0F1..E113 and MAINE F265..F287 are complete34-byte functions, ending at
RETF4; the following explicit zero is outside these scopes. Negative control
changes the disabled-music condition from `<0` to `<=0`.

An independent wrapper produces35 bytes because the earlier measure API is
foreign. Restoring the observed original TU relationship by including unchanged
`measure.cpp` emits the correct direct call to the earlier measure function,
and the wrapper is then34 bytes. `op-sound-wait-d` has two deterministic native
positives and a rejected compiled negative, but fails strict raw and ordered
fixups: TLINK leaves the later foreign frame_delay as a far call with a fixup
at relative20. The original has NOP/PUSH CS/near CALL with no MZ fixup.

No fake near ABI, call template, instruction patch or link-metadata sorting was
introduced. The candidate stays unaccepted and neither artifact has a live
replay entry. MAINE was not compiled after OP demonstrated the same known
forward foreign-call obstacle. Binder integration errors and the first
single-producer size failure remain private alongside the complete failed
receipt. Mode/frame addresses are genuine foreign labels, with no data values.

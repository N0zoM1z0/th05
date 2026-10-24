# Sound driver mode selection

Natural C++ follows ReC98 b6ba5b0a th04/snd/detmodes.cpp. Driver-residency
probes are real external far C functions; the PMD interrupt uses its genuine
AH function number and AL driver-version response. Full BGM/SE enum domains
are retained, including the original INT16 SE sentinel: losing it changes
ternary arithmetic to eight bits and fails the raw oracle. Global mode fields
remain bytes as in the original.

MAIN's full156-byte function is14BD4..14C70. It naturally generates both
far-to-near linker shortenings to the earlier PMD/MMD probes in the real
SHARED segment. Their two NOPs are compared but excluded from authored credit.
`main-sound-modes-b` passes both fresh complete raw/ordered producers and a
compiled driver-response mutation FF toFE. The earlier failed producer is
retained. OP D380..D41C and MAINE E87E..E91A use separately reviewed original
frames/globals and require their own receipts; source reuse grants no credit.

`op-sound-modes-b` and `maine-sound-modes-a` independently pass the same
strict gate and their own compiled driver-response controls. Each credits154
instruction bytes and excludes two real linker NOPs. The OP binder retains
the known foreign music DATA extent through DS2817 to give the no-STACK TLINK
candidate a valid minimum allocation; it supplies no data values and changes
no observed global address. The first smaller-context OP candidate failed MZ
validation and grants no evidence or progress credit.

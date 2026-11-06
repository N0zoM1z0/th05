# General BB loader: natural candidate

The complete native MAIN function is F930..F967, 55 instruction bytes, near
Pascal with one four-byte far filename argument and RET4. The following NOP
is outside this body. It returns a two-byte segment handle in AX. The sole
original ordered MZ fixup is relative 7 at the real far allocation call.

A natural C++ body uses the actual 2048-byte allocation, foreign scratch segment
at DS 4204 and direct DOS open/read/close calls, all unchecked. It retains the
full far filename and segmented result types. LDS uses the named C++ parameter
for actual DOS DS:DX transport; no hard-coded SS:SP displacement, hidden frame
operation, instruction algorithm or alternate return ABI is introduced.

One real first producer emits 56 bytes with a BP frame and first fixup 10.
Its filename argument is accessed through the compiler's BP+4 frame, rather
than the native BX snapshot of the actual entry stack after saving SI.
It also loads its return before restoring SI/BP. Raw bytes and extent fail;
there is no second producer, negative or exact credit. The initial binder-only
attempt stopped on a missing CS assumption before compiling C++.

Evidence: `.analysis/native-producers/main-bb-load-natural-b/native-diagnostic.json`.
The BB text lifecycle has its own [independent exact acceptance](bb_text.md).
This candidate does not justify promoting the general loader to handwritten ASM.

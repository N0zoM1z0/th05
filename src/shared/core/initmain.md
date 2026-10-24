# Shared MAIN/MAINE initialization

Natural C++ follows ReC98 b6ba5b0a th03/core/initmain.cpp with the actual GAME5
branch. It reserves DOS memory, sets the real packfile buffer size, starts
vsync/EGC/graphics/joystick/archive/sound services and preserves the observed
error return. Foreign library routines remain real far Pascal APIs. No
original helper body, initialized DATA or BSS is owned here.

The complete function is MAIN14F7A..14FC2 and decoded MAINEF0BA..F102,
72 bytes in each. Actual MAINE calibration uses BINARY=M; its configured
producer retains that real context. MAIN has SHARED frame14AB/DGROUP209D;
MAINE uses originalE80/1011, rather than calibration's E7F sound frame.
Original native CALL targets and both globals were separately checked in each
artifact. `main-core-init-a` and `maine-core-init-a` pass two fresh producers,
full raw bytes, original ordered fixups and compiled packfile-buffer mutations
from4096 to2048. Neither grants whole-game or packed-file exactness.

// Declarations for the held-input helpers.
#ifndef TH05_SHARED_HARDWARE_INPUT_HELD_HPP
#define TH05_SHARED_HARDWARE_INPUT_HELD_HPP
#pragma codeseg SHARED
int far input_reset_sense(void);
int far input_sense(void);
int far input_reset_sense_held(void);
// Both live in this code segment but are still called far.
#pragma samecodeseg input_reset_sense
#pragma samecodeseg input_sense
#endif

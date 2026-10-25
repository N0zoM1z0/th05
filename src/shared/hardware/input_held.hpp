// Exact far entry declarations in their actual shared code frame.
#ifndef TH05_SHARED_HARDWARE_INPUT_HELD_HPP
#define TH05_SHARED_HARDWARE_INPUT_HELD_HPP
#pragma codeseg SHARED
int far input_reset_sense(void);
int far input_sense(void);
int far input_reset_sense_held(void);
// Both real providers share the current CS and still return far.
#pragma samecodeseg input_reset_sense
#pragma samecodeseg input_sense
#endif

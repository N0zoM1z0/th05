// Persistent 32-bit frame totals and 16-bit story/dialogue frame count.
#pragma option -zCMAIN_FRAME_COUNTER_DATA_TEXT -zPmain_01
// The definitions match the existing gameplay-loop and handoff declarations.
// No header CODE-segment pragmas belong to this data-only translation unit.

unsigned long total_slow_frames = 0;
unsigned long total_frames = 0;
unsigned int total_std_frames = 0;

typedef char main_slow_frames_u32[(sizeof(total_slow_frames) == 4) ? 1 : -1];
typedef char main_frame_count_u32[(sizeof(total_frames) == 4) ? 1 : -1];
typedef char main_std_frames_u16[(sizeof(total_std_frames) == 2) ? 1 : -1];

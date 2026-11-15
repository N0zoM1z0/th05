// Frame counters for the play statistics that GameExecl() saves to the
// resident structure: all frames, slowed-down frames, and dialog frames.
#pragma option -zCMAIN_FRAME_COUNTER_DATA_TEXT -zPmain_01
// Deliberately includes no header: their code segment declarations would
// make TLINK report that group main_01 exceeds 64 KiB.

unsigned long total_slow_frames = 0;
unsigned long total_frames = 0;
unsigned int total_std_frames = 0;

typedef char main_slow_frames_u32[(sizeof(total_slow_frames) == 4) ? 1 : -1];
typedef char main_frame_count_u32[(sizeof(total_frames) == 4) ? 1 : -1];
typedef char main_std_frames_u16[(sizeof(total_std_frames) == 2) ? 1 : -1];

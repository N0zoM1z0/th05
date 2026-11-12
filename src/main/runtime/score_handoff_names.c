/* Score/return UI blank field followed by the third mutable MAINE child name. */
#pragma option -zCSCORE_HANDOFF_DATA_TEXT -zPmain_01
#ifdef __cplusplus
#error Score/child filename DATA requires the native C producer
#endif

#include "src/shared/abi.hpp"

typedef struct ScoreHandoffNames {
    char score_text_blank[3];
    char score_child_program[6];
} ScoreHandoffNames;

ScoreHandoffNames near score_handoff_names = {
    "  ",
    "maine"
};

typedef char score_handoff_blank_offset[
    (offsetof(ScoreHandoffNames, score_text_blank) == 0) ? 1 : -1];
typedef char score_handoff_binary_offset[
    (offsetof(ScoreHandoffNames, score_child_program) == 3) ? 1 : -1];
typedef char score_handoff_size[(sizeof(ScoreHandoffNames) == 9) ? 1 : -1];

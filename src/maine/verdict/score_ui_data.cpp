// Readable verdict score messages, filenames and stage headings.
// Canonical UTF-8 source requires explicit CP932 compiler staging.
#pragma option -zCVERDICT_SCORE_DATA_TEXT -zPgroup_01
#include "src/maine/verdict/ui_data.hpp"

const shiftjis_t near verdict_points_unit[] = "点";
const char near verdict_comment_filename[] = "_ude.txt";
const shiftjis_t near verdict_unrated[] = "？？？？？？点";
const shiftjis_t near verdict_slowdown_warning[] = "処理落ちによる判定不可";
const char near verdict_picture_filename[] = "ude.pi";
const shiftjis_t near verdict_stage_1_title[] = "　１面　";
const shiftjis_t near verdict_stage_2_title[] = "　２面　";
const shiftjis_t near verdict_stage_3_title[] = "　３面　";
const shiftjis_t near verdict_stage_4_title[] = "　４面　";
const shiftjis_t near verdict_stage_5_title[] = "　５面　";
const shiftjis_t near verdict_stage_6_title[] = "　６面　";
const shiftjis_t near verdict_final_score_title[] = "最終得点";

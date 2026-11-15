// Verdict heading and metric labels. (UTF-8; converted to Shift-JIS before
// compiling.)
// Identical const strings within one translation unit may be merged by the
// compiler, so the original's duplicates ("最終得点", "％", "点") are spread
// across this file, score_ui_data.cpp and punctuation_data.c.
#pragma option -zCVERDICT_METRIC_DATA_TEXT -zPgroup_01
#include "src/maine/verdict/ui_data.hpp"

const shiftjis_t near verdict_bonus_percent_sign[] = "％";
const shiftjis_t near verdict_heading[] = "　　　　　　　 腕前判定";
const shiftjis_t near verdict_rank_label[] = "難易度";
const shiftjis_t near verdict_score_label[] = "最終得点";
const shiftjis_t near verdict_misses_label[] = "ミス回数";
const shiftjis_t near verdict_bombs_label[] = "ボム使用回数";
const shiftjis_t near verdict_completion_label[] = "ゲーム達成率";
const shiftjis_t near verdict_kills_label[] = "悪霊退治率";
const shiftjis_t near verdict_items_label[] = "アイテム回収率";
const shiftjis_t near verdict_point_items_label[] = "得点アイテム最高点率";
const shiftjis_t near verdict_bonus_label[] = "気合い";
const shiftjis_t near verdict_slowdown_label[] = "処理落ち率";
const shiftjis_t near verdict_skill_label[] = "あなたの腕前";

// Original TH05 ZUN.COM -S compiler-owned configuration and UI text.
// UTF-8 maintained source; Borland consumes CP932 through the explicit unit
// staging mode. All semantic values originate in the pinned ReC98 sources.
#pragma option -2
#include "src/zun/resident/initialize.hpp"

char debug = 0;
const cfg_options_t OPTS_DEFAULT = {
    ZUN_CFG_SHOW_SETUP_MENU, ZUN_CFG_LIVES_DEFAULT,
    ZUN_CFG_BOMBS_DEFAULT, ZUN_CFG_BGM_FM26, ZUN_CFG_SE_FM, true
};
const char ZUN_CFG_FILENAME[] = "miko.cfg";
const char ZUN_RESIDENT_ID[] = "KSOConfig";
const char ZUN_RESIDENT_LOGO[] =
    "\n\n" "東方怪綺談用　 常駐プログラム　                         Version1.00 (c)zun 1998" "\n";
const char ZUN_RESIDENT_NOT_FOUND[] = "まだいませんよぉ\n\n";
const char ZUN_RESIDENT_REMOVED[] = "じゃぁねー、また会えるよね\n\n";
const char ZUN_RESIDENT_BAD_OPTION[] = "そんなオプション付けられても、困るんですけど\n\n";
const char ZUN_RESIDENT_ALREADY_PRESENT[] = "わたし、すでにいますよぉ\n\n";
const char ZUN_RESIDENT_NO_MEMORY[] = "作れません、わたしの居場所がないの！\n\n";
const char ZUN_RESIDENT_INITIALIZED[] = "おじゃましまーす。\n\n";
const char ZUN_RESIDENT_FILE_FAILURE[] = "ファイルが書き込めないの～\n\n";

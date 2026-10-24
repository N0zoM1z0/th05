// Real four-character/ten-level shot selector. Reuse the canonical Pascal
// callback type and complete array declaration from new-game initialization.
#ifndef TH05_SHOT_TABLES_HPP
#define TH05_SHOT_TABLES_HPP
#include "src/main/runtime/gameplay_session_init.hpp"

#pragma codeseg MAIN_01_TEXT main_01
// The common providers have C++ linkage; character providers have C linkage.
void pascal near shot_l0(void);
void pascal near shot_l1(void);
extern "C" {
    void pascal near shot_reimu_l2(void);
    void pascal near shot_reimu_l3(void);
    void pascal near shot_reimu_l4(void);
    void pascal near shot_reimu_l5(void);
    void pascal near shot_reimu_l6(void);
    void pascal near shot_reimu_l7(void);
    void pascal near shot_reimu_l8(void);
    void pascal near shot_reimu_l9(void);
    void pascal near shot_marisa_l2(void);
    void pascal near shot_marisa_l3(void);
    void pascal near shot_marisa_l4(void);
    void pascal near shot_marisa_l5(void);
    void pascal near shot_marisa_l6(void);
    void pascal near shot_marisa_l7(void);
    void pascal near shot_marisa_l8(void);
    void pascal near shot_marisa_l9(void);
    void pascal near shot_mima_l2(void);
    void pascal near shot_mima_l3(void);
    void pascal near shot_mima_l4(void);
    void pascal near shot_mima_l5(void);
    void pascal near shot_mima_l6(void);
    void pascal near shot_mima_l7(void);
    void pascal near shot_mima_l8(void);
    void pascal near shot_mima_l9(void);
    void pascal near shot_yuuka_l2(void);
    void pascal near shot_yuuka_l3(void);
    void pascal near shot_yuuka_l4(void);
    void pascal near shot_yuuka_l5(void);
    void pascal near shot_yuuka_l6(void);
    void pascal near shot_yuuka_l7(void);
    void pascal near shot_yuuka_l8(void);
    void pascal near shot_yuuka_l9(void);
}
#pragma codeseg
#endif

// Candidate Yuuka shot interface, corroborated by nmlgc/ReC98@b6ba5b0a529edbb3.
// Reuse the accepted Shot/ShotAddIterator definitions without changing them.
#ifndef TH05_MAIN_PLAYER_YUUKA_HPP
#define TH05_MAIN_PLAYER_YUUKA_HPP

#include "src/main/player/reimu.hpp"

extern "C" {
    void pascal near shot_yuuka_l2(void);
    void pascal near shot_yuuka_l3(void);
    void pascal near shot_yuuka_l4(void);
    void pascal near shot_yuuka_l5(void);
    void pascal near shot_yuuka_l6(void);
    void pascal near shot_yuuka_l7(void);
    void pascal near shot_yuuka_l8(void);
    void pascal near shot_yuuka_l9(void);
}

#endif

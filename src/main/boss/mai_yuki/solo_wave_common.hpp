#ifndef TH05_MAI_YUKI_SOLO_WAVE_COMMON_HPP
#define TH05_MAI_YUKI_SOLO_WAVE_COMMON_HPP

// Mai and Yuki both complete a *real* solo reposition before counting a new
// attack pattern. Keep the original write ordering and do not use a helper
// function that would change stack/call layout.
#define MY_SOLO_NEXT_PATTERN() \
    boss.phase_frame = 0; \
    boss.mode++; \
    boss.phase_state.patterns_seen++

// A missed shot exits the outer Boss phase switch directly. The two
// characters supply their own original score bonus and independent HP gate.
#define MY_SOLO_HIT_BONUS_OR_BREAK(score_bonus) \
    if(!boss_hittest_shots()) { \
        break; \
    } \
    boss_score_bonus(score_bonus)

#endif

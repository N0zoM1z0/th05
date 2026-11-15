#ifndef TH05_MAI_YUKI_SOLO_WAVE_COMMON_HPP
#define TH05_MAI_YUKI_SOLO_WAVE_COMMON_HPP

// Mai and Yuki each finish a solo reposition before counting the next attack.
// This stays a macro: a helper function would change the generated code.
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

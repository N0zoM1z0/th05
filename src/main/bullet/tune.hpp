// Local difficulty/performance tuning ABI; candidate source provenance is
// nmlgc/ReC98@b6ba5b0a529edbb3. Acceptance requires this repository's replay.
#ifndef TH05_MAIN_BULLET_TUNE_HPP
#define TH05_MAIN_BULLET_TUNE_HPP

#include "src/main/bullet/template.hpp"

extern "C" {
    extern unsigned char playperf;
    extern BulletTemplate bullet_template;

    void pascal near tune_for_easy(void);
    void pascal near tune_for_hard(void);
    void pascal near tune_for_lunatic(void);
    void pascal near tune_for_playperf(void);
    void pascal near bullet_template_tune_easy(void);
    void pascal near bullet_template_tune_normal(void);
    void pascal near bullet_template_tune_hard(void);
    void pascal near bullet_template_tune_lunatic(void);
}

#endif

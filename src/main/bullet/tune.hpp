// Bullet template tuning by difficulty and play performance ("playperf").
// The tune_for_*() helpers are implemented in spawn_raw.asm.
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

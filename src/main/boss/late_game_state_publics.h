/* Three physical initialized C near-DATA owners, imported by the original
 * Turbo C++ HUD, midboss, bullet-zap and EX-Alice update functions. */
#ifndef TH05_MAIN_LATE_GAME_STATE_PUBLICS_H
#define TH05_MAIN_LATE_GAME_STATE_PUBLICS_H
#ifdef __cplusplus
extern "C" {
/* bool becomes `typedef unsigned char bool` in resident.hpp below. */
extern unsigned char near bullet_zap_drop_point_items;
extern int near hud_hp_bar_value_prev;
extern unsigned char near midboss_defeat_angle;
}
#else
extern unsigned char near bullet_zap_drop_point_items;
extern int near hud_hp_bar_value_prev;
extern unsigned char near midboss_defeat_angle;
#endif
#endif

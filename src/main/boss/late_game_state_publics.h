/* Three unrelated globals that ZUN defined in C. They are shared by the
 * bullet zap and EX-Alice (bullet_zap_drop_point_items), the HUD and the
 * midboss code (hud_hp_bar_value_prev), and the midboss defeat effect. */
#ifndef TH05_MAIN_LATE_GAME_STATE_PUBLICS_H
#define TH05_MAIN_LATE_GAME_STATE_PUBLICS_H
#ifdef __cplusplus
extern "C" {
/* Declared as unsigned char: the `bool` typedef from resident.hpp is not */
/* visible yet, and Turbo C++ rejects declaring it earlier. */
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

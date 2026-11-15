/* Small initialized staff roll state, defined by the staff_*.c files.
 * These are C symbols; include this header before any C++ header that
 * redeclares them, so that the C linkage wins. */
#ifndef TH05_MAINE_STAFF_STATE_PUBLICS_H
#define TH05_MAINE_STAFF_STATE_PUBLICS_H
#ifdef __cplusplus
extern "C" {
#endif
extern unsigned char near staff_back_page;
extern int near staff_spark_cursor;
extern int near staff_orb_opening_frame;
extern unsigned char near staff_camera_accel_phase;
extern int near staff_rain_cursor;
extern int near staff_rain_frame;
extern unsigned char near staff_text_clear_requested;
extern int near staff_image_phase_a;
extern int near staff_image_phase_b;
#ifdef __cplusplus
}
#endif
#endif

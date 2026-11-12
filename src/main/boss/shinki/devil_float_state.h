/* The two original C DATA publics used by Shinki's Devil and float leaf. */
#ifndef TH05_SHINKI_DEVIL_FLOAT_STATE_H
#define TH05_SHINKI_DEVIL_FLOAT_STATE_H
#ifdef __cplusplus
extern "C" {
extern int near shinki_devil_laser_grow_delay;
/* The Borland one-byte C++ bool reads the identical physical C byte. */
extern bool near shinki_float_direction;
}
#else
extern int near shinki_devil_laser_grow_delay;
extern unsigned char near shinki_float_direction;
#endif
#endif

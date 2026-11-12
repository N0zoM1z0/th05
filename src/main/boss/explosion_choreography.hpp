// Actual Boss small/big explosion ring and native palette-flash cadence.
// Compile-time gameplay rules; no replacement Explosion16 state or BSS.
#ifndef TH05_BOSS_EXPLOSION_CHOREOGRAPHY_HPP
#define TH05_BOSS_EXPLOSION_CHOREOGRAPHY_HPP
#define BEXP_LIFETIME_FRAMES 32
#define BEXP_SMALL_SPRITE_W 16
#define BEXP_SMALL_SPRITE_H 16
#define BEXP_SMALL_RING_SPRITES 64
#define BEXP_BIG_CLIP_ASSUMED_W 64
#define BEXP_BIG_CLIP_ASSUMED_H 64
#define BEXP_BIG_RING_SPRITES 16
#define BEXP_FULL_CIRCLE_ANGLE 0x100
#define BEXP_BIG_FLASH_END_FRAME 8
#define BEXP_BIG_FADE_END_FRAME 16
#define BEXP_BIG_ODD_FRAME_MASK 1
#define BEXP_BIG_FLASH_TONE 150
#define BEXP_BASE_TONE 100
#define BEXP_FADE_TONE_PER_FRAME 6
#endif

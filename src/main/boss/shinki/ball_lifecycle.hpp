// Original Shinki 32x32 B6-ball cloud, collision and decay lifecycle.
// Constants only: custom_entities[1..63] remains the actual 26-byte backing.
#ifndef TH05_SHINKI_BALL_LIFECYCLE_HPP
#define TH05_SHINKI_BALL_LIFECYCLE_HPP

// From a 48-pixel birth cloud, every frame shrinks by 2 pixels until the
// radius falls strictly below the 16-pixel sprite half-width.
#define SHINKI_B6_BIRTH_CLOUD_RADIUS_PX 48.0f
#define SHINKI_B6_CLOUD_SHRINK_PX 2.0f
#define SHINKI_B6_HITBOX_HALF_DIVISOR 2
#define SHINKI_B6_DECAY_VELOCITY_DIVISOR 2
#define SHINKI_B6_DECAY_ANIMATION_INTERVAL 4

#endif

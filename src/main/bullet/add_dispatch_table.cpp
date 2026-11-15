// Bullet spawn functions selected by the enemy script's bullet command: after
// tuning [bullet_template], the script interpreter calls
// bullets_add_by_mode[mode] (ReC98 th05_main.asm: `call off_2129C[bx]`).
#pragma option -zCBULLET_DISPATCH_DATA_TEXT -zPmain_03

#pragma codeseg B6_UPDATE_TEXT main_03
extern "C" {
    void near bullets_add_regular(void);
    void near bullets_add_regular_fixedspeed(void);
    void near bullets_add_special(void);
}
#pragma codeseg BULLET_DISPATCH_DATA_TEXT main_03

// Indexed by spawn mode: regular, fixed-speed (no playperf speed tuning),
// and special-motion bullets.
typedef void (near *near BulletAddCallback)(void);
BulletAddCallback near bullets_add_by_mode[3] = {
    bullets_add_regular,
    bullets_add_regular_fixedspeed,
    bullets_add_special
};

typedef char bullet_dispatch_pointer_is_two[(sizeof(BulletAddCallback) == 2) ? 1 : -1];
typedef char bullet_dispatch_three_is_six[(sizeof(bullets_add_by_mode) == 6) ? 1 : -1];

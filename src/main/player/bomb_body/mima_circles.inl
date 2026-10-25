void near mima_circles_update_and_render(void)
{
    mima_circle_t near *circle;
    int i;
    if(bomb_frame == 1) {
        PaletteTone = 100;
        palette_changed = true;
        for(i = 0; i < MIMA_CIRCLE_COUNT; i++) {
            bomb_anim.mima[i].center.x = BOMB_PIXEL_NONE;
        }
    }
    if(bomb_frame % 4 == 0) {
        i = ((bomb_frame - 16) / 4) & (MIMA_CIRCLE_COUNT - 1);
        circle = &bomb_anim.mima[i];
        // The original seeds the center with the player's full two-word point,
        // then overwrites it below with pixel-space polar coordinates.
        reinterpret_cast<SPPoint near &>(circle->center) = player_pos.cur;
        circle->distance = 256;
        circle->angle = randring1_next16();
    }
    circle = bomb_anim.mima;
    for(i = 0; i < MIMA_CIRCLE_COUNT; i++, circle++) {
        if(circle->center.x != BOMB_PIXEL_NONE) {
            vector2_at(reinterpret_cast<SPPoint near &>(circle->center),
                224, 117, circle->distance, circle->angle);
            grcg_circlefill(circle->center.x, circle->center.y, circle->distance / 2);
            circle->distance -= 16;
            if(circle->distance < 4) {
                circle->center.x = BOMB_PIXEL_NONE;
            }
        }
    }
}

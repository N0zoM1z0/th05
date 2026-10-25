#define bomb_beam_color(color) { _AH = color; grcg_setcolor_direct_raw(); }
static const pixel_t MARISA_BEAM_NONE = -999;

void near marisa_lasers_update_and_render(void)
{
    marisa_laser_t near *laser;
    int i;
    int x;
    int y;
    int half_width;
    if(bomb_frame == 16) {
        PaletteTone = 100;
        palette_changed = true;
        for(i = 0; i < MARISA_LASER_COUNT; i++) {
            bomb_anim.marisa[i].center.x.v = MARISA_BEAM_NONE;
        }
    }
    if(bomb_frame % 4 == 0) {
        i = ((bomb_frame - 16) / 4) & (MARISA_LASER_COUNT - 1);
        laser = &bomb_anim.marisa[i];
        laser->center = player_pos.cur;
        bomb_sparks_add_at_player();
        laser->center.x.v = player_pos.cur.x.v;
        laser->center.y.v = player_pos.cur.y.v;
        laser->radius = 24;
        snd_se_play(15);
        PaletteTone = 170;
    } else {
        PaletteTone = 100;
    }
    palette_show();
    grcg_setmode_rmw();
    laser = bomb_anim.marisa;
    for(i = 0; i < MARISA_LASER_COUNT; i++, laser++) {
        if(laser->center.x.v != MARISA_BEAM_NONE) {
            x = laser->center.x.v / 16 + PLAYFIELD_LEFT;
            y = laser->center.y.v / 16 + PLAYFIELD_TOP;
            bomb_beam_color(8);
            half_width = laser->radius / 2;
            grcg_boxfill(x - half_width, PLAYFIELD_TOP, x + half_width, y);
            bomb_beam_color(9);
            half_width--;
            grcg_boxfill(x - half_width, PLAYFIELD_TOP, x + half_width, y);
            bomb_beam_color(V_WHITE);
            half_width--;
            grcg_boxfill(x - half_width, PLAYFIELD_TOP, x + half_width, y);
            grcg_circlefill(x, y, laser->radius);
            laser->radius--;
            if(laser->radius < 4) {
                laser->center.x.v = MARISA_BEAM_NONE;
            }
        }
    }
    outportb(0x7C, 0);
}

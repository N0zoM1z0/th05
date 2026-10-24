// Shared natural implementation; no layout or instruction bytes are supplied.
void near alice_pattern_final_spread(void)
{
    bullet_template.spawn_type = 0x10;
    bullet_template.group = BG_SPREAD;
    bullet_template.angle = 0x40;
    bullet_template.patnum = 84;
    if((boss.phase_frame % 32) == 0) {
        bullet_template.speed.v = to_sp(2);
        reinterpret_cast<uint16_t &>(bullet_template.spread) = 13 | (10 << 8);
        bullet_template_tune();
        bullets_add_regular();
        snd_se_play(3);
    }
}

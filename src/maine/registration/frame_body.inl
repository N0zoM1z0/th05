void near registration_frame(void)
{
    snd_se_update();
    glyphballs_update();
    frame_delay(1);
    outportb(0xA6, registration_page);
    registration_page = 1 - registration_page;
    outportb(0xA4, registration_page);
}

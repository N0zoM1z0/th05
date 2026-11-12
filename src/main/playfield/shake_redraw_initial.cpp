// ReC98 th04/main/playfld[data].asm: original one-byte shake redraw clock.
#pragma option -zCSHAKE_REDRAW_INIT_TEXT -zPmain_01

char playfield_shake_redraw_time = 0;
typedef char shake_redraw_clock_is_byte[(sizeof(playfield_shake_redraw_time) == 1) ? 1 : -1];

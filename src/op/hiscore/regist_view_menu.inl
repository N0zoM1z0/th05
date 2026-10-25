// One canonical natural menu definition, shared by bounded producer contexts.
void near regist_view_menu(void)
{
	snd_kaja_func(KAJA_SONG_STOP, 0);
	snd_load(hi_filenames.hiscore_bgm, SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);

	// ZUN bloat: This both
	// * doesn't work, because fade-ins require the volume to be set to a lower
	//   value than what [KAJA_SONG_PLAY] resets it to, and
	// * sounds terrible, because -128 is the fastest but still not quite
	//   instant fade speed. This leaves the initial note on each channel muted
	//   while the rest of the track fades in very abruptly, clashing with the
	//   bass and chord notes of the name registration themes in both games.
	snd_kaja_func(KAJA_SONG_FADE, -128);

	palette_black_out(1);
	rank = resident->rank;

	pi_load(0, hi_filenames.hiscore_background);
	rank_render();
	palette_black_in(1);

	while(1) {
		// ZUN bug: The TH04 version of this function doesn't address the PC-98
		// keyboard quirk documented in the `Research/HOLDKEY` example, which
		// causes input to occasionally be processed a frame or two later than
		// expected. Not that big of a deal given that every key press launches
		// a 16-frame palette fade animation, but a bug nonetheless.
		input_reset_sense_interface();
		frame_delay(1);

		// ZUN bloat: Testing twice for [INPUT_OK].
		if(
			(key_det & INPUT_OK) || (key_det & INPUT_SHOT) ||
			(key_det & INPUT_CANCEL) || (key_det & INPUT_OK)
		) {
			break;
		}
		if((key_det & INPUT_LEFT) && (rank != RANK_EASY)) {
			rank--;
			palette_settone(0);
			rank_render();
			palette_black_in(1);
		}
		if((key_det & INPUT_RIGHT) && (rank < RANK_EXTRA)) {
			rank++;
			palette_settone(0);
			rank_render();
			palette_black_in(1);
		}
	}

	snd_kaja_func(KAJA_SONG_FADE, 1);
	palette_black_out(1);
	pi_free(0);
	graph_accesspage(1);
	pi_fullres_load_palette_apply_put_free(0, hi_filenames.menu_background);
	graph_copy_page(0);
	palette_black_in(1);

	do {
		// ZUN bug: With that one PC-98 keyboard quirk still not addressed in
		// TH04, the loop will break relatively quickly even while the player
		// is still holding a key. This cuts short any attempt to listen to the
		// fade-out by holding a key. In TH05, this works as intended.
		// (At least it proves that this loop wasn't actually necessary to
		// ensure that this menu isn't re-entered, confirming this entire loop
		// to be an easter egg that allows the player to actually listen to the
		// BGM fade-out.)
		input_reset_sense_interface();
		frame_delay(1);
	} while(key_det != INPUT_NONE);

	snd_kaja_func(KAJA_SONG_STOP, 0);
	snd_load(hi_filenames.menu_bgm, SND_LOAD_SONG);
	snd_kaja_func(KAJA_SONG_PLAY, 0);
}

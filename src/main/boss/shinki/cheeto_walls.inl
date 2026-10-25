void near pattern_cheetos_within_spread_walls(void)
{
	#define interval	boss_statebyte[14]
	#define unused  	boss_statebyte[15]

	if(boss.phase_frame < 128) {
		return;
	}
	if(boss.phase_frame == 128) {
		// Expected to be a multiple of 8.
		interval = select_for_rank(128, 48, 32, 24);

		unused = select_for_rank(32, 40, 48, 56);
	}
	int frame_in_cycle = (boss.phase_frame % interval);
	if((frame_in_cycle & 7) == 0) {
		bullet_template.patnum = PAT_BULLET16_N_OUTLINED_BALL_BLUE;
		bullet_template.spawn_type = (BST_CLOUD_FORWARDS | BST_NO_DECELERATE);
		bullet_template.group = BG_SPREAD;
		bullet_template.speed.v = sara_rand_speed(3.0f, 5.0f);
		sara_set_spread(6, 0x08);
		bullet_template.angle = 0x68;
		bullets_add_regular();

		bullet_template.angle = 0x18;
		bullets_add_regular();
		if(frame_in_cycle == 0) {
			cheeto_template.col = 11;
			cheeto_template.speed.v = sara_to_sp8(4.0f);
			// Firing either right, down, or left.
			cheeto_template.angle = (randring2_next16_mod(3) * 0x40);
			cheetos_add();
			snd_se_play(3);
		}
	}

	#undef unused
	#undef interval
}

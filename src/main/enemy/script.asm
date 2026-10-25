; Complete TH05 STD enemy bytecode interpreter and its private SI/CF helpers.
; Semantic reconstruction from native contracts and pinned ReC98 candidate.
; SI = current 64-byte enemy; ES = script segment; DI = current instruction.
; CL = instruction age; AH = first byte argument/duration; AL = encoded length.
; Timed instructions return AL=0; REMOVE returns AL=1. Invalid opcodes retain
; the original unspecified AL result. No C/C++ calling convention is invented.
.386
.model large
include types.inc
include symbols.inc

PLAYFIELD_W equ 384
PLAYFIELD_H equ 368
ENEMY_W equ 32
ENEMY_H equ 32
ENEMY_CLIP_X equ 01h
ENEMY_CLIP_Y equ 10h
RANK_EASY equ 0
RANK_LUNATIC equ 3
SCRIPT_OPCODE_COUNT equ 59
AUTOFIRE_INTERVAL_MIN equ 16

ENEMY_VM_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_VM_TEXT, ds:DGROUP, es:nothing
public enemy_pos_update, enemy_velocity_set, enemy_aim_velocity_set
public enemy_bullet_template_copy, enemy_script_update, _enemy_script_update
public script_handlers, script_handlers_end, enemy_vm_family_end
enemy_pos_update	proc near
		lea	ax, [si+enemy_t.pos]
		push	ax
		call	@PlayfieldMotion@update_seg3$qv
		test	[si+enemy_t.E_clip], ENEMY_CLIP_X
		jz	short @@clip_y?

		; Note that these comparisons abuse underflow to implicitly handle the
		; negative direction as well.
		add	ax, ((ENEMY_W / 2) shl 4)
		cmp	ax, ((PLAYFIELD_W + ENEMY_W) shl 4)
		jnb	short @@clip

@@clip_y?:
		test	[si+enemy_t.E_clip], ENEMY_CLIP_Y
		jz	short @@on_playfield
		add	dx, ((ENEMY_H / 2) shl 4)
		cmp	dx, ((PLAYFIELD_H + ENEMY_H) shl 4)
		jnb	short @@clip

@@on_playfield:
		clc
		retn


@@clip:
		inc	_enemies_gone
		stc
		retn
enemy_pos_update	endp




public ENEMY_VELOCITY_SET
enemy_velocity_set	proc near
		lea	ax, [si+enemy_t.pos.velocity.x]
		push	ax
		push	word ptr [si+enemy_t.E_angle]
		xor	ah, ah
		mov	al, [si+enemy_t.E_speed]
		push	ax
		call	vector2_near
		retn
enemy_velocity_set	endp





enemy_aim_velocity_set	proc near
		push	es
		push	word ptr [si+enemy_t.pos.cur.x]
		push	word ptr [si+enemy_t.pos.cur.y]
		push	word ptr [si+enemy_t.E_angle]
		call	@player_angle_from$q20%SubpixelBase$ti$ti%t1uc
		mov	[si+enemy_t.E_angle], al
		pop	es
		call	enemy_velocity_set
		retn
enemy_aim_velocity_set	endp





enemy_bullet_template_copy	proc near
		push	si
		push	di
		mov	cx, size bullet_template_t / 2
		add	si, enemy_t.E_bullet_template
		push	es
		push	ds
		pop	es
		assume es:_DATA
		mov	di, offset _bullet_template
		rep movsw
		pop	es
		assume es:nothing
		pop	di
		pop	si
		retn
enemy_bullet_template_copy	endp


		even




_enemy_script_update label near
enemy_script_update	proc near
		push	si
		push	di
		mov	si, _enemy_cur
		mov	es, _std_seg

script_fetch:
		mov	di, [si+enemy_t.E_script]
		add	di, [si+enemy_t.E_script_ip]
		mov	bl, es:[di]
		mov	bh, 0
		cmp	bx, SCRIPT_OPCODE_COUNT - 1
		ja	script_return
		mov	cl, [si+enemy_t.E_cur_instr_frame]
		mov	al, 1
		mov	ah, es:[di+1]
		xor	dx, dx
		add	bx, bx
		jmp	cs:script_handlers[bx]

script_remove:
		mov	byte ptr [si], 2
		mov	al, 1
		jmp	script_return


; Timed polar movement: initialization is only on the first instruction frame.
op_move_set:
		or	cl, cl
		jnz	short move_set_step
		mov	ax, es:[di+1]
		mov	[si+enemy_t.E_speed], ah
		mov	[si+enemy_t.E_angle], al
		call	enemy_velocity_set

move_set_step:
		call	enemy_pos_update
		jb	short script_remove
		mov	ah, es:[di+3]
		mov	al, 4
		jmp	finish_timed


op_move_current:
		or	cl, cl
		jnz	short move_current_step
		call	enemy_velocity_set

move_current_step:
		call	enemy_pos_update
		jb	short script_remove
		mov	ah, es:[di+1]
		mov	al, 2
		jmp	finish_timed


op_move_speed:
		or	cl, cl
		jnz	short move_speed_step
		mov	al, es:[di+1]
		mov	[si+enemy_t.E_speed], al
		call	enemy_velocity_set

move_speed_step:
		call	enemy_pos_update
		jb	short script_remove
		mov	ah, es:[di+2]
		mov	al, 3
		jmp	finish_timed


; Turning updates recompute velocity and then add an optional signed drift.
op_turn_start_with_drift:
		inc	dl

op_turn_start:
		or	cl, cl
		jnz	short turn_start_apply
		mov	ax, es:[di+1]
		mov	[si+enemy_t.E_speed], ah
		mov	[si+enemy_t.E_angle], al
		mov	al, es:[di+3]
		mov	[si+enemy_t.E_angle_delta], al

turn_start_apply:
		push	dx
		call	enemy_velocity_set
		pop	dx
		or	dl, dl
		jz	short turn_start_duration
		mov	al, es:[di+4]
		cbw
		add	[si+enemy_t.pos.velocity.x], ax
		mov	al, es:[di+5]
		cbw
		add	[si+enemy_t.pos.velocity.y], ax
		mov	ah, es:[di+6]
		mov	al, 7
		jmp	short turn_start_move


turn_start_duration:
		mov	ah, es:[di+4]
		mov	al, 5

turn_start_move:
		jmp	short turn_advance


; Original bug: unlike turn-start, this path does not preserve DX across
; vector2_near. That helper returns velocity Y in DX, so DL tests its low byte
; rather than reliably retaining the requested drift mode. Preserve the bug.
op_turn_current_with_drift:
		inc	dl

op_turn_current:
		call	enemy_velocity_set
		or	dl, dl
		jz	short turn_current_duration
		mov	al, es:[di+1]
		cbw
		add	[si+enemy_t.pos.velocity.x], ax
		mov	al, es:[di+2]
		cbw
		add	[si+enemy_t.pos.velocity.y], ax
		mov	ah, es:[di+3]
		mov	al, 4
		jmp	short turn_advance


turn_current_duration:
		mov	ah, es:[di+1]
		mov	al, 2

turn_advance:
		push	ax
		call	enemy_pos_update
		pop	ax
		jb	script_remove
		mov	dl, [si+enemy_t.E_angle_delta]
		add	[si+enemy_t.E_angle], dl
		jmp	finish_timed


op_wait:
		or	cl, cl
		jnz	short wait_timed
		mov	eax, dword ptr [si+enemy_t.pos.cur]
		mov	dword ptr [si+enemy_t.pos.prev], eax
		jmp	short wait_timed


op_scroll:
		or	cl, cl
		jnz	short scroll_move
		mov	[si+enemy_t.pos.velocity.x], 0

scroll_move:
		mov	ax, _scroll_last_delta
		mov	[si+enemy_t.pos.velocity.y], ax
		call	enemy_pos_update
		jb	script_remove

wait_timed:
		mov	ah, es:[di+1]
		mov	al, 2
		jmp	finish_timed


; Wave motion: Q8 cosine amplitude, signed drift, optional axis exchange.
op_wave_vertical:
		inc	dl

op_wave_horizontal:
		or	cl, cl
		jnz	short wave_move
		mov	[si+enemy_t.E_angle], 0
		mov	al, es:[di+2]
		mov	[si+enemy_t.E_angle_delta], al

wave_move:
		mov	cl, dl
		movzx	eax, byte ptr es:[di+1]
		mov	bl, [si+enemy_t.E_angle]
		mov	bh, 0
		add	bx, bx
		movsx	edx, _CosTable8[bx]
		imul	eax, edx
		sar	eax, 8
		mov	[si+enemy_t.pos.velocity.x], ax
		mov	al, es:[di+3]
		cbw
		mov	[si+enemy_t.pos.velocity.y], ax
		or	cl, cl
		jnz	short wave_advance
		mov	dx, [si+enemy_t.pos.velocity.x]
		mov	ax, [si+enemy_t.pos.velocity.y]
		mov	[si+enemy_t.pos.velocity.x], ax
		mov	[si+enemy_t.pos.velocity.y], dx

wave_advance:
		call	enemy_pos_update
		jb	script_remove
		mov	al, [si+enemy_t.E_angle_delta]
		add	[si+enemy_t.E_angle], al
		mov	ah, es:[di+4]
		mov	al, 5
		jmp	finish_timed


op_aim:
		mov	ax, es:[di+1]
		mov	[si+enemy_t.E_angle], al
		mov	[si+enemy_t.E_speed], ah
		call	enemy_aim_velocity_set
		mov	al, 3
		jmp	advance_and_continue


op_angle_add:
		add	[si+enemy_t.E_angle], ah
		jmp	short polar_update


op_speed_add:
		add	[si+enemy_t.E_speed], ah

polar_update:
		call	enemy_velocity_set
		mov	al, 2
		jmp	advance_and_continue


op_angle_random:
		call	@randring2_next16$qv
		mov	[si+enemy_t.E_angle], al
		mov	al, 1
		jmp	advance_and_continue


; Three emission callbacks share the tuned, enemy-relative bullet template.
op_emit_slot2:
		mov	dl, 2
		jmp	short op_emit_slot0


op_emit_slot1:
		inc	dl

op_emit_slot0:
		mov	enemy_vm_emitter_slot, dx
		call	enemy_bullet_template_copy
		mov	ax, [si+enemy_t.pos.cur.x]
		add	word ptr _bullet_template[bullet_template_t.BT_origin.x], ax
		mov	ax, [si+enemy_t.pos.cur.y]
		add	word ptr _bullet_template[bullet_template_t.BT_origin.y], ax
		push	es
		call	_bullet_template_tune
		mov	bx, enemy_vm_emitter_slot
		add	bx, bx
		call	enemy_bullet_emitters[bx]
		pop	es
		mov	al, 1
		jmp	advance_and_continue


op_bullet_set:
		mov	[si+enemy_t.E_autofire], 0
		mov	[si+enemy_t.E_bullet_template.spawn_type], ah
		mov	ax, es:[di+2]
		mov	[si+enemy_t.E_bullet_template.BT_group], al
		mov	[si+enemy_t.E_bullet_template.BT_angle], ah
		mov	ax, es:[di+4]
		mov	[si+enemy_t.E_bullet_template.speed], al
		mov	[si+enemy_t.E_bullet_template.patnum], ah
		mov	al, 6
		jmp	advance_and_continue


op_bullet_spawn:
		mov	[si+enemy_t.E_bullet_template.spawn_type], ah
		jmp	short advance_two


op_bullet_origin:
		mov	eax, es:[di+1]
		mov	dword ptr [si+enemy_t.E_bullet_template.BT_origin], eax
		mov	al, 5
		jmp	advance_and_continue


op_bullet_angle:
		mov	[si+enemy_t.E_bullet_template.BT_angle], ah
		jmp	short advance_two


op_bullet_angle_add:
		add	[si+enemy_t.E_bullet_template.BT_angle], ah
		jmp	short advance_two


op_bullet_angle_random:
		call	@randring2_next16$qv
		mov	[si+enemy_t.E_bullet_template.BT_angle], al
		mov	al, 1
		jmp	advance_and_continue


op_bullet_pattern:
		mov	[si+enemy_t.E_bullet_template.patnum], ah
		jmp	short advance_two


op_bullet_speed:
		mov	[si+enemy_t.E_bullet_template.speed], ah
		jmp	short advance_two


op_bullet_speed_add:
		add	[si+enemy_t.E_bullet_template.speed], ah
		jmp	short advance_two


op_bullet_group:
		mov	[si+enemy_t.E_bullet_template.BT_group], ah

advance_two:
		mov	al, 2
		jmp	advance_and_continue


; Rank/performance-adjusted interval: scale around playperf32 and clamp.
op_autofire_interval:
		mov	al, ah
		xor	ah, ah
		mov	dl, _playperf
		cmp	dl, 32
		jbe	short interval_slow
		sub	dl, 32
		mul	dl
		shr	ax, 6
		xor	dh, dh
		mov	dl, es:[di+1]
		sub	dx, ax
		cmp	dl, AUTOFIRE_INTERVAL_MIN
		jnb	short interval_rank
		mov	dl, AUTOFIRE_INTERVAL_MIN
		jmp	short interval_rank


interval_slow:
		mov	cl, 32
		sub	cl, dl
		mul	cl
		shr	ax, 6
		xor	dh, dh
		mov	dl, es:[di+1]
		add	dx, ax
		cmp	dx, 256
		jb	short interval_rank
		mov	dl, 255

interval_rank:
		cmp	_rank, RANK_EASY
		jnz	short interval_store
		mov	dl, 255

interval_store:
		mov	[si+enemy_t.E_autofire_interval], dl
		jmp	short advance_two


op_autofire_on:
		inc	dl

op_autofire_off:
		mov	[si+enemy_t.E_autofire], dl
		jmp	advance_and_continue


op_bullet_spread:
		mov	[si+enemy_t.E_bullet_template.spread], ah
		mov	al, es:[di+2]
		mov	[si+enemy_t.E_bullet_template.spread_angle_delta], al

advance_three:
		mov	al, 3
		jmp	advance_and_continue


op_bullet_stack:
		mov	[si+enemy_t.E_bullet_template.BT_stack], ah
		mov	al, es:[di+2]

stack_speed_store:
		mov	[si+enemy_t.E_bullet_template.stack_speed_delta], al

stack_advance:
		jmp	short advance_three


op_bullet_motion:
		mov	[si+enemy_t.E_bullet_template.BT_special_motion], ah
		jmp	short advance_two


op_bullet_aim:
		push	es
		mov	ax, [si+enemy_t.pos.cur.x]
		add	ax, [si+enemy_t.E_bullet_template[bullet_template_t.BT_origin.x]]
		push	ax
		mov	ax, [si+enemy_t.pos.cur.y]
		add	ax, [si+enemy_t.E_bullet_template[bullet_template_t.BT_origin.y]]
		push	ax
		push	word ptr es:[di+1]
		call	@player_angle_from$q20%SubpixelBase$ti$ti%t1uc
		mov	[si+enemy_t.E_bullet_template.BT_angle], al
		pop	es

aim_advance:
		jmp	advance_two


; Enemy visual/combat state instructions execute without waiting a frame.
op_attributes:
		inc	dl
		mov	[si+enemy_t.flag], dl
		mov	[si+enemy_t.E_patnum_base], ah
		mov	ax, es:[di+2]
		mov	[si+enemy_t.E_hp], ax
		mov	ax, es:[di+4]
		mov	[si+enemy_t.E_score], ax
		mov	[si+enemy_t.E_can_be_damaged], dl
		mov	[si+enemy_t.E_kills_player_on_collision], dl
		mov	al, 6
		jmp	advance_and_continue


op_clip_both:
		mov	[si+enemy_t.E_clip], (ENEMY_CLIP_X or ENEMY_CLIP_Y)
		jmp	advance_and_continue


op_clip_x:
		or	[si+enemy_t.E_clip], ENEMY_CLIP_X
		jmp	advance_and_continue


op_clip_y:
		or	[si+enemy_t.E_clip], ENEMY_CLIP_Y
		jmp	advance_and_continue


op_animation:
		mov	[si+enemy_t.E_anim_cels], ah
		mov	al, es:[di+2]
		mov	[si+enemy_t.E_anim_frames_per_cel], al
		mov	al, 3
		jmp	advance_and_continue


op_sound:
		mov	al, ah
		mov	ah, 0
		push	ax
		call	snd_se_play

advance_two_sound:
		mov	al, 2
		jmp	advance_and_continue


op_pattern:
		mov	[si+enemy_t.E_patnum_base], ah
		jmp	short advance_two_sound


op_invulnerable:
		mov	[si+enemy_t.E_can_be_damaged], dl

autofire_store_advance:
		mov	[si+enemy_t.E_autofire], dl
		jmp	advance_and_continue


op_vulnerable_lunatic_autofire:
		mov	[si+enemy_t.E_can_be_damaged], 1
		cmp	_rank, RANK_LUNATIC
		jnz	short autofire_store_advance
		inc	dl
		jmp	short autofire_store_advance


op_collision_on:
		inc	dl

op_collision_off:
		mov	[si+enemy_t.E_kills_player_on_collision], dl
		jmp	advance_and_continue


; Teleports preserve the previous position and yield once through timed finish.
op_position:
		mov	eax, dword ptr [si+enemy_t.pos.cur]
		mov	dword ptr [si+enemy_t.pos.prev], eax
		mov	eax, es:[di+1]
		mov	dword ptr [si+enemy_t.pos.cur],	eax
		jmp	short position_timed


op_position_add:
		mov	eax, dword ptr [si+enemy_t.pos.cur]
		mov	dword ptr [si+enemy_t.pos.prev], eax
		mov	ax, es:[di+1]
		add	[si+enemy_t.pos.cur.x], ax
		mov	ax, es:[di+3]
		add	[si+enemy_t.pos.cur.y], ax

position_timed:
		mov	ah, 0
		mov	al, 5
		jmp	short finish_timed


op_pattern_add:
		add	[si+enemy_t.E_patnum_base], ah
		mov	al, 2
		jmp	short advance_and_continue


op_velocity:
		mov	[si+enemy_t.E_angle], ah
		mov	al, es:[di+2]
		mov	[si+enemy_t.E_speed], al

velocity_advance:
		call	enemy_velocity_set
		mov	al, 3
		jmp	short advance_and_continue


op_velocity_mirror:
		mov	[si+enemy_t.E_angle], ah
		mov	al, es:[di+2]
		mov	[si+enemy_t.E_speed], al
		cmp	[si+enemy_t.E_spawned_in_left_half], 0
		jnz	short velocity_advance
		mov	al, 80h
		sub	al, ah
		mov	[si+enemy_t.E_angle], al
		jmp	short velocity_advance


op_speed:
		mov	[si+enemy_t.E_speed], ah
		call	enemy_velocity_set
		mov	al, 2
		jmp	short advance_and_continue


; Backward relative loops share the single per-enemy loop counter.
op_repeat:
		mov	al, [si+enemy_t.E_loop_i]
		cmp	al, es:[di+2]
		jb	short repeat_back
		mov	[si+enemy_t.E_loop_i], 0
		mov	al, 3
		jmp	short advance_and_continue


repeat_back:
		inc	[si+enemy_t.E_loop_i]

op_jump_back:
		mov	al, ah
		mov	ah, 0

jump_back_apply:
		sub	[si+enemy_t.E_script_ip], ax
		jmp	script_fetch


op_subtype_skip:
		mov	al, 3
		cmp	ah, [si+enemy_t.E_subtype]
		jz	short advance_and_continue
		add	al, es:[di+2]
		; Original inert branch: checked, zero authored credit.
		jz	short advance_and_continue

advance_and_continue:
		mov	ah, 0
		add	[si+enemy_t.E_script_ip], ax
		jmp	script_fetch


; Duration is tested before increment: reaching it advances IP and yields.
finish_timed:
		cmp	ah, [si+enemy_t.E_cur_instr_frame]
		ja	short timed_wait
		mov	ah, 0
		mov	[si+enemy_t.E_cur_instr_frame], ah
		add	[si+enemy_t.E_script_ip], ax
		jmp	short timed_done


timed_wait:
		inc	[si+enemy_t.E_cur_instr_frame]

timed_done:
		xor	ax, ax

script_return:
		pop	di
		pop	si
		retn
enemy_script_update	endp


script_handlers label word
		dw offset script_remove
		dw offset op_attributes
		dw offset op_move_set
		dw offset op_move_current
		dw offset op_move_speed
		dw offset op_turn_start
		dw offset op_turn_start_with_drift
		dw offset op_turn_current
		dw offset op_turn_current_with_drift
		dw offset op_wait
		dw offset op_scroll
		dw offset op_wave_vertical
		dw offset op_wave_horizontal
		dw offset op_aim
		dw offset op_angle_add
		dw offset op_speed_add
		dw offset op_angle_random
		dw offset op_emit_slot0
		dw offset op_bullet_set
		dw offset op_bullet_spawn
		dw offset op_bullet_origin
		dw offset op_bullet_angle
		dw offset op_bullet_angle_add
		dw offset op_bullet_angle_random
		dw offset op_bullet_pattern
		dw offset op_bullet_speed
		dw offset op_bullet_speed_add
		dw offset op_bullet_group
		dw offset op_autofire_interval
		dw offset op_autofire_on
		dw offset op_autofire_off
		dw offset op_bullet_angle_add
		dw offset op_bullet_spread
		dw offset op_bullet_stack
		dw offset op_clip_x
		dw offset op_clip_y
		dw offset op_clip_both
		dw offset op_animation
		dw offset op_sound
		dw offset op_pattern
		dw offset op_invulnerable
		dw offset op_vulnerable_lunatic_autofire
		dw offset op_collision_off
		dw offset op_collision_on
		dw offset op_position
		dw offset op_position_add
		dw offset op_pattern_add
		dw offset op_velocity
		dw offset op_velocity_mirror
		dw offset op_speed
		dw offset op_repeat
		dw offset op_repeat
		dw offset op_subtype_skip
		dw offset op_jump_back
		dw offset move_current_step
		dw offset op_emit_slot2
		dw offset op_bullet_motion
		dw offset op_emit_slot1
		dw offset op_bullet_aim

script_handlers_end label word
		even

enemy_vm_family_end label byte
ENEMY_VM_TEXT ends
end

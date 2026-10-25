; Full original byte-packed geometry, bullet-template and enemy records.
; Keep in agreement with shared/geometry.hpp, bullet/template.hpp and enemy.hpp.
; All declarations are type-only; they emit no DATA or BSS payload.
Point struc
    x dw ?
    y dw ?
Point ends
motion_t struc
    cur Point <?>
    prev Point <?>
    velocity Point <?>
motion_t ends
bullet_template_t struc
    spawn_type db ?
    patnum db ?
    BT_origin Point <?>
    BT_group db ?
    BT_special_motion db ?
    spread db ?
    spread_angle_delta db ?
    BT_stack db ?
    stack_speed_delta db ?
    BT_angle db ?
    speed db ?
bullet_template_t ends
enemy_t struc
    flag db ?
    age db ?
    pos motion_t <?>
    E_hp dw ?
    E_score dw ?
    E_script dw ?
    E_script_ip dw ?
    E_speed db ?
    E_patnum_base db ?
    E_cur_instr_frame db ?
    E_loop_i db ?
    E_angle db ?
    E_angle_delta db ?
    E_anim_cels db ?
    E_anim_frames_per_cel db ?
    E_anim_cur_cel db ?
    E_clip db ?
    E_item db ?
    E_damaged_this_frame db ?
    E_can_be_damaged db ?
    E_autofire db ?
    E_kills_player_on_collision db ?
    E_spawned_in_left_half db ?
    E_autofire_cur_frame db ?
    E_autofire_interval db ?
    E_bullet_template bullet_template_t <?>
    E_subtype db ?
    unused_1 db ?
    unused_2 dw ?
    unused_3 db ?
    unused_tail db 5 dup(?)
enemy_t ends
if size Point ne 4
    .err
endif
if size motion_t ne 12
    .err
endif
if size bullet_template_t ne 14
    .err
endif
if size enemy_t ne 64
    .err
endif

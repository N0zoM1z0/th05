; Shared real state/provider declarations. Bindings carry addresses only.
extrn _randring:byte, _randring_p:word, _playperf:byte
extrn _group_is_special:byte, _group_fixedspeed:byte
extrn _group_i_spread_angle:byte, _group_i:byte
extrn _group_i_absolute_angle:byte, _group_i_speed:byte
extrn _group_i_velocity:Point
extrn _bullet_template:bullet_template_t
extrn _bullet_zap:byte, _bullet_clear_time:byte
extrn _bullet_template_special_angle:bullet_special_angle_t
extrn _pellets:bullet_t, _bullets16:bullet_t
extrn _gather_template:gather_template_t
extrn @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC:near
extrn VECTOR2_NEAR:near

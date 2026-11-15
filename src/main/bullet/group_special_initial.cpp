// Set while a bullet group is spawned with special motion. The spawn group
// code (spawn_groups.asm) sets it to 1 around special-group dispatch, and
// the raw spawner (spawn_raw.asm) uses it to pick the special initialization.
// ReC98 th05_main.asm: `_group_is_special db 0`, followed by `evendata`.
#pragma option -zCBULLET_GROUP_SPECIAL_INIT_TEXT -zPmain_03

unsigned char group_is_special = 0;
typedef char bullet_group_special_flag_is_byte[(sizeof(group_is_special) == 1) ? 1 : -1];

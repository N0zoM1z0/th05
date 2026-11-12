// TH05's original per-group special-bullet selector, before the EVEN byte.
// ReC98 th05_main.asm: public _group_is_special; db 0; evendata.
#pragma option -zCBULLET_GROUP_SPECIAL_INIT_TEXT -zPmain_03

unsigned char group_is_special = 0;
typedef char bullet_group_special_flag_is_byte[(sizeof(group_is_special) == 1) ? 1 : -1];

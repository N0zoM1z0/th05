/* TH05's initial DOS-memory assignment budget, before each entry changes it. */
/* Original initialized word: th05/mem[data].asm, 320000 bytes / 16. */
#pragma option -zCMEM_ASSIGN_INIT_TEXT
#ifdef __cplusplus
#error This initial 16-bit DATA word uses the original C linkage
#endif

unsigned int mem_assign_paras = (320000UL >> 4);
typedef char mem_assign_init_is_word[(sizeof(mem_assign_paras) == 2) ? 1 : -1];

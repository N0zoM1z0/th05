// The zero byte at DS:1F6D, right after the dialog resource bank.
//
// Open question: this is defined as dialog_sequence_id, but the dialog code
// reads that variable at DS:1EE8, which is the bank's first field
// (DialogResourceBank::sequence_id, see resources.c and ReC98's
// th05_main.asm). DS:1F6D is most likely the bank's word-alignment padding.
#pragma option -zCDIALOG_SEQUENCE_INIT_TEXT -zPmain_01

signed char dialog_sequence_id = 0;
typedef char th05_dialog_sequence_has_byte_abi[(sizeof(dialog_sequence_id) == 1) ? 1 : -1];

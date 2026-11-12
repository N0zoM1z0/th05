// Original TH05 `_dialog_sequence_id db 0` at MAIN DS:1F6D.
// The signed byte tracks which Extra demo/dialog continuation is active.
#pragma option -zCDIALOG_SEQUENCE_INIT_TEXT -zPmain_01

signed char dialog_sequence_id = 0;
typedef char th05_dialog_sequence_has_byte_abi[(sizeof(dialog_sequence_id) == 1) ? 1 : -1];

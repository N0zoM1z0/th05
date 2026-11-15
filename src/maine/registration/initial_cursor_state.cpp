// The VRAM page that registration_frame() flips, and the edited name
// position. Both are initialized data in the original.
#pragma option -zCREG_CURSOR_INIT_TEXT -zPGROUP_01

unsigned char registration_page = 0;
int entered_name_cursor = 0;

// Registration page and name glyph cursor, in their original DGROUP order.
#pragma option -zCREG_CURSOR_INIT_TEXT -zPGROUP_01

unsigned char registration_page = 0;
int entered_name_cursor = 0;

typedef char reg_page_is_byte[(sizeof(registration_page) == 1) ? 1 : -1];
typedef char reg_cursor_is_word[(sizeof(entered_name_cursor) == 2) ? 1 : -1];

// Both mutable all-cast line counters start at zero in the source-level model.
// Their original historical TU/BSS split is not inferred from zero MZ bytes.
#pragma option -zCALLCAST_COUNTER_DATA_TEXT -zPgroup_01

int line_id_total = 0;
int line_id_on_screen = 0;

typedef char allcast_total_line_index_is_word[(sizeof(line_id_total) == 2) ? 1 : -1];
typedef char allcast_screen_line_index_is_word[(sizeof(line_id_on_screen) == 2) ? 1 : -1];

// All Cast line counters, as initialized data. In ReC98, [line_id_total] is
// defined in allcast.cpp and [line_id_on_screen] is only declared there; where
// ZUN actually defined them is unknown.
#pragma option -zCALLCAST_COUNTER_DATA_TEXT -zPgroup_01

int line_id_total = 0;
int line_id_on_screen = 0;

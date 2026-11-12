/* Distinct mutable All Cast PI backgrounds, including repeated filenames. */
#pragma option -zCALLCAST_BACKGROUND_FILES_TEXT -zPgroup_01
#ifdef __cplusplus
#error These natural filename initializers require a C compiler producer
#endif

/* Four background programs, seven named slides each. Each original screen
 * also has a terminal null pointer in its separate eight-entry index. */
char allcast_background_filenames[4][7][10] = {
    {
        "EXED01.pi", "EXED07.pi", "EXED08.pi", "EXED09.pi",
        "EXED10.pi", "EXED16.pi", "EXED15.pi"
    },
    {
        "EXED01.pi", "EXED11.pi", "EXED11.pi", "EXED11.pi",
        "EXED03.pi", "EXED16.pi", "EXED15.pi"
    },
    {
        "EXED01.pi", "EXED12.pi", "EXED12.pi", "EXED13.pi",
        "EXED04.pi", "EXED16.pi", "EXED15.pi"
    },
    {
        "EXED01.pi", "EXED14.pi", "EXED05.pi", "EXED14.pi",
        "EXED06.pi", "EXED16.pi", "EXED15.pi"
    }
};

typedef char allcast_bg_file_size[(sizeof(allcast_background_filenames) == 280) ? 1 : -1];
typedef char allcast_bg_program_size[(sizeof(allcast_background_filenames[0]) == 70) ? 1 : -1];
typedef char allcast_bg_filename_width[(sizeof(allcast_background_filenames[0][0]) == 10) ? 1 : -1];

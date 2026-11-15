/* All Cast background picture file names, per player character. Repeated
 * names are separate strings in the original, too. */
#pragma option -zCALLCAST_BACKGROUND_FILES_TEXT -zPgroup_01
#ifdef __cplusplus
#error This file is compiled as C
#endif

/* Seven screens per character. BG_FN in background_index.cpp points into
 * this table and adds an eighth null entry per character. */
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

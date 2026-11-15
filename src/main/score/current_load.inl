// Loads [hi] with the section for the current character and rank, and decodes
// it. Leaves [hi] unchanged if GENSOU.SCR can't be opened.
void near scoredat_load_for_cur(void)
{
    // DOS file open (read-only)
    _AX = 0x3D00;
    _DX = FP_OFF(main_score_filename);
    geninterrupt(0x21);
    if(_FLAGS & 0x01) {
        return;
    }
    _BX = _AX;
    seek_to_playchar_and_rank();

    // DOS file read
    _AH = 0x3F;
    _DX = FP_OFF(&hi);
    _CX = sizeof(hi);
    geninterrupt(0x21);

    // DOS file close
    _AH = 0x3E;
    geninterrupt(0x21);
    scoredat_decode();
}

void near scoredat_save_cur(void)
{
    scoredat_encode();
    _AX = 0x3D02;
    _DX = FP_OFF(main_score_filename);
    geninterrupt(0x21);
    _BX = _AX;
    seek_to_playchar_and_rank();

    _AH = 0x40;
    _DX = FP_OFF(&hi);
    _CX = sizeof(hi);
    geninterrupt(0x21);

    _AH = 0x3E;
    geninterrupt(0x21);
    scoredat_decode();
}

inline void seek_to_playchar_and_rank(void)
{
    _AH ^= _AH;
    _AL = playchar;
    _AX = (_AX * RANK_COUNT);
    _AL += rank;
    _DX = (_AX * sizeof(scoredat_section_t));
    _CX ^= _CX;
    _AX = 0x4200;
    geninterrupt(0x21);
}

void pascal near alphabet_cursor_put(int col, int row, int attr)
{
    register int col_r = col;
    register int row_r = row;
    gaiji_putca(
        ((col_r * 2) + 23), (row_r + 21),
        gALPHABET[(row_r * REGISTRATION_ALPHABET_COLS) + col_r], attr
    );
}

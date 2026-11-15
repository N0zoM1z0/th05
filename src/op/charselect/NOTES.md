# OP character selection

`menu.cpp` follows ReC98's `th05/m_char.cpp` with the darkening loop from
`th04/op/darken.cpp`. Its two `ZUN bloat` BSS bytes (`unused_1`, `unused_0`)
must stay; they keep the selection state at its original addresses
(DS `5138..5147`).

The unit's code ends at `D303`, three bytes past the paragraph frame `D300`
that the following shared segment uses. The link scaffold therefore puts one
alignment byte after the unit and starts the next context at `D304`, keeping
frame `0D30`. Moving or truncating the unit to fit `D300` does not work.

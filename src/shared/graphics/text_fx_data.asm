; Self-modifying text renderer DATA, reconstructed symbolically.
; Native CODE and the four raster-mask resources are separate owners.
.386
.model large
include symbols.inc

_DATA segment word public 'DATA' use16
public _grppsafx_func_offsets_1, _grppsafx_func_offsets_2, _grppsafx_mask_ptrs
_grppsafx_func_offsets_1 label word
    dw glyph_weight_normal - (grppsafx_glyph_func_1 + 2)
    dw glyph_weight_heavy - (grppsafx_glyph_func_1 + 2)
    dw glyph_weight_bold - (grppsafx_glyph_func_1 + 2)
    dw glyph_weight_black - (grppsafx_glyph_func_1 + 2)
    dw glyph_weight_bold_and_mask - (grppsafx_glyph_func_1 + 2)
_grppsafx_func_offsets_2 label word
    dw glyph_weight_normal - (grppsafx_glyph_func_2 + 2)
    dw glyph_weight_heavy - (grppsafx_glyph_func_2 + 2)
    dw glyph_weight_bold - (grppsafx_glyph_func_2 + 2)
    dw glyph_weight_black - (grppsafx_glyph_func_2 + 2)
    dw glyph_weight_bold_and_mask - (grppsafx_glyph_func_2 + 2)
_grppsafx_mask_ptrs label word
    dw _grppsafx_mask_1, _grppsafx_mask_2, _grppsafx_mask_3, _grppsafx_mask_4
_DATA ends

TEXT_FX_STATE_DATA segment word public 'DATA' use16
public _graph_putsa_fx_func, _graph_putsa_fx_spacing
FX_WEIGHT_BOLD equ 2
_graph_putsa_fx_func dw FX_WEIGHT_BOLD
_graph_putsa_fx_spacing dw 16
TEXT_FX_STATE_DATA ends
end

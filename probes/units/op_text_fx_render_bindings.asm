; Foreign ranges reserve placement only; no initialized target payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
TEXT_FX_RENDER_CONTEXT segment byte public 'CODE' use16
org (0d300h - 0a390h)
TEXT_FX_RENDER_CONTEXT ends
op_01 group TEXT_FX_RENDER_CONTEXT
SHARED segment para public 'CODE' use16
org (0d436h - 0d300h)
SHARED ends
TEXT_FX_RENDER_FOREIGN_TAIL segment byte public 'CODE' use16
org (00efe0h - 0d590h)
TEXT_FX_RENDER_FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
org 009deh
public _graph_putsa_fx_func, _graph_putsa_fx_spacing
_graph_putsa_fx_func label word
org 009e0h
_graph_putsa_fx_spacing label word
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

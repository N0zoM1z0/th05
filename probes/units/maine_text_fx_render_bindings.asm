; Foreign ranges reserve placement only; no initialized target payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
TEXT_FX_RENDER_CONTEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
TEXT_FX_RENDER_CONTEXT ends
group_01 group TEXT_FX_RENDER_CONTEXT
SHARED segment para public 'CODE' use16
org (0e91ah - 0e800h)
SHARED ends
TEXT_FX_RENDER_FOREIGN_TAIL segment byte public 'CODE' use16
org (010110h - 0ea74h)
TEXT_FX_RENDER_FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
org 006bch
public _graph_putsa_fx_func, _graph_putsa_fx_spacing
_graph_putsa_fx_func label word
org 006beh
_graph_putsa_fx_spacing label word
org 006c0h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

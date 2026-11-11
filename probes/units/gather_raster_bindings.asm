; Original main_03 CS1527 / DGROUP209D positions, no source bytes in binder.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
GATHER_RASTER_PRE_FRAME segment para public 'CODE' use16
org (015270h - 0AE10h)
GATHER_RASTER_PRE_FRAME ends
GATHER_RASTER_PREFIX segment byte public 'CODE' use16
org (015312h - 015270h)
GATHER_RASTER_PREFIX ends
GATHER_RASTER_TEXT segment byte public 'CODE' use16
GATHER_RASTER_TEXT ends
GATHER_RASTER_TAIL segment byte public 'CODE' use16
org (0209D0h - 01538Ch)
GATHER_RASTER_TAIL ends
main_03 group GATHER_RASTER_PREFIX, GATHER_RASTER_TEXT, GATHER_RASTER_TAIL
_DATA segment word public 'DATA' use16
public _sPELLET
org 00E4Ah
_sPELLET label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

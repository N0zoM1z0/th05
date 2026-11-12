; Original MAIN code groups and DATA prefix, no hardware address payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_VRAM_PLANES_TEXT segment byte public 'CODE' use16
org 09ca0h
MAIN_VRAM_PLANES_TEXT ends
main_01 group MAIN_VRAM_PLANES_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
VRAM_PLANES_MAIN03 segment byte public 'CODE' use16
org 0b760h
VRAM_PLANES_MAIN03 ends
main_03 group VRAM_PLANES_MAIN03
_DATA segment word public 'DATA' use16
org 00838h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

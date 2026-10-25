; Outside-only original decoded-MAINE frames; source owns all51 keyboard bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
REG_ALPHA_DATA_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
REG_ALPHA_DATA_TEXT ends
GROUP_01 group REG_ALPHA_DATA_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 014eeh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

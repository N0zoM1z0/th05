; Foreign-only addresses for the complete TH05 alphabet cursor helper.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTCA
org 0121ah
GAIJI_PUTCA label far
org 0a540h
_TEXT ends
REG_ALPHA_PREFIX segment byte public 'CODE' use16
org (0bcedh - 0a540h)
REG_ALPHA_PREFIX ends
REG_ALPHA_TEXT segment byte public 'CODE' use16
REG_ALPHA_TEXT ends
REG_ALPHA_TAIL segment byte public 'CODE' use16
org (10110h - 0bd1eh)
REG_ALPHA_TAIL ends
GROUP_01 group REG_ALPHA_PREFIX, REG_ALPHA_TEXT, REG_ALPHA_TAIL
_DATA segment word public 'DATA' use16
public _gALPHABET
org 014eeh
_gALPHABET label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

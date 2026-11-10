; Actual empty CODE frames and DATA prefix; all six strings are compiler-owned.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
ZUNSOFT_DATA_TEXT segment byte public 'CODE' use16
ZUNSOFT_DATA_TEXT ends
ZUNSOFT_DATA_TAIL segment byte public 'CODE' use16
org (0d300h - 0a390h)
ZUNSOFT_DATA_TAIL ends
op_01 group ZUNSOFT_DATA_TEXT, ZUNSOFT_DATA_TAIL
SHARED segment para public 'CODE' use16
org (0efe0h - 0d300h)
SHARED ends
_DATA segment word public 'DATA' use16
org 0eeah
_DATA ends
; Foreign initialized DATA continues beyond the six compiler-owned strings.
; Preserve the accepted Music Room DATA endpoint (DS:2817) as outside context,
; rather than inventing a stack or adding bytes to this DATA contribution.
ZUNSOFT_FILENAMES_FOREIGN_DATA_TAIL segment word public 'DATA' use16
org (02817h - 00f20h)
ZUNSOFT_FILENAMES_FOREIGN_DATA_TAIL ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, ZUNSOFT_FILENAMES_FOREIGN_DATA_TAIL, _BSS
end

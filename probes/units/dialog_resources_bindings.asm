; Place only the complete compiler-owned resource bank at its original DS slot.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
DIALOG_RESOURCE_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
DIALOG_RESOURCE_MAIN01_GAP ends
DIALOG_RESOURCE_SHARED_GAP segment byte public 'CODE' use16
org (209d0h - 14ab0h)
DIALOG_RESOURCE_SHARED_GAP ends
_DATA segment word public 'DATA' use16
org 01ee8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

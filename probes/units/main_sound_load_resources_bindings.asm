; Original MAIN DGROUP prefix; the entire sound resource bank is C-owned.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SOUND_RESOURCE_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
SOUND_RESOURCE_MAIN01_GAP ends
SOUND_RESOURCE_SHARED_GAP segment byte public 'CODE' use16
org (209d0h - 14ab0h)
SOUND_RESOURCE_SHARED_GAP ends
_DATA segment word public 'DATA' use16
org 0826h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

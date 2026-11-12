; The original All Cast filename bank is a genuine *foreign* DATA public.
; No pointer payload or filename data is supplied within the accepted scope.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
ALLCAST_BG_INDEX_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
ALLCAST_BG_INDEX_TEXT ends
group_01 group ALLCAST_BG_INDEX_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 00760h
_DATA ends
ALLCAST_BG_FILE_CONTEXT segment byte public 'DATA' use16
public _allcast_background_filenames
org 00ceh
_allcast_background_filenames label byte
ALLCAST_BG_FILE_CONTEXT ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, ALLCAST_BG_FILE_CONTEXT, _BSS
end

; Original MAINE code and outside-only DATA prefix; no string payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
ALLCAST_SONG_NAME_TEXT segment byte public 'CODE' use16
org (0e800h - 0a540h)
ALLCAST_SONG_NAME_TEXT ends
group_01 group ALLCAST_SONG_NAME_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 014e9h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

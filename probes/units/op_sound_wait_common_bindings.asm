; Genuine ungrouped SHARED common-segment context; foreign symbols only.
.386
ifdef BINDINGS_AFTER
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public @FRAME_DELAY$QI
org (0e15eh - 0e113h)
@FRAME_DELAY$QI label far
SHARED ends
else
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0e0ceh - 0d300h)
SHARED ends
SOUND_WAIT_DATA_GAP segment byte public 'CODE' use16
org (0efe0h - 0e15eh)
SOUND_WAIT_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 0a62h
_snd_bgm_mode label byte
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
endif
end

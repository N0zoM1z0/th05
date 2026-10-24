; Real TH05 MAIN sound-effect context; no instructions, stack or values.
.386
.model large
SHARED_BASE equ 14ab0h
UNIT_START equ 14ce2h
UNIT_END equ 14d68h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_SOUND
org 03c44h
BGM_SOUND label far
org 0ae10h
_TEXT ends
SE_SHARED_PREFIX_GAP segment byte public 'CODE' use16
org (SHARED_BASE - 0ae10h)
SE_SHARED_PREFIX_GAP ends
SHARED segment byte public 'CODE' use16
assume cs:SHARED
org (UNIT_START - SHARED_BASE)
SHARED ends
; A true outside-function paragraph context keeps DS fixed for either
; natural133-byte CODE or original134-byte extent, without adding CODE bytes.
SE_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 14d70h)
SE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_priorities, _snd_se_priority_frames, _snd_se_playing, _snd_se_frame, _snd_se_mode
org 00800h
_snd_se_priorities label byte
org 00811h
_snd_se_priority_frames label byte
org 00822h
_snd_se_playing label byte
org 00823h
_snd_se_frame label byte
org 00835h
_snd_se_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real TH05 MAINE sound-effect context; no instructions, stack or values.
.386
.model large
SHARED_BASE equ 0e800h
UNIT_START equ 0eae6h
UNIT_END equ 0eb6ch
DGROUP_BASE equ 10110h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_SOUND
org 0344ch
BGM_SOUND label far
org SHARED_BASE
_TEXT ends
SHARED segment byte public 'CODE' use16
assume cs:SHARED
org (UNIT_START - SHARED_BASE)
SHARED ends
; A true outside-function paragraph context keeps DS fixed for either
; natural133-byte CODE or original134-byte extent, without adding CODE bytes.
SE_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 0eb70h)
SE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_priorities, _snd_se_priority_frames, _snd_se_playing, _snd_se_frame, _snd_se_mode
org 0065eh
_snd_se_priorities label byte
org 0066fh
_snd_se_priority_frames label byte
org 006c0h
_snd_se_playing label byte
org 006c1h
_snd_se_frame label byte
org 006dbh
_snd_se_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

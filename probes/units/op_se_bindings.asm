; Real TH05 OP sound-effect context; no instructions, stack or values.
.386
.model large
SHARED_BASE equ 0d300h
UNIT_START equ 0d602h
UNIT_END equ 0d688h
DGROUP_BASE equ 0efe0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_SOUND
org 03284h
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
org (DGROUP_BASE - 0d690h)
SE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_priorities, _snd_se_priority_frames, _snd_se_playing, _snd_se_frame, _snd_se_mode
org 00980h
_snd_se_priorities label byte
org 00991h
_snd_se_priority_frames label byte
org 009e2h
_snd_se_playing label byte
org 009e3h
_snd_se_frame label byte
org 00a61h
_snd_se_mode label byte
; Retain the independently accepted foreign Music Room DATA end only.
; This is an ORG extent with no copied values or authored-byte claim.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

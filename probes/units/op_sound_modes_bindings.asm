; Original decoded OP driver context; no payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
public _snd_pmd_resident
org 00022h
_snd_pmd_resident label far
public _snd_mmd_resident
org 00050h
_snd_mmd_resident label far
org 00080h
SHARED ends
SOUND_DATA_GAP segment byte public 'CODE' use16
org 01bc4h
SOUND_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_mode
org 00a61h
_snd_se_mode label byte
public _snd_bgm_mode
org 00a62h
_snd_bgm_mode label byte
public _snd_midi_possible
org 00a63h
_snd_midi_possible label byte
; Real external OP music DATA ends at DS:2817. Retain that known foreign
; extent so TLINK's no-STACK candidate has a valid minimum allocation.
; No byte values or authored DATA are supplied by this context.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

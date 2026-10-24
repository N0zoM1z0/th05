; Original decoded MAINE driver context; no payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
public _snd_pmd_resident
org 00020h
_snd_pmd_resident label far
public _snd_mmd_resident
org 0004eh
_snd_mmd_resident label far
org 0007eh
SHARED ends
SOUND_DATA_GAP segment byte public 'CODE' use16
org 017f6h
SOUND_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_mode
org 006dbh
_snd_se_mode label byte
public _snd_bgm_mode
org 006dch
_snd_bgm_mode label byte
public _snd_midi_possible
org 006ddh
_snd_midi_possible label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Actual installed-driver probes are foreign APIs; no bodies or state.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SOUND_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
SOUND_MAIN01_CONTEXT ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
public _snd_pmd_resident
org 0c6h
_snd_pmd_resident label far
public _snd_mmd_resident
org 0f4h
_snd_mmd_resident label far
org 0124h
SHARED ends
SOUND_SHARED_TAIL segment byte public 'CODE' use16
org 0600h
SOUND_SHARED_TAIL ends
SOUND_MAIN03_CONTEXT segment byte public 'CODE' use16
org 0b760h
SOUND_MAIN03_CONTEXT ends
_DATA segment word public 'DATA' use16
public _snd_se_mode
org 0835h
_snd_se_mode label byte
public _snd_bgm_mode
org 0836h
_snd_bgm_mode label byte
public _snd_midi_possible
org 0837h
_snd_midi_possible label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

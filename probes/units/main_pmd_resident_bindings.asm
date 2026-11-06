; Genuine MAIN SHARED and DGROUP context for the complete PMD detector.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
PMD_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
PMD_MAIN01_GAP ends
SHARED segment para public 'CODE' use16
org (14b76h - 14ab0h)
SHARED ends
PMD_DGROUP_GAP segment para public 'CODE' use16
org (209d0h - 14bb0h)
PMD_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_se_mode, _snd_bgm_mode, _snd_midi_possible, _snd_interrupt_if_midi
org 0835h
_snd_se_mode label byte
org 0836h
_snd_bgm_mode label byte
org 0837h
_snd_midi_possible label byte
org 02f8eh
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

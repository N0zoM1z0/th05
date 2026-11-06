; Genuine MAIN SHARED and DGROUP context for the complete MMD detector.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MMD_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
MMD_MAIN01_GAP ends
SHARED segment para public 'CODE' use16
org (14ba4h - 14ab0h)
SHARED ends
MMD_DGROUP_GAP segment byte public 'CODE' use16
org (209d0h - 14bd3h)
MMD_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_midi_possible, _snd_interrupt_if_midi
org 0837h
_snd_midi_possible label byte
org 02f8eh
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

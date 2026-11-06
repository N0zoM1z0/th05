; Original OP shared function and sound-selection bytes; foreign context only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org (0d350h - 0d300h)
SHARED ends
MMD_DGROUP_GAP segment byte public 'CODE' use16
org (0efe0h - 0d37fh)
MMD_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_midi_possible, _snd_interrupt_if_midi
org 0a63h
_snd_midi_possible label byte
org 03762h
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

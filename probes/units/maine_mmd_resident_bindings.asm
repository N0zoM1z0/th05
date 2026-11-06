; Original MAINE shared function and sound-selection bytes; foreign context only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
org (0e84eh - 0e800h)
SHARED ends
MMD_DGROUP_GAP segment byte public 'CODE' use16
org (010110h - 0e87dh)
MMD_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _snd_midi_possible, _snd_interrupt_if_midi
org 06ddh
_snd_midi_possible label byte
org 026deh
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

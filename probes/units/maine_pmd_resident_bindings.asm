; Real MAINE PMD detector at SHARED E820..E84E, foreign suffix only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
org (0e820h - 0e800h)
SHARED ends
MAINE_PMD_FOREIGN_TAIL segment byte public 'CODE' use16
org (010110h - 0e84eh)
MAINE_PMD_FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _snd_se_mode, _snd_bgm_mode, _snd_midi_possible, _snd_interrupt_if_midi
org 06dbh
_snd_se_mode label byte
org 06dch
_snd_bgm_mode label byte
org 06ddh
_snd_midi_possible label byte
org 026deh
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

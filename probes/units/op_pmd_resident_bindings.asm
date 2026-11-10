; Real OP PMD detector at SHARED D322..D350, with foreign suffix only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org (0d322h - 0d300h)
SHARED ends
OP_PMD_FOREIGN_TAIL segment byte public 'CODE' use16
org (0efe0h - 0d350h)
OP_PMD_FOREIGN_TAIL ends
_DATA segment word public 'DATA' use16
public _snd_se_mode, _snd_bgm_mode, _snd_midi_possible, _snd_interrupt_if_midi
org 0a61h
_snd_se_mode label byte
org 0a62h
_snd_bgm_mode label byte
org 0a63h
_snd_midi_possible label byte
org 03762h
_snd_interrupt_if_midi label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

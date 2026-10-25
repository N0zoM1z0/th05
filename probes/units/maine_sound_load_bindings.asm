; Actual foreign code/data frames and typed addresses only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_READ_SDATA
org 0301ah
BGM_READ_SDATA label far
public BGM_INIT
org 03556h
BGM_INIT label far
public BGM_FINISH
org 036fah
BGM_FINISH label far
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 042c0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 00566h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public SND_KAJA_INTERRUPT
SND_KAJA_INTERRUPT label far
org 012f2h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _SND_LOAD_EXT
org 006cch
_SND_LOAD_EXT label byte
public _snd_se_mode
org 006dbh
_snd_se_mode label byte
public _snd_bgm_mode
org 006dch
_snd_bgm_mode label byte
public _snd_load_fn
org 027a6h
_snd_load_fn label byte
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

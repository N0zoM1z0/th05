; Actual foreign code/data frames and typed addresses only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_READ_SDATA
org 02e52h
BGM_READ_SDATA label far
public BGM_INIT
org 0338eh
BGM_INIT label far
public BGM_FINISH
org 03532h
BGM_FINISH label far
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 02f70h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 008beh
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public SND_KAJA_INTERRUPT
SND_KAJA_INTERRUPT label far
org 0136ah
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _SND_LOAD_EXT
org 00a52h
_SND_LOAD_EXT label byte
public _snd_se_mode
org 00a61h
_snd_se_mode label byte
public _snd_bgm_mode
org 00a62h
_snd_bgm_mode label byte
public _snd_load_fn
org 0383eh
_snd_load_fn label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

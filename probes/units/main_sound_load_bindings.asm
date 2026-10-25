; Actual foreign code/data frames and typed addresses only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public BGM_READ_SDATA
org 03812h
BGM_READ_SDATA label far
public BGM_INIT
org 03d4eh
BGM_INIT label far
public BGM_FINISH
org 03ef2h
BGM_FINISH label far
org 0ae10h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org 09ca0h
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 003f4h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public SND_KAJA_INTERRUPT
SND_KAJA_INTERRUPT label far
org 0ba74h
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _SND_LOAD_EXT
org 00826h
_SND_LOAD_EXT label byte
public _snd_se_mode
org 00835h
_snd_se_mode label byte
public _snd_bgm_mode
org 00836h
_snd_bgm_mode label byte
public _snd_load_fn
org 03056h
_snd_load_fn label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

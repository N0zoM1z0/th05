; Original MAINE earlier measure and later VSync wait addresses only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
org 00a42h
SHARED ends
SHARED_WAIT_TAIL segment byte public 'CODE' use16
assume cs:SHARED_WAIT_TAIL
public @FRAME_DELAY$QI
org 00001h
@FRAME_DELAY$QI label far
SHARED_WAIT_TAIL ends
shared_wait group SHARED, SHARED_WAIT_TAIL
WAIT_DATA_GAP segment byte public 'CODE' use16
org 00e88h
WAIT_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _snd_bgm_mode
org 006dch
_snd_bgm_mode label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

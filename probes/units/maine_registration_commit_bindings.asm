; Real foreign frame/sound/angle providers; no helper bodies or game state.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IATAN2
org 01a8ch
IATAN2 label far
org 0a540h
_TEXT ends
REG_FRAME_TEXT segment byte public 'CODE' use16
assume cs:REG_FRAME_TEXT
public @registration_frame$qv
org (0bd1eh - 0a540h)
@registration_frame$qv label near
org (0c16ch - 0a540h)
REG_FRAME_TEXT ends
REG_COMMIT_TEXT segment byte public 'CODE' use16
REG_COMMIT_TEXT ends
REG_COMMIT_TAIL segment byte public 'CODE' use16
org (0e800h - 0c1ddh)
REG_COMMIT_TAIL ends
GROUP_01 group REG_FRAME_TEXT, REG_COMMIT_TEXT, REG_COMMIT_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 02e6h
SND_SE_PLAY label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _glyphballs
org 04f7ah
_glyphballs label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

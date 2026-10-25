; Foreign-only pool/alphabet and real frame/RNG providers; no owned code/data.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public IRAND
org 01df8h
IRAND label far
org 0a540h
_TEXT ends
REG_FRAME_TEXT segment byte public 'CODE' use16
assume cs:REG_FRAME_TEXT
public @registration_frame$qv
org (0bd1eh - 0a540h)
@registration_frame$qv label near
org (0bd46h - 0a540h)
REG_FRAME_TEXT ends
REG_SPAWN_TEXT segment byte public 'CODE' use16
REG_SPAWN_TEXT ends
REG_SPAWN_TAIL segment byte public 'CODE' use16
org (10110h - 0be76h)
REG_SPAWN_TAIL ends
GROUP_01 group REG_FRAME_TEXT, REG_SPAWN_TEXT, REG_SPAWN_TAIL
_DATA segment word public 'DATA' use16
public _gALPHABET
org 014eeh
_gALPHABET label byte
public _glyphballs
org 04f7ah
_glyphballs label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

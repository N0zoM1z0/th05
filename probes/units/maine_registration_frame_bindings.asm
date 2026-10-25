; Outside-only original providers/state; no executable helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a540h
_TEXT ends
REG_FRAME_PREFIX segment byte public 'CODE' use16
org (0bd1eh - 0a540h)
REG_FRAME_PREFIX ends
REG_FRAME_TEXT segment byte public 'CODE' use16
REG_FRAME_TEXT ends
REG_GLYPH_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:REG_GLYPH_UPDATE_TEXT
public @glyphballs_update$qv
org (0be76h - 0bd46h)
@glyphballs_update$qv label near
org (0e800h - 0bd46h)
REG_GLYPH_UPDATE_TEXT ends
GROUP_01 group REG_FRAME_PREFIX, REG_FRAME_TEXT, REG_GLYPH_UPDATE_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public _snd_se_update, @FRAME_DELAY$QI
org 0320h
_snd_se_update label far
org 0a88h
@FRAME_DELAY$QI label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _registration_page
org 01521h
_registration_page label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

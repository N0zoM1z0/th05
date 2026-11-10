; Full OP source-free keyboard/joystick original SHARED context.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public JS_SENSE
org 02cbah
JS_SENSE label far
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org (00d300h - 00a390h)
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
org (00df8eh - 00d300h)
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org (00efe0h - 00e094h)
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _key_det, _shiftkey, js_stat, js_bexist
org 00544h
js_bexist label word
org 02e1ah
js_stat label word
org 03a92h
_key_det label word
org 03a94h
_shiftkey label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

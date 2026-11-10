; Full MAINE source-free keyboard/joystick original SHARED context.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public JS_SENSE
org 02e82h
JS_SENSE label far
org 0a540h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org (00e800h - 00a540h)
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
assume cs:SHARED
org (00f102h - 00e800h)
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
org (010110h - 00f208h)
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _key_det, _shiftkey, js_stat, js_bexist
org 0022eh
js_bexist label word
org 01d96h
js_stat label word
org 029fah
_key_det label word
org 029fch
_shiftkey label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

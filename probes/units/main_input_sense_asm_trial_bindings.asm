; Strict source-free native MAIN SHARED input 262-byte physical context.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public JS_SENSE
org 0367ah
JS_SENSE label far
org 0ae10h
_TEXT ends
MAIN01_FOREIGN segment byte public 'CODE' use16
org (014ab0h - 0ae10h)
MAIN01_FOREIGN ends
main_01 group MAIN01_FOREIGN
SHARED segment para public 'CODE' use16
assume cs:SHARED
org (014fc2h - 014ab0h)
SHARED ends
SHARED_TAIL segment byte public 'CODE' use16
org (015270h - 0150c8h)
SHARED_TAIL ends
MAIN03_FOREIGN segment byte public 'CODE' use16
org (0209d0h - 015270h)
MAIN03_FOREIGN ends
main_03 group MAIN03_FOREIGN
_DATA segment word public 'DATA' use16
public _key_det, _shiftkey, js_stat, js_bexist
org 003d0h
js_bexist label word
org 02646h
js_stat label word
org 03064h
_key_det label word
org 03066h
_shiftkey label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

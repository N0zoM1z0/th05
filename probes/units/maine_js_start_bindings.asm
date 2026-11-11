; MAINE original joystick/sound CODE anchor. All extern routines and original
; DATA/BSS are symbol-only; this binder emits no initialized CODE or DATA.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public SOUND_O, SOUND_I
org 0226eh
SOUND_O label near
org 02284h
SOUND_I label near
org 02e46h
_TEXT ends

; The original real CODE contribution covers 02E46..02E82, and MAINE's
; original 16-byte link-frame shift places DGROUP at 10110.
FOREIGN_MAINE_CODE segment byte public 'CODE' use16
org (010110h - 02e82h)
FOREIGN_MAINE_CODE ends

_DATA segment word public 'DATA' use16
public js_bexist
org 022eh
js_bexist label word
; Original MAINE initialized DATA ends at DGROUP:1D4A.
org 01d4ah
_DATA ends
_BSS segment word public 'BSS' use16
; Exact original native BSS length from the pinned calibration MAP.
org 0a800h
_BSS ends
DGROUP group _DATA, _BSS
end

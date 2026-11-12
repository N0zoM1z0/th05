; Only original main_03 near CODE publics, with no game instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
DISPATCH_MAIN01 segment byte public 'CODE' use16
org 09ca0h
DISPATCH_MAIN01 ends
main_01 group DISPATCH_MAIN01
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B6_UPDATE_TEXT
public _bullets_add_regular
org 01f94h
_bullets_add_regular label near
public _bullets_add_special
org 01fa8h
_bullets_add_special label near
public _bullets_add_regular_fixedspeed
org 01fc6h
_bullets_add_regular_fixedspeed label near
org 0b760h
B6_UPDATE_TEXT ends
BULLET_DISPATCH_DATA_TEXT segment byte public 'CODE' use16
BULLET_DISPATCH_DATA_TEXT ends
main_03 group B6_UPDATE_TEXT,BULLET_DISPATCH_DATA_TEXT
_DATA segment word public 'DATA' use16
org 00f4ch
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

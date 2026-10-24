; Symbol-only TH05 MAIN Extra-stage midboss context, no executable bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_TEXT segment byte public 'CODE' use16
MAI_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
MX_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
MX_MAIN01_SPACE ends
main_01 group MAI_TEXT, GENERIC_BOSS_MAIN01_TEXT, MX_MAIN01_SPACE
MX_SHARED segment para public 'CODE' use16
assume cs:MX_SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
MX_SHARED ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
MIDBOSSX_TEXT segment byte public 'CODE' use16
assume cs:MIDBOSSX_TEXT
public @PlayfieldMotion@update_seg3$qv, VECTOR2_NEAR
public @RANDRING2_NEXT16_AND$QUI
org (1527ch - 15270h)
@PlayfieldMotion@update_seg3$qv label near
org (152aah - 15270h)
@RANDRING2_NEXT16_AND$QUI label near
org (152dah - 15270h)
VECTOR2_NEAR label near
org (163feh - 15270h)
MIDBOSSX_TEXT ends
; Follows the complete five-function prefix at original165B6.
MX_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:MX_MAIN03_TAIL
public _bullets_add_regular, _bullets_add_special
org (01f94h - 01346h)
_bullets_add_regular label near
org (01fa8h - 01346h)
_bullets_add_special label near
org (0b760h - 01346h)
MX_MAIN03_TAIL ends
main_03 group BOSS_TEXT, MIDBOSSX_TEXT, MX_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _midbossx_pattern, _bullet_special, _bullet_template_special_angle
public _page_back, _bullet_template, _midboss, _boss_statebyte
org 147ah
_midbossx_pattern label byte
org 3f94h
_bullet_special label byte
org 3f95h
_bullet_template_special_angle label byte
org 4ad6h
_page_back label byte
org 577eh
_bullet_template label byte
org 5aa4h
_midboss label byte
org 0c682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

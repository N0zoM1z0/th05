; Symbol-only original foreign context. No implementations or state values.
.386
.model large
.stack 80h
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAI_YUKI_FRAME_GAP segment byte public 'CODE' use16
org 0a460h
MAI_YUKI_FRAME_GAP ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @randring2_next16$qv, @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI, VECTOR2_NEAR
org 02ch
@randring2_next16$qv label near
org 03ah
@RANDRING2_NEXT16_AND$QUI label near
org 050h
@RANDRING2_NEXT16_MOD$QUI label near
org 06ah
VECTOR2_NEAR label near
org 025efh
B4_UPDATE_TEXT ends
main_03 group B4_UPDATE_TEXT
MAI_YUKI_DS_GAP segment byte public 'CODE' use16
org 09079h
MAI_YUKI_DS_GAP ends
_DATA segment word public 'DATA' use16
public _boss, _boss2, _mai_flystep_random_next_y_direct, _yuki_flystep_random_next_y_direc
org 0442ch
_mai_flystep_random_next_y_direct label byte
org 0442dh
_yuki_flystep_random_next_y_direc label byte
org 05abah
_boss label byte
org 05ad2h
_boss2 label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

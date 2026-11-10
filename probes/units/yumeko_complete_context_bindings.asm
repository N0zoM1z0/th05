; Genuine adjacent Yumeko near-code context with full independent MAIN01
; sword renderer and MAIN03 allocator, updater, and seven attack callbacks.
; Only foreign labels/physical outside spans, never a candidate function body.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
GENERIC_BOSS_MAIN01_TEXT segment byte public 'CODE' use16
GENERIC_BOSS_MAIN01_TEXT ends
BULLET_RENDER_TEXT segment byte public 'CODE' use16
assume cs:BULLET_RENDER_TEXT
public Z_SUPER_ROLL_PUT_TINY_32X32_RAW, SELECT_FOR_RANK
public SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
org (0BF62h - 0AE10h)
Z_SUPER_ROLL_PUT_TINY_32X32_RAW label near
org (0CFB2h - 0AE10h)
SELECT_FOR_RANK label far
org (0DF28h - 0AE10h)
SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1 label near
org (0E2D6h - 0AE10h)
BULLET_RENDER_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:CIRCLE_TEXT
public @CIRCLES_ADD_SHRINKING$QII
@CIRCLES_ADD_SHRINKING$QII label far
org (0143E0h - 0E2D6h)
CIRCLE_TEXT ends
YUMEKO_UPDATE_MAIN01_TEXT segment byte public 'CODE' use16
YUMEKO_UPDATE_MAIN01_TEXT ends
YUMEKO_AFTER_RENDER_CONTEXT segment byte public 'CODE' use16
org (014AB0h - 014422h)
YUMEKO_AFTER_RENDER_CONTEXT ends
main_01 group GENERIC_BOSS_MAIN01_TEXT, BULLET_RENDER_TEXT, CIRCLE_TEXT, YUMEKO_UPDATE_MAIN01_TEXT, YUMEKO_AFTER_RENDER_CONTEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public VECTOR2, SND_SE_PLAY, VECTOR2_AT
org 0008h
VECTOR2 label far
org 0232h
SND_SE_PLAY label far
org 03B0h
VECTOR2_AT label far
org 07C0h
SHARED ends
LASER_SC_TEXT segment byte public 'CODE' use16
LASER_SC_TEXT ends
BOSS_TEXT segment byte public 'CODE' use16
BOSS_TEXT ends
B5_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B5_UPDATE_TEXT
public @PlayfieldMotion@update_seg3$qv, @randring2_next16$qv
public @RANDRING2_NEXT16_AND$QUI, @RANDRING2_NEXT16_MOD$QUI
public VECTOR2_NEAR, @lasers_shootout_add$qv
public @BULLET_PATNUM_FOR_ANGLE$QUIUC, @GATHER_ADD_ONLY_3STACK$QIUIUI
public @PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC
public @playperf_speedtune, _bullets_add_regular, _bullets_add_special
public @BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T
org 000Ch
@PlayfieldMotion@update_seg3$qv label near
org 002Ch
@randring2_next16$qv label near
org 003Ah
@RANDRING2_NEXT16_AND$QUI label near
org 0050h
@RANDRING2_NEXT16_MOD$QUI label near
org 006Ah
VECTOR2_NEAR label near
org (01A66Eh - 015270h)
@lasers_shootout_add$qv label near
org (016F52h - 015270h)
@BULLET_PATNUM_FOR_ANGLE$QUIUC label near
org (01705Dh - 015270h)
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (0171CCh - 015270h)
@PLAYER_ANGLE_FROM$Q20%SUBPIXELBASE$TI$TI%T1UC label near
org (0171EAh - 015270h)
@playperf_speedtune label near
org (017204h - 015270h)
_bullets_add_regular label near
org (017218h - 015270h)
_bullets_add_special label near
org (0176DDh - 015270h)
@BOSS_EXPLODE_SMALL$Q16EXPLOSION_TYPE_T label near
org (01ED41h - 015270h)
B5_UPDATE_TEXT ends
YUMEKO_AFTER_ATTACKS_TAIL segment para public 'CODE' use16
org (0209D0h - 01F5A0h)
YUMEKO_AFTER_ATTACKS_TAIL ends
main_03 group LASER_SC_TEXT, BOSS_TEXT, B5_UPDATE_TEXT, YUMEKO_AFTER_ATTACKS_TAIL
_DATA segment word public 'DATA' use16
public _circles_color, _custom_entities, _player_pos, _player_is_hit
public _bullet_clear_time, _bullet_template_tune, _bullet_template
public _boss, _boss_statebyte, _laser_template
org 036D2h
_player_pos label byte
org 036F3h
_player_is_hit label byte
org 03F97h
_bullet_clear_time label byte
org 041DAh
_circles_color label byte
org 041DEh
_bullet_template_tune label byte
org 0577Eh
_bullet_template label byte
org 05A8Ch
_laser_template label byte
org 05ABAh
_boss label byte
org 0B3F4h
_custom_entities label byte
org 0C682h
_boss_statebyte label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

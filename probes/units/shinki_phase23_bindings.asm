; Foreign-only context for the genuine complete private phase helper.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_0_TEXT segment byte public 'CODE' use16
org 09ca0h
MAIN_0_TEXT ends
BOSS_BG_TEXT segment byte public 'CODE' use16
BOSS_BG_TEXT ends
main_01 group MAIN_0_TEXT, BOSS_BG_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_SE_PLAY
org 0232h
SND_SE_PLAY label far
org 07c0h
SHARED ends
BULLET_A_TEXT segment byte public 'CODE' use16
BULLET_A_TEXT ends
LASER_SC_TEXT segment byte public 'CODE' use16
assume cs:LASER_SC_TEXT
public @GATHER_ADD_ONLY_3STACK$QIUIUI
org 01dedh
@GATHER_ADD_ONLY_3STACK$QIUIUI label near
org (1acbah - 15270h)
LASER_SC_TEXT ends
B6_BALLS_TEXT segment byte public 'CODE' use16
B6_BALLS_TEXT ends
B6_PATTERN_A_TEXT segment byte public 'CODE' use16
B6_PATTERN_A_TEXT ends
B6_UPDATE_TEXT segment byte public 'CODE' use16
B6_UPDATE_TEXT ends
PHASE23_MAIN03_TAIL segment byte public 'CODE' use16
org (209d0h - 1ad20h)
PHASE23_MAIN03_TAIL ends
main_03 group BULLET_A_TEXT, LASER_SC_TEXT, B6_BALLS_TEXT, B6_PATTERN_A_TEXT, B6_UPDATE_TEXT, PHASE23_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _bullet_template_tune
org 041deh
_bullet_template_tune label word
public _bullet_template
org 0577eh
_bullet_template label byte
public _boss
org 05abah
_boss label byte
public _shinki_phase_2_3_pattern
org 0c33ah
_shinki_phase_2_3_pattern label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

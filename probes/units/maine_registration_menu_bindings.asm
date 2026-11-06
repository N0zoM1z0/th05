; Actual foreign code frames and DATA labels only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN
org 0600h
PALETTE_BLACK_IN label far
public PALETTE_BLACK_OUT
org 0644h
PALETTE_BLACK_OUT label far
public GAIJI_PUTCA
org 0121ah
GAIJI_PUTCA label far
public GRAPH_COPY_PAGE
org 0133ch
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 01b8ah
PALETTE_SHOW label far
public TEXT_CLEAR
org 02298h
TEXT_CLEAR label far
public _super_free
org 02730h
_super_free label far
public SUPER_ENTRY_BFNT
org 02894h
SUPER_ENTRY_BFNT label far
org 0a540h
_TEXT ends
REG_SCORE_TEXT segment byte public 'CODE' use16
assume cs:REG_SCORE_TEXT
public @HISCORE_SCOREDAT_LOAD_FOR$QI
org (0b646h - 0a540h)
@HISCORE_SCOREDAT_LOAD_FOR$QI label near
public @hiscore_scoredat_save$qv
org (0b6a3h - 0a540h)
@hiscore_scoredat_save$qv label near
public @score_insert$qv
org (0b730h - 0a540h)
@score_insert$qv label near
org (0ba84h - 0a540h)
REG_SCORE_TEXT ends
REG_HELPERS_TEXT segment byte public 'CODE' use16
assume cs:REG_HELPERS_TEXT
public @REG_NAME_PUT$QI10PLAYCHAR_TUC
org (0ba84h - 0ba84h)
@REG_NAME_PUT$QI10PLAYCHAR_TUC label near
public @PLACES_PUT$QI
org (0bcd3h - 0ba84h)
@PLACES_PUT$QI label near
public @ALPHABET_CURSOR_PUT$QIII
org (0bcedh - 0ba84h)
@ALPHABET_CURSOR_PUT$QIII label near
public @registration_frame$qv
org (0bd1eh - 0ba84h)
@registration_frame$qv label near
public @GLYPHBALL_SPAWN$QIII10PLAYCHAR_TUC
org (0bd46h - 0ba84h)
@GLYPHBALL_SPAWN$QIII10PLAYCHAR_TUC label near
public @glyphballs_commit_and_wait$qv
org (0c16ch - 0ba84h)
@glyphballs_commit_and_wait$qv label near
org (0c1ddh - 0ba84h)
REG_HELPERS_TEXT ends
REG_MENU_TEXT segment byte public 'CODE' use16
REG_MENU_TEXT ends
REG_MENU_TAIL segment byte public 'CODE' use16
org (0e800h - 0c5e7h)
REG_MENU_TAIL ends
GROUP_01 group REG_SCORE_TEXT, REG_HELPERS_TEXT, REG_MENU_TEXT, REG_MENU_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011ah
GRAPH_PUTSA_FX label far
public SND_SE_PLAY
org 02e6h
SND_SE_PLAY label far
public _bgimage_snap
org 036ch
_bgimage_snap label far
public _bgimage_free
org 040ah
_bgimage_free label far
public SND_LOAD
org 0566h
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 061eh
SND_KAJA_INTERRUPT label far
public @PI_LOAD$QINXC
org 0780h
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org 07b2h
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org 0862h
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0888h
@PI_FREE$QI label far
public @input_reset_sense_held$qv
org 0a08h
@input_reset_sense_held$qv label far
public @INPUT_WAIT_FOR_CHANGE$QI
org 0a18h
@INPUT_WAIT_FOR_CHANGE$QI label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _gALPHABET
org 014eeh
_gALPHABET label byte
public _entered_name_cursor
org 01522h
_entered_name_cursor label word
public _registration_bg_fn
org 01550h
_registration_bg_fn label byte
public _registration_score_font
org 01558h
_registration_score_font label byte
public _registration_cloud_font
org 01562h
_registration_cloud_font label byte
public _registration_ball_font
org 0156ch
_registration_ball_font label byte
public _registration_turbo_warning_shado
org 01576h
_registration_turbo_warning_shado label byte
public _registration_turbo_warning
org 015a9h
_registration_turbo_warning label byte
public _registration_bgm_fn
org 015dch
_registration_bgm_fn label byte
public _resident
org 01d6eh
_resident label dword
public _key_det
org 029fah
_key_det label word
public _hi
org 04f1ah
_hi label byte
public _glyphballs
org 04f7ah
_glyphballs label byte
public _entered_place
org 05076h
_entered_place label byte
public _rank
org 05077h
_rank label byte
public _playchar
org 05078h
_playchar label byte
org 05079h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; One original-order display/menu C++ source, all foreign providers and original DATA only.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_IN, PALETTE_BLACK_OUT, FILE_APPEND, FILE_CLOSE, FILE_CREATE, FILE_EXIST, FILE_READ, FILE_ROPEN, FILE_SEEK, FILE_WRITE, GRCG_HLINE, GRCG_SETCOLOR, GRCG_VLINE, GAIJI_PUTCA, GRAPH_COPY_PAGE, IATAN2, PALETTE_SHOW, IRAND, TEXT_CLEAR, _super_free, SUPER_ENTRY_BFNT, SUPER_PUT_RECT, SUPER_PUT, GRAPH_GAIJI_PUTS, GRAPH_GAIJI_PUTC
org 00600h
PALETTE_BLACK_IN label far
org 00644h
PALETTE_BLACK_OUT label far
org 00886h
FILE_APPEND label far
org 00946h
FILE_CLOSE label far
org 00956h
FILE_CREATE label far
org 00996h
FILE_EXIST label far
org 009b2h
FILE_READ label far
org 00a66h
FILE_ROPEN label far
org 00aa2h
FILE_SEEK label far
org 00af2h
FILE_WRITE label far
org 00e5eh
GRCG_HLINE label far
org 00f28h
GRCG_SETCOLOR label far
org 00f58h
GRCG_VLINE label far
org 0121ah
GAIJI_PUTCA label far
org 0133ch
GRAPH_COPY_PAGE label far
org 01a8ch
IATAN2 label far
org 01b8ah
PALETTE_SHOW label far
org 01df8h
IRAND label far
org 02298h
TEXT_CLEAR label far
org 02730h
_super_free label far
org 02894h
SUPER_ENTRY_BFNT label far
org 02974h
SUPER_PUT_RECT label far
org 02b68h
SUPER_PUT label far
org 0383ch
GRAPH_GAIJI_PUTS label far
org 038e6h
GRAPH_GAIJI_PUTC label far
org 0a540h
_TEXT ends
REG_SCORE_TEXT segment byte public 'CODE' use16
org (0b4d6h - 0a540h)
REG_SCORE_TEXT ends
REG_FULL_TEXT segment byte public 'CODE' use16
REG_FULL_TEXT ends
REG_VALUES_TEXT segment byte public 'CODE' use16
REG_VALUES_TEXT ends
REG_DISPLAY_TEXT segment byte public 'CODE' use16
REG_DISPLAY_TEXT ends
REG_PLACE_ENTRY_TEXT segment byte public 'CODE' use16
REG_PLACE_ENTRY_TEXT ends
REG_PLACES_TEXT segment byte public 'CODE' use16
REG_PLACES_TEXT ends
REG_ALPHA_TEXT segment byte public 'CODE' use16
REG_ALPHA_TEXT ends
REG_NAME_TEXT segment byte public 'CODE' use16
REG_NAME_TEXT ends
REG_MOTION_TEXT segment byte public 'CODE' use16
REG_MOTION_TEXT ends
REG_HELPERS_TEXT segment byte public 'CODE' use16
REG_HELPERS_TEXT ends
REG_MENU_TEXT segment byte public 'CODE' use16
REG_MENU_TEXT ends
REG_FULL_TAIL segment byte public 'CODE' use16
org (0e800h - 0c5e7h)
REG_FULL_TAIL ends
GROUP_01 group REG_SCORE_TEXT, REG_FULL_TEXT, REG_VALUES_TEXT, REG_DISPLAY_TEXT, REG_PLACE_ENTRY_TEXT, REG_PLACES_TEXT, REG_ALPHA_TEXT, REG_NAME_TEXT, REG_MOTION_TEXT, REG_HELPERS_TEXT, REG_MENU_TEXT, REG_FULL_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX, SND_SE_PLAY, _snd_se_update, _bgimage_snap, _bgimage_free, VECTOR2_AT, BGIMAGE_PUT_RECT_16, SND_LOAD, SND_KAJA_INTERRUPT, @PI_LOAD$QINXC, @PI_PUT_8$QIII, @PI_PALETTE_APPLY$QI, @PI_FREE$QI, @input_reset_sense_held$qv, @INPUT_WAIT_FOR_CHANGE$QI, @FRAME_DELAY$QI
org 011ah
GRAPH_PUTSA_FX label far
org 02e6h
SND_SE_PLAY label far
org 0320h
_snd_se_update label far
org 036ch
_bgimage_snap label far
org 040ah
_bgimage_free label far
org 04a0h
VECTOR2_AT label far
org 04e4h
BGIMAGE_PUT_RECT_16 label far
org 0566h
SND_LOAD label far
org 061eh
SND_KAJA_INTERRUPT label far
org 0780h
@PI_LOAD$QINXC label far
org 07b2h
@PI_PUT_8$QIII label far
org 0862h
@PI_PALETTE_APPLY$QI label far
org 0888h
@PI_FREE$QI label far
org 0a08h
@input_reset_sense_held$qv label far
org 0a18h
@INPUT_WAIT_FOR_CHANGE$QI label far
org 0a88h
@FRAME_DELAY$QI label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _gALPHABET, _registration_page, _entered_name_cursor, _SCOREDAT_FN, _SCOREDAT_FN_0
public _SCOREDAT_FN_1, _SCOREDAT_FN_2, _registration_bg_fn, _registration_score_font, _registration_cloud_font, _registration_ball_font
public _registration_turbo_warning_shado, _registration_turbo_warning, _registration_bgm_fn, _resident, _key_det, _hi
public _glyphballs, _entered_place, _rank, _playchar
org 00238h
_PaletteTone label word
org 014eeh
_gALPHABET label byte
org 01521h
_registration_page label byte
org 01522h
_entered_name_cursor label word
org 01524h
_SCOREDAT_FN label byte
org 0152fh
_SCOREDAT_FN_0 label byte
org 0153ah
_SCOREDAT_FN_1 label byte
org 01545h
_SCOREDAT_FN_2 label byte
org 01550h
_registration_bg_fn label byte
org 01558h
_registration_score_font label byte
org 01562h
_registration_cloud_font label byte
org 0156ch
_registration_ball_font label byte
org 01576h
_registration_turbo_warning_shado label byte
org 015a9h
_registration_turbo_warning label byte
org 015dch
_registration_bgm_fn label byte
org 01d6eh
_resident label dword
org 029fah
_key_det label word
org 04f1ah
_hi label byte
org 04f7ah
_glyphballs label byte
org 05076h
_entered_place label byte
org 05077h
_rank label byte
org 05078h
_playchar label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

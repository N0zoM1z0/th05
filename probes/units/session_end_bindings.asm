; Real outside-only code/state context for adjacent cleanup and pause.
; No instruction bodies, resource/glyph bytes, stack or inside-owner padding.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTSA
org 01dbeh
GAIJI_PUTSA label far
public TEXT_PUTSA
org 02598h
TEXT_PUTSA label far
public SUPER_CLEAN
org 02df0h
SUPER_CLEAN label far
org 0ae10h
_TEXT ends
SESSION_END_TEXT segment byte public 'CODE' use16
assume cs:SESSION_END_TEXT
org 07f8h
SESSION_END_TEXT ends
SESSION_END_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:SESSION_END_MAIN01_TEXT
public @std_free$qv
org 010a4h
@std_free$qv label near
public @map_free$qv
org 02eb0h
@map_free$qv label near
public @dialog_free$qv
org 08280h
@dialog_free$qv label near
public @bb_boss_free$qv
org 08dcbh
@bb_boss_free$qv label near
org 0935ah
SESSION_END_MAIN01_TEXT ends
main_01 group SESSION_END_TEXT, SESSION_END_MAIN01_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public @input_reset_sense_held$qv
org 0618h
@input_reset_sense_held$qv label far
public @INPUT_WAIT_FOR_CHANGE$QI
org 0628h
@INPUT_WAIT_FOR_CHANGE$QI label far
public CDG_FREE
org 0788h
CDG_FREE label far
org 07c0h
SHARED ends
SESSION_END_MAIN03_SPACE segment byte public 'CODE' use16
assume cs:SESSION_END_MAIN03_SPACE
org 0b760h
SESSION_END_MAIN03_SPACE ends
_DATA segment word public 'DATA' use16
public _gsCHUUDAN
org 092h
_gsCHUUDAN label byte
public _gsSAIKAI
org 095h
_gsSAIKAI label byte
public _gsSHUURYOU
org 098h
_gsSHUURYOU label byte
public _aGAME_PAUSE_SPACES_1
org 020dh
_aGAME_PAUSE_SPACES_1 label byte
public _aGAME_PAUSE_SPACES_2
org 0212h
_aGAME_PAUSE_SPACES_2 label byte
public _aGAME_PAUSE_SPACES_3
org 0217h
_aGAME_PAUSE_SPACES_3 label byte
public _key_det
org 03064h
_key_det label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

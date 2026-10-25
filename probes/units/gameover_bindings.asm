; Real symbol-only MAIN game-over context. No foreign bodies or data values.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT, GAIJI_PUTCA, GAIJI_PUTSA, PALETTE_SHOW, TEXT_PUTSA
org 00644h
PALETTE_BLACK_OUT label far
org 01d7ah
GAIJI_PUTCA label far
org 01dbeh
GAIJI_PUTSA label far
org 02158h
PALETTE_SHOW label far
org 02598h
TEXT_PUTSA label far
org 0ae10h
_TEXT ends
GAMEOVER_TEXT segment byte public 'CODE' use16
assume cs:GAMEOVER_TEXT
public NULLFUNC_NEAR, @hiscore_continue_enter$qv, @GAMEEXECL$QNXC
public @score_reset$qv, @hud_lives_put$qv, @hud_bombs_put$qv, HUD_SCORE_PUT
org 0192eh
NULLFUNC_NEAR label near
org 01b88h
@hiscore_continue_enter$qv label near
org 020b2h
@GAMEEXECL$QNXC label far
org 021b6h
@score_reset$qv label near
org 02225h
@hud_lives_put$qv label far
org 022d9h
@hud_bombs_put$qv label far
org 026b0h
HUD_SCORE_PUT label near
org 0296ch
GAMEOVER_TEXT ends
; This contribution follows the complete compiler owner [D77C,DAE1).
GAMEOVER_AFTER_TEXT segment byte public 'CODE' use16
assume cs:GAMEOVER_AFTER_TEXT
public SHOT_LEVEL_UPDATE, @overlay_wipe$qv, @overlay_black$qv
org 00901h
SHOT_LEVEL_UPDATE label far
org 0426fh
@overlay_wipe$qv label near
org 04291h
@overlay_black$qv label near
org 06fcfh
GAMEOVER_AFTER_TEXT ends
main_01 group GAMEOVER_TEXT, GAMEOVER_AFTER_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_KAJA_INTERRUPT, @input_reset_sense_held$qv
public @INPUT_WAIT_FOR_CHANGE$QI, @FRAME_DELAY$QI
org 004ach
SND_KAJA_INTERRUPT label far
org 00618h
@input_reset_sense_held$qv label far
org 00628h
@INPUT_WAIT_FOR_CHANGE$QI label far
org 00652h
@FRAME_DELAY$QI label far
org 0bf20h
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone, _gGAMEOVER, _gCONTINUE_QUESTION, _gYES, _gNO, _gCREDIT
public _gameover_erase_in, _gameover_erase_out, _maine_binary
public _key_det, _power, _dream, _continues_used, _gameover_fade_frame
public _resident, _overlay1, _lives, _bombs, _stage_id
org 003dah
_PaletteTone label word
org 0144ah
_gGAMEOVER label byte
org 01454h
_gCONTINUE_QUESTION label byte
org 0145fh
_gYES label byte
org 01463h
_gNO label byte
org 01466h
_gCREDIT label byte
org 0146dh
_gameover_erase_in label byte
org 01470h
_gameover_erase_out label byte
org 01473h
_maine_binary label byte
org 03064h
_key_det label word
org 036f0h
_power label byte
org 036f6h
_dream label byte
org 03702h
_continues_used label byte
org 03722h
_gameover_fade_frame label byte
org 041fch
_resident label dword
org 04abeh
_overlay1 label word
org 04ad4h
_lives label byte
org 04ad5h
_bombs label byte
org 0576eh
_stage_id label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

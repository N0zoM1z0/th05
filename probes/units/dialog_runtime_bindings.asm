; True foreign TH05 dialog symbols only. The three compiler-body ASM graphics
; helpers and other dialog TUs remain foreign. No instructions/values/stack.
.386
.model large
MAIN01_BASE equ 0ae10h
UNIT_START equ 13b18h
UNIT_END equ 13e58h
TAIL_LAST equ 14081h
SHARED_BASE equ 14ab0h
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GAIJI_PUTCA, TEXT_BOXFILLA, TEXT_PUTCA, TEXT_PUTSA
public PALETTE_WHITE_IN, PALETTE_WHITE_OUT, SUPER_ENTRY_BFNT, SUPER_CLEAN, SUPER_ROLL_PUT, _strlen
org 01d7ah
GAIJI_PUTCA label far
org 024a8h
TEXT_BOXFILLA label far
org 02540h
TEXT_PUTCA label far
org 02598h
TEXT_PUTSA label far
org 0272ah
PALETTE_WHITE_IN label far
org 0276ah
PALETTE_WHITE_OUT label far
org 02d16h
SUPER_ENTRY_BFNT label far
org 02df0h
SUPER_CLEAN label far
org 02fe0h
SUPER_ROLL_PUT label far
org 0684dh
_strlen label far
org MAIN01_BASE
_TEXT ends
DIALOG_RUN_TEXT segment byte public 'CODE' use16
assume cs:DIALOG_RUN_TEXT
public @overlay_wipe$qv, @DIALOG_BOX_PUT$QUIUII
org (11d50h - MAIN01_BASE)
@overlay_wipe$qv label near
org (13a3eh - MAIN01_BASE)
@DIALOG_BOX_PUT$QUIUII label near
org (UNIT_START - MAIN01_BASE)
DIALOG_RUN_TEXT ends
DIALOG_RUN_TAIL segment byte public 'CODE' use16
assume cs:DIALOG_RUN_TAIL
public @DIALOG_FACE_LOAD_UNPUT_PUT_FREE_$QIII
public @main_pat_exalice_override_and_su$qv
org (13f0fh - UNIT_END)
@DIALOG_FACE_LOAD_UNPUT_PUT_FREE_$QIII label near
org (TAIL_LAST - UNIT_END)
@main_pat_exalice_override_and_su$qv label near
DIALOG_RUN_TAIL ends
main_01 group DIALOG_RUN_TEXT, DIALOG_RUN_TAIL
DIALOG_RUNTIME_SHARED_GAP segment byte public 'CODE' use16
org (SHARED_BASE - TAIL_LAST)
DIALOG_RUNTIME_SHARED_GAP ends
DIALOG_RUNTIME_SHARED segment word public 'CODE' use16
assume cs:DIALOG_RUNTIME_SHARED
public SND_LOAD, SND_KAJA_INTERRUPT, @input_reset_sense$qv, @input_sense$qv
public @INPUT_WAIT_FOR_CHANGE$QI, @FRAME_DELAY$QI
org 003f4h
SND_LOAD label far
org 004ach
SND_KAJA_INTERRUPT label far
org 00512h
@input_reset_sense$qv label far
org 0051ah
@input_sense$qv label far
org 00628h
@INPUT_WAIT_FOR_CHANGE$QI label far
org 00652h
@FRAME_DELAY$QI label far
DIALOG_RUNTIME_SHARED ends
DIALOG_RUNTIME_DGROUP_GAP segment para public 'CODE' use16
org (DGROUP_BASE - 15110h)
DIALOG_RUNTIME_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _dialog_kanji_buf, _vsync_Count1, _key_det, _stage_id
public _dialog_p, _dialog_cursor, _dialog_side
org 01ef3h
_dialog_kanji_buf label byte
org 0267ah
_vsync_Count1 label word
org 03064h
_key_det label word
org 0576eh
_stage_id label byte
org 0c658h
_dialog_p label dword
org 0c65ch
_dialog_cursor label byte
org 0c660h
_dialog_side label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

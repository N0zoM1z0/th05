; Original outside-only context for natural MAIN entry/gameplay prefix.
; No implementation, NOP, resource payload or stack is supplied here.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_SHOW
org 02158h
PALETTE_SHOW label far
public TEXT_CLEAR
org 024f6h
TEXT_CLEAR label far
org 0ae10h
_TEXT ends
DEMO_TEXT segment word public 'CODE' use16
org 028h
DEMO_TEXT ends
RUNTIME_MAIN01_TEXT segment byte public 'CODE' use16
assume cs:RUNTIME_MAIN01_TEXT
public @gameplay_loop$qv
@gameplay_loop$qv label near
public @stage_session_init$qv
org (0b237h - 0aea6h)
@stage_session_init$qv label near
public _stage_session_free
org (0b608h - 0aea6h)
_stage_session_free label near
public @ems_allocate_and_preload_eyecatc$qv
org (0b826h - 0aea6h)
@ems_allocate_and_preload_eyecatc$qv label near
public @GAMEEXECL$QNXC
org (0cec2h - 0aea6h)
@GAMEEXECL$QNXC label far
public @cfg_load_resident_ptr$qv
org (0e61eh - 0aea6h)
@cfg_load_resident_ptr$qv label near
org (014ab0h - 0aea6h)
RUNTIME_MAIN01_TEXT ends
main_01 group DEMO_TEXT, RUNTIME_MAIN01_TEXT
SHARED segment para public 'CODE' use16
assume cs:SHARED
public SND_DETERMINE_MODES
org 0124h
SND_DETERMINE_MODES label far
public _snd_se_update
org 026ch
_snd_se_update label far
public SND_LOAD
org 03f4h
SND_LOAD label far
public @GAME_INIT_MAIN$QNXUC
org 04cah
@GAME_INIT_MAIN$QNXUC label far
public @input_reset_sense$qv
org 0512h
@input_reset_sense$qv label far
public @input_sense$qv
org 051ah
@input_sense$qv label far
public @FRAME_DELAY$QI
org 0652h
@FRAME_DELAY$QI label far
org 07c0h
SHARED ends
ENTRY_MAIN03_SPACE segment byte public 'CODE' use16
org 0b760h
ENTRY_MAIN03_SPACE ends
main_03 group ENTRY_MAIN03_SPACE
_DATA segment word public 'DATA' use16
public _main_pf_fn
org 0b2h
_main_pf_fn label byte
public _se_fn
org 0beh
_se_fn label byte
public _op_fn
org 0c3h
_op_fn label byte
public _random_seed
org 0418h
_random_seed label dword
public _mem_assign_paras
org 0824h
_mem_assign_paras label word
public _resident
org 041fch
_resident label dword
public _quit
org 0576ch
_quit label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

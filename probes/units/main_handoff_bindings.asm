; Real outside-only context for score-save34 and GameExecl159.
; No foreign bodies, assets, stack or inside-owner instruction gaps.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRAPH_HIDE
org 01edch
GRAPH_HIDE label far
public TEXT_CLEAR
org 024f6h
TEXT_CLEAR label far
public SUPER_FREE
org 029eah
SUPER_FREE label far
public EMS_FREE
org 0402ah
EMS_FREE label far
public _execl
org 0a6a1h
_execl label far
org 0ae10h
_TEXT ends
HANDOFF_TEXT segment byte public 'CODE' use16
assume cs:HANDOFF_TEXT
public @std_free$qv
org 019eah
@std_free$qv label near
org 02090h
HANDOFF_TEXT ends
HANDOFF_FOREIGN_TEXT segment byte public 'CODE' use16
assume cs:HANDOFF_FOREIGN_TEXT
public @score_reset$qv
org 065h
@score_reset$qv label near
public BB_TXT_FREE
org 015a1h
BB_TXT_FREE label near
public @map_free$qv
org 016a5h
@map_free$qv label near
public BB_PLAYCHAR_FREE
org 034e3h
BB_PLAYCHAR_FREE label near
public @dialog_free$qv
org 06a75h
@dialog_free$qv label near
public @bb_boss_free$qv
org 075c0h
@bb_boss_free$qv label near
org 07b4fh
HANDOFF_FOREIGN_TEXT ends
main_01 group HANDOFF_TEXT, HANDOFF_FOREIGN_TEXT
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public @game_exit$qv
org 034ch
@game_exit$qv label far
public CDG_FREE_ALL
org 07beh
CDG_FREE_ALL label far
org 0bf20h
SHARED ends
_DATA segment word public 'DATA' use16
public _enemies_gone
org 014a4h
_enemies_gone label word
public _enemies_killed
org 014a6h
_enemies_killed label word
public _items_spawned
org 01e7ah
_items_spawned label word
public _items_collected
org 01e7ch
_items_collected label word
public _total_point_items_collected
org 01e80h
_total_point_items_collected label word
public _total_max_valued_point_items_col
org 01e82h
_total_max_valued_point_items_col label word
public _total_slow_frames
org 01ec2h
_total_slow_frames label dword
public _total_frames
org 01ec6h
_total_frames label dword
public _total_std_frames
org 01ecah
_total_std_frames label word
public _score
org 03702h
_score label byte
public _resident
org 041fch
_resident label dword
public _Ems
org 05774h
_Ems label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

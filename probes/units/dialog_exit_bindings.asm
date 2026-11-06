; Foreign symbol positions for the complete dialog-exit compiler contribution.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_ALLOCBYTE, EMS_READ
org 0281ah
HMEM_ALLOCBYTE label far
org 03f6ah
EMS_READ label far
org 0ae10h
_TEXT ends
DEMO_GAMEEXECL_CONTEXT segment byte public 'CODE' use16
DEMO_GAMEEXECL_CONTEXT ends
DEMO_TEXT segment byte public 'CODE' use16
DEMO_TEXT ends
DIALOG_TAIL_TEXT segment byte public 'CODE' use16
org (14007h - 0ae10h)
DIALOG_TAIL_TEXT ends
main_01 group DEMO_GAMEEXECL_CONTEXT, DEMO_TEXT, DIALOG_TAIL_TEXT
DIALOG_EXIT_SHARED_GAP segment byte public 'CODE' use16
org (14ab0h - 14081h)
DIALOG_EXIT_SHARED_GAP ends
SHARED segment word public 'CODE' use16
assume cs:SHARED
public CDG_LOAD_SINGLE_NOALPHA
org 00668h
CDG_LOAD_SINGLE_NOALPHA label far
SHARED ends
DIALOG_EXIT_DGROUP_GAP segment para public 'CODE' use16
org (209d0h - 15120h)
DIALOG_EXIT_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _BOMB_BG_REIMU_FN, _BOMB_BG_MARISA_FN, _BOMB_BG_MIMA_FN, _BOMB_BG_YUUKA_FN
public _cdg_slots, _playchar, _Ems
org 01f2dh
_BOMB_BG_REIMU_FN label byte
org 01f35h
_BOMB_BG_MARISA_FN label byte
org 01f3dh
_BOMB_BG_MIMA_FN label byte
org 01f45h
_BOMB_BG_YUUKA_FN label byte
org 0306ch
_cdg_slots label byte
org 05773h
_playchar label byte
org 05774h
_Ems label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

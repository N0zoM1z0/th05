; Real outside-only callback context for semantic SHOT_FUNCS data80.
; No callback bodies, raw word values, stack or DATA payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SHOT_TABLE_CONTEXT segment byte public 'CODE' use16
SHOT_TABLE_CONTEXT ends
SESSION_INIT_TEXT segment byte public 'CODE' use16
SESSION_INIT_TEXT ends
SESSION_MAIN01_TEXT segment byte public 'CODE' use16
SESSION_MAIN01_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
assume cs:MAIN_01_TEXT
public @SHOT_L0$QV
org 038a6h
@SHOT_L0$QV label near
public @SHOT_L1$QV
org 038c1h
@SHOT_L1$QV label near
public SHOT_REIMU_L2
org 038ebh
SHOT_REIMU_L2 label near
public SHOT_REIMU_L3
org 0396ch
SHOT_REIMU_L3 label near
public SHOT_REIMU_L4
org 039f0h
SHOT_REIMU_L4 label near
public SHOT_REIMU_L5
org 03a74h
SHOT_REIMU_L5 label near
public SHOT_REIMU_L6
org 03b11h
SHOT_REIMU_L6 label near
public SHOT_REIMU_L7
org 03baeh
SHOT_REIMU_L7 label near
public SHOT_REIMU_L8
org 03c4bh
SHOT_REIMU_L8 label near
public SHOT_REIMU_L9
org 03ccch
SHOT_REIMU_L9 label near
public SHOT_MARISA_L2
org 03d82h
SHOT_MARISA_L2 label near
public SHOT_MARISA_L3
org 03e04h
SHOT_MARISA_L3 label near
public SHOT_MARISA_L4
org 03ebfh
SHOT_MARISA_L4 label near
public SHOT_MARISA_L5
org 03fbdh
SHOT_MARISA_L5 label near
public SHOT_MARISA_L6
org 040c5h
SHOT_MARISA_L6 label near
public SHOT_MARISA_L7
org 041d3h
SHOT_MARISA_L7 label near
public SHOT_MARISA_L8
org 04311h
SHOT_MARISA_L8 label near
public SHOT_MARISA_L9
org 0444fh
SHOT_MARISA_L9 label near
public SHOT_MIMA_L2
org 045d8h
SHOT_MIMA_L2 label near
public SHOT_MIMA_L3
org 04643h
SHOT_MIMA_L3 label near
public SHOT_MIMA_L4
org 046bbh
SHOT_MIMA_L4 label near
public SHOT_MIMA_L5
org 04754h
SHOT_MIMA_L5 label near
public SHOT_MIMA_L6
org 047ebh
SHOT_MIMA_L6 label near
public SHOT_MIMA_L7
org 04897h
SHOT_MIMA_L7 label near
public SHOT_MIMA_L8
org 0494fh
SHOT_MIMA_L8 label near
public SHOT_MIMA_L9
org 04a16h
SHOT_MIMA_L9 label near
public SHOT_YUUKA_L2
org 0764eh
SHOT_YUUKA_L2 label near
public SHOT_YUUKA_L3
org 076c6h
SHOT_YUUKA_L3 label near
public SHOT_YUUKA_L4
org 07751h
SHOT_YUUKA_L4 label near
public SHOT_YUUKA_L5
org 077efh
SHOT_YUUKA_L5 label near
public SHOT_YUUKA_L6
org 078aeh
SHOT_YUUKA_L6 label near
public SHOT_YUUKA_L7
org 07997h
SHOT_YUUKA_L7 label near
public SHOT_YUUKA_L8
org 07a99h
SHOT_YUUKA_L8 label near
public SHOT_YUUKA_L9
org 07b9ah
SHOT_YUUKA_L9 label near
org (14ab0h - 0ae10h)
MAIN_01_TEXT ends
main_01 group SHOT_TABLE_CONTEXT, SESSION_INIT_TEXT, SESSION_MAIN01_TEXT, MAIN_01_TEXT
SHOT_TABLE_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
SHOT_TABLE_SHARED_SPACE ends
BULLET_A_TEXT segment byte public 'CODE' use16
org (209d0h - 15270h)
BULLET_A_TEXT ends
main_03 group BULLET_A_TEXT
_DATA segment word public 'DATA' use16
org 01d70h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

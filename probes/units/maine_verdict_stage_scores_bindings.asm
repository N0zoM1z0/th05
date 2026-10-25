; Real foreign symbols/extents only; owned compiler contribution remains empty.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0A540h
_TEXT ends
VERDICT_FMT_TEXT segment byte public 'CODE' use16
assume cs:VERDICT_FMT_TEXT
public @VERDICT_SCORE_PUT$QIIMX13SCORE_LEBCD_T
org 0213Fh
@VERDICT_SCORE_PUT$QIIMX13SCORE_LEBCD_T label near
org 02CDDh
VERDICT_FMT_TEXT ends
VERDICT_COMMENT_TEXT segment byte public 'CODE' use16
VERDICT_COMMENT_TEXT ends
VERDICT_SCORES_TEXT segment byte public 'CODE' use16
VERDICT_SCORES_TEXT ends
VERDICT_DISPLAY_TAIL segment byte public 'CODE' use16
org 014E1h
VERDICT_DISPLAY_TAIL ends
group_01 group VERDICT_FMT_TEXT, VERDICT_COMMENT_TEXT, VERDICT_SCORES_TEXT, VERDICT_DISPLAY_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
org 01910h
SHARED ends
_DATA segment word public 'DATA' use16
public _verdict_text_left
org 015E2h
_verdict_text_left label word
public _verdict_text_color
org 015E4h
_verdict_text_color label word
public _verdict_comment_color
org 015E6h
_verdict_comment_color label word
public _verdict_text_top
org 015E8h
_verdict_text_top label word
public _verdict_stage_1_title
org 016FBh
_verdict_stage_1_title label byte
public _verdict_stage_2_title
org 01704h
_verdict_stage_2_title label byte
public _verdict_stage_3_title
org 0170Dh
_verdict_stage_3_title label byte
public _verdict_stage_4_title
org 01716h
_verdict_stage_4_title label byte
public _verdict_stage_5_title
org 0171Fh
_verdict_stage_5_title label byte
public _verdict_stage_6_title
org 01728h
_verdict_stage_6_title label byte
public _verdict_final_score_title
org 01731h
_verdict_final_score_title label byte
public _resident
org 01D6Eh
_resident label dword
org 050C3h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Complete natural3384-byte verdict family; all supplied labels/extents are foreign.
; No function instructions, inside holes, target values, table bytes or .stack.
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
public FILE_CLOSE
org 0946h
FILE_CLOSE label far
public FILE_READ
org 09B2h
FILE_READ label far
public FILE_ROPEN
org 0A66h
FILE_ROPEN label far
public FILE_SEEK
org 0AA2h
FILE_SEEK label far
public GRAPH_COPY_PAGE
org 0133Ch
GRAPH_COPY_PAGE label far
public PALETTE_SHOW
org 01B8Ah
PALETTE_SHOW label far
public GRAPH_GAIJI_PUTS
org 0383Ch
GRAPH_GAIJI_PUTS label far
org 0A540h
_TEXT ends
VERDICT_FULL_TEXT segment byte public 'CODE' use16
org 020A7h
VERDICT_FULL_TEXT ends
VERDICT_FULL_TAIL segment byte public 'CODE' use16
org (0E800h - 0D31Fh)
VERDICT_FULL_TAIL ends
group_01 group VERDICT_FULL_TEXT, VERDICT_FULL_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public GRAPH_PUTSA_FX
org 011Ah
GRAPH_PUTSA_FX label far
public @PI_LOAD$QINXC
org 0780h
@PI_LOAD$QINXC label far
public @PI_PUT_8$QIII
org 07B2h
@PI_PUT_8$QIII label far
public @PI_PALETTE_APPLY$QI
org 0862h
@PI_PALETTE_APPLY$QI label far
public @PI_FREE$QI
org 0888h
@PI_FREE$QI label far
public @INPUT_WAIT_FOR_CHANGE$QI
org 0A18h
@INPUT_WAIT_FOR_CHANGE$QI label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
org 01910h
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _random_seed
org 0276h
_random_seed label dword
public _graph_putsa_fx_func
org 06BCh
_graph_putsa_fx_func label word
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
public _skill_subtract
org 015EAh
_skill_subtract label byte
public _verdict_rank_glyphs
org 015EBh
_verdict_rank_glyphs label byte
public _graph_3_digit_put_as_fixed_2_dig
org 01613h
_graph_3_digit_put_as_fixed_2_dig label byte
public _verdict_score_unit
org 01614h
_verdict_score_unit label byte
public _verdict_decimal_point
org 01617h
_verdict_decimal_point label byte
public _verdict_percent_sign
org 0161Ah
_verdict_percent_sign label byte
public _verdict_fraction_point
org 0161Dh
_verdict_fraction_point label byte
public _verdict_bonus_percent_sign
org 01620h
_verdict_bonus_percent_sign label byte
public _verdict_heading
org 01623h
_verdict_heading label byte
public _verdict_rank_label
org 0163Bh
_verdict_rank_label label byte
public _verdict_score_label
org 01642h
_verdict_score_label label byte
public _verdict_misses_label
org 0164Bh
_verdict_misses_label label byte
public _verdict_bombs_label
org 01654h
_verdict_bombs_label label byte
public _verdict_completion_label
org 01661h
_verdict_completion_label label byte
public _verdict_kills_label
org 0166Eh
_verdict_kills_label label byte
public _verdict_items_label
org 01679h
_verdict_items_label label byte
public _verdict_point_items_label
org 01688h
_verdict_point_items_label label byte
public _verdict_bonus_label
org 0169Dh
_verdict_bonus_label label byte
public _verdict_slowdown_label
org 016A4h
_verdict_slowdown_label label byte
public _verdict_skill_label
org 016AFh
_verdict_skill_label label byte
public _verdict_miss_times
org 016BCh
_verdict_miss_times label byte
public _verdict_bomb_times
org 016BFh
_verdict_bomb_times label byte
public _verdict_points_unit
org 016C2h
_verdict_points_unit label byte
public _verdict_comment_filename
org 016C5h
_verdict_comment_filename label byte
public _verdict_unrated
org 016CEh
_verdict_unrated label byte
public _verdict_slowdown_warning
org 016DDh
_verdict_slowdown_warning label byte
public _verdict_picture_filename
org 016F4h
_verdict_picture_filename label byte
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
public _verdict_capture_quarter
org 0507Ch
_verdict_capture_quarter label byte
public _skill
org 0507Eh
_skill label dword
public _verdict_skill_quarter
org 05082h
_verdict_skill_quarter label dword
public _verdict_rank
org 05086h
_verdict_rank label byte
public _verdict_comments
org 05087h
_verdict_comments label byte
org 050C3h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Complete 17-function Staff scene and two real inline-ASM bitmap kernels plus controller; foreign providers only.
; All non-owned providers and frames use the true physical MAINE addresses, with no instruction/asset bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BOXFILL, GRCG_BYTEBOXFILL_X, GRCG_CIRCLEFILL, GRC_SETCLIP, GRCG_SETCOLOR, GAIJI_PUTSA
public IATAN2, IHYPOT, PALETTE_SHOW, IRAND, TEXT_CLEAR, TEXT_PUTSA
public SUPER_PUT_RECT, SUPER_PUT_TINY_SMALL, SUPER_FREE, SUPER_ENTRY_BFNT, SUPER_CONVERT_TINY
org 00bceh
GRCG_BOXFILL label far
org 00c9eh
GRCG_BYTEBOXFILL_X label far
org 00d36h
GRCG_CIRCLEFILL label far
org 00dcch
GRC_SETCLIP label far
org 00f28h
GRCG_SETCOLOR label far
org 0125eh
GAIJI_PUTSA label far
org 01a8ch
IATAN2 label far
org 01af8h
IHYPOT label far
org 01b8ah
PALETTE_SHOW label far
org 01df8h
IRAND label far
org 02298h
TEXT_CLEAR label far
org 022aah
TEXT_PUTSA label far
org 02730h
SUPER_FREE label far
org 02894h
SUPER_ENTRY_BFNT label far
org 02974h
SUPER_PUT_RECT label far
org 02d1ah
SUPER_CONVERT_TINY label far
org 02db6h
SUPER_PUT_TINY_SMALL label far
org 0a540h
_TEXT ends
VERDICT_FULL_TEXT segment byte public 'CODE' use16
assume cs:VERDICT_FULL_TEXT
public @verdict_main$qv
org 0255bh
@verdict_main$qv label near
public @verdict_comments_put$qv
org 02c2fh
@verdict_comments_put$qv label near
public @verdict_stage_scores_put$qv
org 02cddh
@verdict_stage_scores_put$qv label near
org 02ddfh
VERDICT_FULL_TEXT ends
STAFF_FULL_TEXT segment byte public 'CODE' use16
STAFF_FULL_TEXT ends
; Complete 4229-byte source-owned Staff family now reaches E3A4 exactly.
; The real bitmap CODE now comes from inline assembly in the C++ unit.
; Compiler emits an empty secondary SEGDEF from the real controller header.
; Declare it before SHARED so it does not extend the CODE group past E801.
STAFF_BITMAP_TEXT segment byte public 'CODE' use16
STAFF_BITMAP_TEXT ends
STAFF_CONTROL_TEXT segment byte public 'CODE' use16
STAFF_CONTROL_TEXT ends
; Actual odd controller RET at E800, next SHARED WORD SEGDEF aligns E801 naturally.
group_01 group VERDICT_FULL_TEXT, STAFF_FULL_TEXT, STAFF_BITMAP_TEXT, STAFF_CONTROL_TEXT
SHARED segment word public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8, VECTOR2_AT, @snd_bgm_measure$qv, @FRAME_DELAY$QI, SND_LOAD, SND_KAJA_INTERRUPT
public @input_reset_sense_held$qv, CDG_LOAD_ALL_NOALPHA, CDG_FREE_ALL
org 00272h
CDG_PUT_NOALPHA_8 label far
org 0049eh
VECTOR2_AT label far
org 00564h
SND_LOAD label far
org 0061ch
SND_KAJA_INTERRUPT label far
org 00a06h
@input_reset_sense_held$qv label far
org 00a40h
@snd_bgm_measure$qv label far
org 00a86h
@FRAME_DELAY$QI label far
org 00b5ah
CDG_LOAD_ALL_NOALPHA label far
org 00bf2h
CDG_FREE_ALL label far
org 0190eh
SHARED ends
_DATA segment word public 'DATA' use16
public _staff_back_page, _staff_spark_cursor, _staff_orb_opening_frame, _staff_camera_accel_phase, _staff_rain_cursor, _staff_rain_frame
public _staff_text_clear_requested, _staff_image_phase_a, _staff_image_phase_b, _staff_image_cover_a, _staff_image_cover_b, _Palettes
public _cdg_slots, _staff_image_wipe_extent_a, _staff_image_wipe_frame_a, _staff_image_wipe_extent_b, _staff_image_wipe_frame_b, _staff_orb_sprite_frame
public _space_window_w, _space_window_h, _staff_spawn_point, _space_window_center, _space_camera_velocity, _staff_particle_decay
public _staff_bgm_measure, _staff_frame, _particles, _orb_trails_center, _stars_center, _PaletteTone
public _verdict_text_left, _verdict_text_color, _verdict_comment_color, _verdict_text_top, _staff_bgm_filename, _staff_cdg_00_filename
public _staff_cdg_01_filename, _staff_cdg_02_filename, _staff_cdg_03_filename, _staff_cdg_04_filename, _staff_cdg_05_filename, _staff_cdg_06_filename
public _staff_cdg_07_filename, _staff_cdg_08_filename, _staff_cdg_09_filename, _staff_cdg_10_filename, _staff_bfnt_01_filename, _staff_bfnt_00_filename
public _key_det, _verdict_bitmap
org 00238h
_PaletteTone label word
org 015e2h
_verdict_text_left label word
org 015e4h
_verdict_text_color label word
org 015e6h
_verdict_comment_color label word
org 015e8h
_verdict_text_top label word
org 0173ah
_staff_back_page label byte
org 0173ch
_staff_spark_cursor label word
org 0173eh
_staff_orb_opening_frame label word
org 01740h
_staff_camera_accel_phase label byte
org 01742h
_staff_rain_cursor label word
org 01744h
_staff_rain_frame label word
org 01746h
_staff_text_clear_requested label byte
org 01748h
_staff_image_phase_a label word
org 0174ah
_staff_image_phase_b label word
org 0174ch
_staff_image_cover_a label byte
org 0174fh
_staff_image_cover_b label byte
org 01752h
_staff_bgm_filename label byte
org 01758h
_staff_cdg_00_filename label byte
org 01762h
_staff_cdg_01_filename label byte
org 0176ch
_staff_cdg_02_filename label byte
org 01776h
_staff_cdg_03_filename label byte
org 01780h
_staff_cdg_04_filename label byte
org 0178ah
_staff_cdg_05_filename label byte
org 01794h
_staff_cdg_06_filename label byte
org 0179eh
_staff_cdg_07_filename label byte
org 017a8h
_staff_cdg_08_filename label byte
org 017b2h
_staff_cdg_09_filename label byte
org 017bch
_staff_cdg_10_filename label byte
org 017c6h
_staff_bfnt_01_filename label byte
org 017d0h
_staff_bfnt_00_filename label byte
org 01d9ah
_Palettes label byte
org 029fah
_key_det label word
org 029feh
_cdg_slots label byte
org 050c4h
_staff_image_wipe_extent_a label word
org 050c6h
_staff_image_wipe_frame_a label word
org 050c8h
_staff_image_wipe_extent_b label word
org 050cah
_staff_image_wipe_frame_b label word
org 050cch
_staff_orb_sprite_frame label byte
org 050ceh
_space_window_w label word
org 050d0h
_space_window_h label word
org 050d2h
_staff_spawn_point label dword
org 050d6h
_space_window_center label dword
org 050dah
_space_camera_velocity label dword
org 050deh
_staff_particle_decay label word
org 050e0h
_staff_bgm_measure label word
org 050e2h
_staff_frame label word
org 050e4h
_particles label byte
org 055f8h
_orb_trails_center label dword
org 05618h
_stars_center label dword
org 056d8h
_verdict_bitmap label byte
org 0c4d8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

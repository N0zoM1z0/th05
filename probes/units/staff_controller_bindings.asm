; Genuine outside providers only. Owned controller [E422,E801) remains CPP.
; E801 is one outside zero; SHARED is truly WORD-aligned at E802.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public GRCG_BYTEBOXFILL_X
org 0c9eh
GRCG_BYTEBOXFILL_X label far
public GRC_SETCLIP
org 0dcch
GRC_SETCLIP label far
public GRCG_SETCOLOR
org 0f28h
GRCG_SETCOLOR label far
public PALETTE_SHOW
org 01b8ah
PALETTE_SHOW label far
public SUPER_FREE
org 02730h
SUPER_FREE label far
public SUPER_ENTRY_BFNT
org 02894h
SUPER_ENTRY_BFNT label far
public SUPER_CONVERT_TINY
org 02d1ah
SUPER_CONVERT_TINY label far
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
SCORE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_TEXT
public @SPACE_WINDOW_SET$QIIII
org 00h
@SPACE_WINDOW_SET$QIIII label near
org 068h
SCORE_TEXT ends
STAFF_LIFE_TEXT segment byte public 'CODE' use16
assume cs:STAFF_LIFE_TEXT
public @staff_particles_init$qv
org 00h
@staff_particles_init$qv label near
public @staff_particles_gather$qv
org 0116h
@staff_particles_gather$qv label near
public @staff_particles_clear$qv
org 0182h
@staff_particles_clear$qv label near
public @staff_particles_scatter$qv
org 01aah
@staff_particles_scatter$qv label near
public @staff_particles_update$qv
org 025ah
@staff_particles_update$qv label near
org 04cch
STAFF_LIFE_TEXT ends
STAFF_TRAIL_TEXT segment byte public 'CODE' use16
assume cs:STAFF_TRAIL_TEXT
public @staff_orb_spark_add$qv
org 00h
@staff_orb_spark_add$qv label near
public @staff_orb_trail_update$qv
org 063h
@staff_orb_trail_update$qv label near
public @staff_orb_particles_age$qv
org 0a2h
@staff_orb_particles_age$qv label near
public @staff_orb_opening_update$qv
org 0deh
@staff_orb_opening_update$qv label near
org 01e3h
STAFF_TRAIL_TEXT ends
STAFF_RAIN_TEXT segment byte public 'CODE' use16
assume cs:STAFF_RAIN_TEXT
public @staff_rain_spawn$qv
org 00h
@staff_rain_spawn$qv label near
public @staff_rain_update$qv
org 0a1h
@staff_rain_update$qv label near
org 01b0h
STAFF_RAIN_TEXT ends
STAFF_WIPE_TEXT segment byte public 'CODE' use16
assume cs:STAFF_WIPE_TEXT
public @STAFF_TEXT_WIPE$QIIIIII
org 00h
@STAFF_TEXT_WIPE$QIIIIII label near
org 011bh
STAFF_WIPE_TEXT ends
STAFF_IMAGE_A_TEXT segment byte public 'CODE' use16
assume cs:STAFF_IMAGE_A_TEXT
public @STAFF_IMAGE_UPDATE_A$QIIII
org 00h
@STAFF_IMAGE_UPDATE_A$QIIII label near
org 0178h
STAFF_IMAGE_A_TEXT ends
STAFF_IMAGE_B_TEXT segment byte public 'CODE' use16
assume cs:STAFF_IMAGE_B_TEXT
public @STAFF_IMAGE_UPDATE_B$QIIII
org 00h
@STAFF_IMAGE_UPDATE_B$QIIII label near
org 0178h
STAFF_IMAGE_B_TEXT ends
STAFF_DRAW_TEXT segment byte public 'CODE' use16
assume cs:STAFF_DRAW_TEXT
public @staff_scene_render$qv
org 00h
@staff_scene_render$qv label near
org 035dh
STAFF_DRAW_TEXT ends
STAFF_FRAME_TEXT segment byte public 'CODE' use16
assume cs:STAFF_FRAME_TEXT
public @staff_frame_advance$qv
org 00h
@staff_frame_advance$qv label near
org 056h
STAFF_FRAME_TEXT ends
STAFF_BITMAP_TEXT segment byte public 'CODE' use16
assume cs:STAFF_BITMAP_TEXT
public @VERDICT_BITMAP_SNAP$QUI
org 00h
@VERDICT_BITMAP_SNAP$QUI label near
public @VERDICT_BITMAP_PUT$QUI
org 02bh
@VERDICT_BITMAP_PUT$QUI label near
org 07eh
STAFF_BITMAP_TEXT ends
STAFF_CONTROL_TEXT segment byte public 'CODE' use16
assume cs:STAFF_CONTROL_TEXT
STAFF_CONTROL_TEXT ends
group_01 group VERDICT_FULL_TEXT, SCORE_TEXT, STAFF_LIFE_TEXT, STAFF_TRAIL_TEXT, STAFF_RAIN_TEXT, STAFF_WIPE_TEXT, STAFF_IMAGE_A_TEXT, STAFF_IMAGE_B_TEXT, STAFF_DRAW_TEXT, STAFF_FRAME_TEXT, STAFF_BITMAP_TEXT, STAFF_CONTROL_TEXT
SHARED segment word public 'CODE' use16
assume cs:SHARED
public SND_LOAD
org 0564h
SND_LOAD label far
public SND_KAJA_INTERRUPT
org 061ch
SND_KAJA_INTERRUPT label far
public @input_reset_sense_held$qv
org 0a06h
@input_reset_sense_held$qv label far
public CDG_LOAD_ALL_NOALPHA
org 0b5ah
CDG_LOAD_ALL_NOALPHA label far
public CDG_FREE_ALL
org 0bf2h
CDG_FREE_ALL label far
org 0190eh
SHARED ends
_DATA segment word public 'DATA' use16
public _PaletteTone
org 0238h
_PaletteTone label word
public _verdict_text_left
org 015e2h
_verdict_text_left label word
public _verdict_text_color
org 015e4h
_verdict_text_color label word
public _verdict_comment_color
org 015e6h
_verdict_comment_color label word
public _verdict_text_top
org 015e8h
_verdict_text_top label word
public _staff_bgm_filename
org 01752h
_staff_bgm_filename label byte
public _staff_cdg_00_filename
org 01758h
_staff_cdg_00_filename label byte
public _staff_cdg_01_filename
org 01762h
_staff_cdg_01_filename label byte
public _staff_cdg_02_filename
org 0176ch
_staff_cdg_02_filename label byte
public _staff_cdg_03_filename
org 01776h
_staff_cdg_03_filename label byte
public _staff_cdg_04_filename
org 01780h
_staff_cdg_04_filename label byte
public _staff_cdg_05_filename
org 0178ah
_staff_cdg_05_filename label byte
public _staff_cdg_06_filename
org 01794h
_staff_cdg_06_filename label byte
public _staff_cdg_07_filename
org 0179eh
_staff_cdg_07_filename label byte
public _staff_cdg_08_filename
org 017a8h
_staff_cdg_08_filename label byte
public _staff_cdg_09_filename
org 017b2h
_staff_cdg_09_filename label byte
public _staff_cdg_10_filename
org 017bch
_staff_cdg_10_filename label byte
public _staff_bfnt_01_filename
org 017c6h
_staff_bfnt_01_filename label byte
public _staff_bfnt_00_filename
org 017d0h
_staff_bfnt_00_filename label byte
public _Palettes
org 01d9ah
_Palettes label byte
public _key_det
org 029fah
_key_det label word
public _staff_bgm_measure
org 050e0h
_staff_bgm_measure label word
public _staff_frame
org 050e2h
_staff_frame label word
org 0c4d8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

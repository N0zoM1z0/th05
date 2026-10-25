; Only true foreign code/state labels and outside extents; no helper bodies.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public TEXT_PUTSA
org 022aah
TEXT_PUTSA label far
org 0a540h
_TEXT ends
STAFF_WIPE_TEXT segment byte public 'CODE' use16
assume cs:STAFF_WIPE_TEXT
public @STAFF_TEXT_WIPE$QIIIIII
org (0dbe6h - 0a540h)
@STAFF_TEXT_WIPE$QIIIIII label near
org (0dd01h - 0a540h)
STAFF_WIPE_TEXT ends
STAFF_IMAGE_A_TEXT segment byte public 'CODE' use16
STAFF_IMAGE_A_TEXT ends
STAFF_IMAGE_A_TAIL segment byte public 'CODE' use16
org (0e800h - 0de79h)
STAFF_IMAGE_A_TAIL ends
group_01 group STAFF_WIPE_TEXT, STAFF_IMAGE_A_TEXT, STAFF_IMAGE_A_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8
org 0274h
CDG_PUT_NOALPHA_8 label far
org (10110h - 0e800h)
SHARED ends
_DATA segment word public 'DATA' use16
public _staff_text_clear_requested
org 01746h
_staff_text_clear_requested label byte
public _staff_image_phase_a
org 01748h
_staff_image_phase_a label word
public _staff_image_cover_a
org 0174ch
_staff_image_cover_a label byte
public _cdg_slots
org 029feh
_cdg_slots label byte
public _staff_image_wipe_extent_a, _staff_image_wipe_frame_a
org 050c4h
_staff_image_wipe_extent_a label word
org 050c6h
_staff_image_wipe_frame_a label word
public _staff_bgm_measure
org 050e0h
_staff_bgm_measure label word
org 0c4d8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Real foreign code/data identities only; no own-function instructions or bytes.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public TEXT_PUTSA
org 022AAh
TEXT_PUTSA label far
org 0A540h
_TEXT ends
STAFF_WIPE_TEXT segment byte public 'CODE' use16
assume cs:STAFF_WIPE_TEXT
public @STAFF_TEXT_WIPE$QIIIIII
org (0DBE6h - 0A540h)
@STAFF_TEXT_WIPE$QIIIIII label near
org (0DD01h - 0A540h)
STAFF_WIPE_TEXT ends
STAFF_IMAGE_A_TEXT segment byte public 'CODE' use16
assume cs:STAFF_IMAGE_A_TEXT
public @STAFF_IMAGE_UPDATE_A$QIIII
@STAFF_IMAGE_UPDATE_A$QIIII label near
org (0DE79h - 0DD01h)
STAFF_IMAGE_A_TEXT ends
STAFF_IMAGE_B_TEXT segment byte public 'CODE' use16
STAFF_IMAGE_B_TEXT ends
STAFF_IMAGE_B_TAIL segment byte public 'CODE' use16
org (0E800h - 0DFF1h)
STAFF_IMAGE_B_TAIL ends
group_01 group STAFF_WIPE_TEXT, STAFF_IMAGE_A_TEXT, STAFF_IMAGE_B_TEXT, STAFF_IMAGE_B_TAIL
SHARED segment para public 'CODE' use16
assume cs:SHARED
public CDG_PUT_NOALPHA_8
org 0274h
CDG_PUT_NOALPHA_8 label far
org 01910h
SHARED ends
_DATA segment word public 'DATA' use16
public _staff_text_clear_requested
org 01746h
_staff_text_clear_requested label byte
public _staff_image_phase_b
org 0174Ah
_staff_image_phase_b label word
public _staff_image_cover_b
org 0174Fh
_staff_image_cover_b label byte
public _cdg_slots
org 029FEh
_cdg_slots label byte
public _staff_image_wipe_extent_b
org 050C8h
_staff_image_wipe_extent_b label word
public _staff_image_wipe_frame_b
org 050CAh
_staff_image_wipe_frame_b label word
public _staff_bgm_measure
org 050E0h
_staff_bgm_measure label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

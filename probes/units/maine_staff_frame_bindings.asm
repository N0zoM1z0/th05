; Only original provider symbols and holes outside the complete86-byte CODE.
.386
.model large
GROUP01_BASE equ 0A540h
UNIT_START equ 0E34Eh
UNIT_SIZE equ 056h
UNIT_END equ (UNIT_START + UNIT_SIZE)
SHARED_BASE equ 0E800h
DGROUP_BASE equ 10110h

_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public TEXT_CLEAR
org 02298h
TEXT_CLEAR label far
org GROUP01_BASE
_TEXT ends

SCORE_TEXT segment byte public 'CODE' use16
org (0D387h - GROUP01_BASE)
SCORE_TEXT ends

STAFF_LIFE_TEXT segment byte public 'CODE' use16
assume cs:STAFF_LIFE_TEXT
public @staff_particles_update$qv
org (0D5E1h - 0D387h)
@staff_particles_update$qv label near
org (0D853h - 0D387h)
STAFF_LIFE_TEXT ends

STAFF_TRAIL_TEXT segment byte public 'CODE' use16
org (0DFF1h - 0D853h)
STAFF_TRAIL_TEXT ends

STAFF_DRAW_TEXT segment byte public 'CODE' use16
assume cs:STAFF_DRAW_TEXT
public @staff_scene_render$qv
@staff_scene_render$qv label near
org (UNIT_START - 0DFF1h)
STAFF_DRAW_TEXT ends

STAFF_FRAME_TEXT segment byte public 'CODE' use16
STAFF_FRAME_TEXT ends
STAFF_FRAME_TAIL segment byte public 'CODE' use16
org (SHARED_BASE - UNIT_END)
STAFF_FRAME_TAIL ends
group_01 group SCORE_TEXT, STAFF_LIFE_TEXT, STAFF_TRAIL_TEXT, STAFF_DRAW_TEXT, STAFF_FRAME_TEXT, STAFF_FRAME_TAIL

SHARED segment para public 'CODE' use16
assume cs:SHARED
public @snd_bgm_measure$qv
org 0A42h
@snd_bgm_measure$qv label far
public @FRAME_DELAY$QI
org 0A88h
@FRAME_DELAY$QI label far
org (DGROUP_BASE - SHARED_BASE)
SHARED ends

_DATA segment word public 'DATA' use16
public _staff_back_page
org 0173Ah
_staff_back_page label byte
public _staff_text_clear_requested
org 01746h
_staff_text_clear_requested label byte
public _staff_bgm_measure
org 050E0h
_staff_bgm_measure label word
public _staff_frame
org 050E2h
_staff_frame label word
org 0C4D8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

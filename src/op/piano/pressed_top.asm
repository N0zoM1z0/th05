; Twelve note-top masks in the black-key band of the PC-98 Music Room.
; Original note geometry preserved in ReC98 th05/op/piano_a.asm.
.386
.model large
locals

PIANO_TOP_PLANE_SHIFT equ 5
PIANO_SHARP_OR_OUTER equ 110b
PIANO_CENTER_WHITE equ 010b
PIANO_RIGHT_WHITE_EDGE equ 011b

SHARED segment byte public 'CODE' use16
assume cs:SHARED
public PIANO_KEY_PRESSED_TOP, piano_pressed_top_end
PIANO_KEY_PRESSED_TOP label byte
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; C
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; C sharp
    db (PIANO_CENTER_WHITE shl PIANO_TOP_PLANE_SHIFT) ; D
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; D sharp
    db (PIANO_RIGHT_WHITE_EDGE shl PIANO_TOP_PLANE_SHIFT) ; E
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; F
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; F sharp
    db (PIANO_CENTER_WHITE shl PIANO_TOP_PLANE_SHIFT) ; G
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; G sharp
    db (PIANO_CENTER_WHITE shl PIANO_TOP_PLANE_SHIFT) ; A
    db (PIANO_SHARP_OR_OUTER shl PIANO_TOP_PLANE_SHIFT) ; A sharp
    db (PIANO_RIGHT_WHITE_EDGE shl PIANO_TOP_PLANE_SHIFT) ; B
piano_pressed_top_end label byte
SHARED ends
end

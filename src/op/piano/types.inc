; Full external eight-byte note state; opaque driver pointers are not narrowed.
piano_notes_t struc
 fm db 5 dup (?)
 unused db 3 dup (?)
piano_notes_t ends
ONKAI_REST equ -1
ONKAI_NOTE_MASK equ 0Fh
ROW_SIZE equ (640/8)
BYTE_DOTS equ 8

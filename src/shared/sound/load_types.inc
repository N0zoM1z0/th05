; Complete word API domains and actual byte modes; no sound/file DATA payload.
SOUND_FILENAME_BYTES equ 13
SND_LOAD_SONG equ 0600h
SND_LOAD_SE equ 0B00h
SND_BGM_OFF equ 0
SND_BGM_FM26 equ 1
SND_BGM_FM86 equ 2
SND_BGM_MIDI equ 3
SND_BGM_MODE_COUNT equ 3 ; MIDI remains the original unsupported value3
SND_SE_OFF equ 0
SND_SE_FM equ 1
SND_SE_BEEP equ 2
SND_SE_MODE_COUNT equ 3
KAJA_SONG_STOP equ 1
KAJA_GET_SONG_ADDRESS equ 6
PMD_INTERRUPT equ 60h
MMD_INTERRUPT equ 61h
DOS_INTERRUPT equ 21h
DOS_OPEN_READ equ 3D00h
DOS_READ equ 3F00h
DOS_CLOSE equ 3Eh
DOS_FILE_NOT_FOUND equ 2
; Packed extension bank is15 bytes, followed by a distinct foreign SE-mode byte.
sound_extension_bank_t struc
 effect db 4 dup (?)
 fm26 db 4 dup (?)
 fm86 db 4 dup (?)
 midi db 3 dup (?)
sound_extension_bank_t ends

; Eight displayed score digits, or a right-aligned five-digit integer.
HUD_SCORE_DIGITS equ 8
HUD_SMALL_DIGITS equ 5
HUD_SCORE_DIVISOR_INDEX equ 2
HUD_DIVISOR_BYTES equ 4
HUD_DIGIT_ZERO equ 0a0h
HUD_NUMBER_EMPTY equ 2
HUD_WHITE equ 0e1h
; Both far Pascal APIs consume eight argument bytes after saved BP and RETF.
HUD_NUMBER_ARG_ATTRIBUTE equ 6
HUD_NUMBER_ARG_VALUE equ 8
HUD_POINTS_ARG_VALUE equ 6
HUD_NUMBER_ARG_ROW equ 10
HUD_NUMBER_ARG_LEFT equ 12
HUD_NUMBER_ARGUMENT_BYTES equ 8

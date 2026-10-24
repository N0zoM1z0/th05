; Symbol-only context for the complete 2134-byte Marisa shot-control producer.
; No external implementation, instructions or target payload bytes are emitted.
; The original main_01 frame is 0AE1 and the source begins at offset 3D82.
.386
.model large
.stack 80h

MASTER_TEXT_END equ 0ae10h
UNIT_START equ 0eb92h

_TEXT segment word public 'CODE' use16
org MASTER_TEXT_END
_TEXT ends

MAIN_01_TEXT segment word public 'CODE' use16
assume cs:MAIN_01_TEXT
public @RANDRING1_NEXT16_AND$QUI
public @shots_add$qv, @SHOT_VELOCITY_SET$QP7SPPOINTUC, @shot_cycle_init$qv
org (0c70eh - MASTER_TEXT_END)
@RANDRING1_NEXT16_AND$QUI label near
org (0e38ch - MASTER_TEXT_END)
@shots_add$qv label near
org (0e3c4h - MASTER_TEXT_END)
@SHOT_VELOCITY_SET$QP7SPPOINTUC label near
org (0e644h - MASTER_TEXT_END)
@shot_cycle_init$qv label near
org (UNIT_START - MASTER_TEXT_END)
MAIN_01_TEXT ends
main_01 group MAIN_01_TEXT
end

; Semantic candidate from pinned ReC98 b6ba5b0a th04/hardware/input_s.asm.
; The reset entry deliberately falls through into the shared FAR sense body.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

OR_INPUT_LOW macro value
 or byte ptr _key_det, low value
endm
OR_INPUT_HIGH macro value
 or byte ptr _key_det+1, high value
endm

.code SHARED
public @input_reset_sense$qv
@input_reset_sense$qv label far
 xor ax, ax
 mov _key_det, ax
 mov js_stat, ax

public @input_sense$qv
@input_sense$qv proc far
 ; Firmware key state is read in ES=0; DS remains the game's data segment.
 xor ax, ax
 mov es, ax
 mov ah, byte ptr es:[KEYGROUP_7]
 test ah, K7_ARROW_UP
 jz short @@down
 OR_INPUT_LOW INPUT_UP
@@down:
 test ah, K7_ARROW_DOWN
 jz short @@left
 OR_INPUT_LOW INPUT_DOWN
@@left:
 test ah, K7_ARROW_LEFT
 jz short @@right
 OR_INPUT_LOW INPUT_LEFT
@@right:
 test ah, K7_ARROW_RIGHT
 jz short @@num6
 OR_INPUT_LOW INPUT_RIGHT
@@num6:
 mov ah, byte ptr es:[KEYGROUP_9]
 test ah, K9_NUM_6
 jz short @@num1
 OR_INPUT_LOW INPUT_RIGHT
@@num1:
 test ah, K9_NUM_1
 jz short @@num2
 OR_INPUT_HIGH INPUT_DOWN_LEFT
@@num2:
 test ah, K9_NUM_2
 jz short @@num3
 OR_INPUT_LOW INPUT_DOWN
@@num3:
 test ah, K9_NUM_3
 jz short @@num4
 OR_INPUT_HIGH INPUT_DOWN_RIGHT
@@num4:
 mov ah, byte ptr es:[KEYGROUP_8]
 test ah, K8_NUM_4
 jz short @@num7
 OR_INPUT_LOW INPUT_LEFT
@@num7:
 test ah, K8_NUM_7
 jz short @@num8
 OR_INPUT_HIGH INPUT_UP_LEFT
@@num8:
 test ah, K8_NUM_8
 jz short @@num9
 OR_INPUT_LOW INPUT_UP
@@num9:
 test ah, K8_NUM_9
 jz short @@z
 OR_INPUT_HIGH INPUT_UP_RIGHT
@@z:
 mov ah, byte ptr es:[KEYGROUP_5]
 test ah, K5_Z
 jz short @@x
 OR_INPUT_LOW INPUT_SHOT
@@x:
 test ah, K5_X
 jz short @@q
 OR_INPUT_LOW INPUT_BOMB
@@q:
 mov ah, byte ptr es:[KEYGROUP_2]
 test ah, K2_Q
 jz short @@escape
 OR_INPUT_HIGH INPUT_Q
@@escape:
 mov ah, byte ptr es:[KEYGROUP_0]
 test ah, K0_ESC
 jz short @@enter
 OR_INPUT_HIGH INPUT_CANCEL
@@enter:
 mov ah, byte ptr es:[KEYGROUP_3]
 test ah, K3_RETURN
 jz short @@space
 OR_INPUT_HIGH INPUT_OK
@@space:
 mov ah, byte ptr es:[KEYGROUP_6]
 test ah, K6_SPACE
 jz short @@shift
 OR_INPUT_LOW INPUT_SHOT
@@shift:
 ; BIOS AH=2 returns shift state in AL. Keep only the Shift bit.
 mov ah, 2
 int 18h
 and al, 1
 mov _shiftkey, al
 cmp js_bexist, 0
 jz short @@ret
 call JS_SENSE
 or _key_det, ax
@@ret:
 mov ax, _key_det
 retf
@input_sense$qv endp
; Real word alignment after the common RETF; zero authored credit.
even
public input_sense_end
input_sense_end label byte
end

; Original far-Pascal 64-slot random Spark spawning state machine.
; Source-backed by ReC98 th04/main/spark_a.asm SPARKS_ADD_RANDOM; the
; historical 16-bit TASM register flow is intentional, not copied opcodes.
; Far args: [BP+6] count, [BP+8] minimum radial speed,
; [BP+10] center Y and [BP+12] center X.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group SPARK_RANDOM_TEXT
SPARK_RANDOM_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public SPARKS_ADD_RANDOM
SPARKS_ADD_RANDOM proc far
    push bp
    mov bp, sp
    cmp word ptr [bp+12], SPARK_PLAYFIELD_X_MAX
    ja short @@ret
    cmp word ptr [bp+10], SPARK_PLAYFIELD_Y_MAX
    ja short @@ret
    push si
    push di
    mov di, word ptr [bp+6]
@@next_spark:
    mov si, _spark_ring_offset
    add si, offset _sparks
    cmp byte ptr [si+SPARK_FLAG_AND_AGE], SPARK_FREE
    jne short @@advance_ring
    mov word ptr [si+SPARK_FLAG_AND_AGE], SPARK_ALIVE
    mov ax, word ptr [bp+12]
    mov word ptr [si+SPARK_POSITION_X], ax
    mov ax, word ptr [bp+10]
    mov word ptr [si+SPARK_POSITION_Y], ax
    push SPARK_RANDOM_SPEED_SPAN_MASK
    call @RANDRING2_NEXT16_AND$QUI
    add ax, word ptr [bp+8]
    lea bx, [si+SPARK_VELOCITY]
    push bx
    push word ptr [si+SPARK_ANGLE]
    push ax
    call VECTOR2_NEAR
@@advance_ring:
    add _spark_ring_offset, SPARK_RECORD_BYTES
    cmp _spark_ring_offset, SPARK_RING_BYTES
    jb short @@slot_available
    mov _spark_ring_offset, 0
@@slot_available:
    dec di
    jne short @@next_spark
    pop di
    pop si
@@ret:
    pop bp
    retf 8
SPARKS_ADD_RANDOM endp
public sparks_add_random_end
sparks_add_random_end label byte
SPARK_RANDOM_TEXT ends
end

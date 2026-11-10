; Full original near-Pascal 64-slot radial spark generation state machine.
; Preserved semantic source: ReC98 th04/main/spark_a.asm, circle procedure.
; Arguments [BP+4] count, [BP+6] radius, [BP+8] Y, [BP+10] X.
.386
.model large
locals
include types.inc
include symbols.inc

main_03 group SPARK_CIRCLE_TEXT
SPARK_CIRCLE_TEXT segment byte public 'CODE' use16
assume cs:main_03, ds:DGROUP
public SPARKS_ADD_CIRCLE
SPARKS_ADD_CIRCLE proc near
    push bp
    mov bp, sp
    cmp word ptr [bp+10], SPARK_PLAYFIELD_X_MAX
    ja short @@ret
    cmp word ptr [bp+8], SPARK_PLAYFIELD_Y_MAX
    ja short @@ret
    push si
    push di
    mov di, word ptr [bp+4]
    shl di, 8
@@next_spark:
    mov si, _spark_ring_offset
    add si, offset _sparks
    cmp byte ptr [si+SPARK_FLAG_AND_AGE], SPARK_FREE
    jne short @@advance_ring
    mov word ptr [si+SPARK_FLAG_AND_AGE], SPARK_ALIVE
    mov ax, word ptr [bp+10]
    mov word ptr [si+SPARK_POSITION_X], ax
    mov ax, word ptr [bp+8]
    mov word ptr [si+SPARK_POSITION_Y], ax
    lea ax, [si+SPARK_VELOCITY]
    push ax
    xor dx, dx
    mov ax, di
    div word ptr [bp+4]
    xor ah, ah
    push ax
    push word ptr [bp+6]
    call VECTOR2_NEAR
@@advance_ring:
    add _spark_ring_offset, SPARK_RECORD_BYTES
    cmp _spark_ring_offset, SPARK_RING_BYTES
    jb short @@slot_available
    mov _spark_ring_offset, 0
@@slot_available:
    sub di, SPARK_COMPLETE_ANGLE
    jne short @@next_spark
    pop di
    pop si
@@ret:
    pop bp
    ret 8
SPARKS_ADD_CIRCLE endp
    even
public sparks_add_circle_end
sparks_add_circle_end label byte
SPARK_CIRCLE_TEXT ends
end

; TH05 spark lifecycle: skip free, clear removed, update motion, clip/expire.
; Source expresses the original active-pool algorithm and real DX:AX return;
; it does not own any spark records or draw routines.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group SPARK_UPDATE_TEXT
SPARK_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public _sparks_update
_sparks_update proc near
    push si
    push di
    mov di, SPARK_ACTIVE_COUNT
    mov si, offset _sparks
@@next:
    cmp byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_FREE
    je short @@advance
    cmp byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_ALIVE
    je short @@move
    mov byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_FREE
    jmp short @@advance
@@move:
    lea ax, [si + SPARK_CENTER_OFFSET]
    push ax
    call @PlayfieldMotion@update_seg1$qv
    add ax, ((SPARK_WIDTH_PIXELS / 2) * SPARK_SUBPIXELS_PER_DOT)
    cmp ax, ((PLAYFIELD_WIDTH_PIXELS + SPARK_WIDTH_PIXELS) * SPARK_SUBPIXELS_PER_DOT)
    jae short @@remove
    add dx, ((SPARK_HEIGHT_PIXELS / 2) * SPARK_SUBPIXELS_PER_DOT)
    cmp dx, ((PLAYFIELD_HEIGHT_PIXELS + SPARK_HEIGHT_PIXELS) * SPARK_SUBPIXELS_PER_DOT)
    jb short @@age
@@remove:
    mov byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_REMOVE
    jmp short @@advance
@@age:
    inc word ptr [si + SPARK_VELOCITY_Y_OFFSET]
    inc byte ptr [si + SPARK_AGE_OFFSET]
    cmp byte ptr [si + SPARK_AGE_OFFSET], SPARK_MAX_AGE
    jbe short @@advance
    mov byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_REMOVE
@@advance:
    add si, SPARK_RECORD_SIZE
    dec di
    jg short @@next
    pop di
    pop si
    ret
_sparks_update endp
public sparks_update_end
sparks_update_end label byte
SPARK_UPDATE_TEXT ends
end

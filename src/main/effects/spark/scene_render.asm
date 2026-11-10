; Render the active 64 spark records to the genuine PC-98 blue VRAM plane.
; Semantic hardware/geometry reconstruction, no embedded game pixels or state.
.386
.model large
locals
include types.inc
include symbols.inc
SPARK_RENDER_COLOR equ 12
SPARK_RENDER_PLANE equ 0A800h
SPARK_RENDER_LEFT equ 32
SPARK_RENDER_TOP equ 16

main_01 group SPARK_SCENE_RENDER_TEXT
SPARK_SCENE_RENDER_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public _sparks_render
_sparks_render proc near
    push si
    push di
    mov ah, SPARK_RENDER_COLOR
    call @grcg_setcolor_direct_raw$qv
    mov ax, SPARK_RENDER_PLANE
    mov es, ax
    mov di, SPARK_ACTIVE_COUNT
    mov si, offset _sparks
@@next:
    cmp byte ptr [si + SPARK_FLAG_OFFSET], SPARK_FLAG_ALIVE
    jne short @@advance
    mov ax, [si + SPARK_CENTER_OFFSET + 2]
    add ax, ((SPARK_RENDER_TOP - (SPARK_HEIGHT_PIXELS / 2)) * SPARK_SUBPIXELS_PER_DOT)
    push ax
    call SCROLL_SUBPIXEL_Y_TO_VRAM_SEG1
    mov dx, ax
    mov ax, [si + SPARK_CENTER_OFFSET]
    add ax, ((SPARK_RENDER_LEFT - (SPARK_WIDTH_PIXELS / 2)) * SPARK_SUBPIXELS_PER_DOT)
    sar ax, 4
    mov cl, [si + SPARK_AGE_OFFSET]
    call @spark_render
@@advance:
    add si, SPARK_RECORD_SIZE
    dec di
    jg short @@next
    pop di
    pop si
    ret
_sparks_render endp
    even
public sparks_scene_render_end
sparks_scene_render_end label byte
SPARK_SCENE_RENDER_TEXT ends
end

; Original near-register Louise backdrop fill callback (stage 2).
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group LOUISE_BACKDROP_TEXT
LOUISE_BACKDROP_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @louise_backdrop_colorfill$qv, louise_backdrop_fill_end
@louise_backdrop_colorfill$qv proc near
    push di
    mov ax, LOUISE_VRAM_WINDOW_SEG
    mov es, ax
    mov di, LOUISE_BOTTOM_ROW_LEFT
    call grcg_fill_playfield_rows
    pop di
    ret
@louise_backdrop_colorfill$qv endp
louise_backdrop_fill_end label byte
LOUISE_BACKDROP_TEXT ends
end

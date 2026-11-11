; Early Boss stage backdrops: Sara dark bands and Mai/Yuki GRCG fill ribbons.
; Original near-register drawing interfaces, no bitmap data owned.
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group BOSS_BD_EARLY_TEXT
BOSS_BD_EARLY_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @sara_backdrop_colorfill$qv
public @mai_yuki_backdrop_colorfill$qv
public boss_backdrop_early_end

@sara_backdrop_colorfill$qv proc near
    push di
    cli
    mov dx, GRCG_TILE_PORT
    xor al, al
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    sti
    mov dx, SARA_VRAM_TOP_SEG
    mov es, dx
    mov di, SARA_UPPER_LAST_ROW
    call grcg_fill_playfield_rows
    mov ax, SHARED_VRAM_SEG
    mov es, ax
    mov di, SARA_LOWER_LAST_ROW
@@side_strip:
    mov es:[di], eax
    mov es:[di+SARA_SIDE_GAP], eax
    sub di, VRAM_ROW_BYTES
    jge short @@side_strip
    pop di
    ret
@sara_backdrop_colorfill$qv endp
    even

@mai_yuki_backdrop_colorfill$qv proc near
    push di
    mov ax, SHARED_VRAM_SEG
    mov es, ax
    mov di, MAI_YUKI_UPPER_LEFT
    even
@@upper_band:
    mov cx, UPPER_RUN_DWORDS
@@upper_run:
    mov es:[di+MAI_YUKI_UPPER_SIDE_DELTA], eax
    stosd
    loop @@upper_run
    sub di, UPPER_STRIDE_BYTES
    jge short @@upper_band
    mov ax, MAI_YUKI_VRAM_LOWER_SEG
    mov es, ax
    mov di, MAI_YUKI_LOWER_LEFT
    even
@@lower_band:
    mov es:[di+MAI_YUKI_LOWER_SIDE_DELTA], eax
    stosd
    mov es:[di+MAI_YUKI_LOWER_SIDE_DELTA], eax
    stosd
    sub di, LOWER_STRIDE_BYTES
    jge short @@lower_band
    pop di
    ret
@mai_yuki_backdrop_colorfill$qv endp
    even
boss_backdrop_early_end label byte
BOSS_BD_EARLY_TEXT ends
end

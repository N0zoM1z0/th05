; Shinki stage/TBW backdrop fills, real GRCG port and ES:DI interfaces.
; The separately reconstructed row painter is kept as a foreign near provider.
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group SHINKI_BD_FILL_TEXT
SHINKI_BD_FILL_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @shinki_stage_backdrop_colorfill$qv
public @boss_bg_fill_col_0$qv
public @shinki_bg_type_d_colorfill$qv
public shinki_backdrop_fill_end

@shinki_stage_backdrop_colorfill$qv proc near
    push di
    mov ax, VRAM_UPPER_PLAYFIELD
    mov es, ax
    mov di, STAGE_FIRST_BOTTOM_LEFT
    call grcg_fill_playfield_rows
    mov ax, VRAM_LOWER_PLAYFIELD
    mov es, ax
    mov di, STAGE_SECOND_BOTTOM_LEFT
    call grcg_fill_playfield_rows
    pop di
    ret
@shinki_stage_backdrop_colorfill$qv endp
    even

@boss_bg_fill_col_0$qv proc near
    pushf
    cli
    mov al, GRCG_TILE_DIRECT
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    xor al, al
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    popf
    push di
    mov ax, VRAM_UPPER_PLAYFIELD
    mov es, ax
    mov di, FILL_BG_COLUMN_BOTTOM_LEFT
    call grcg_fill_playfield_rows
    xor al, al
    out GRCG_MODE_PORT, al
    pop di
    ret
@boss_bg_fill_col_0$qv endp

@shinki_bg_type_d_colorfill$qv proc near
    pushf
    cli
    mov al, GRCG_TILE_DIRECT
    out GRCG_MODE_PORT, al
    mov dx, GRCG_TILE_PORT
    xor al, al
    out dx, al
    out dx, al
    out dx, al
    out dx, al
    popf
    push di
    mov ax, VRAM_UPPER_PLAYFIELD
    mov es, ax
    mov di, TYPE_D_BOTTOM_LEFT
    call grcg_fill_playfield_rows
    xor al, al
    out GRCG_MODE_PORT, al
    pop di
    ret
@shinki_bg_type_d_colorfill$qv endp
shinki_backdrop_fill_end label byte
SHINKI_BD_FILL_TEXT ends
end

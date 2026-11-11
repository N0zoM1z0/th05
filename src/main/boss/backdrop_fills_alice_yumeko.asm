; Alice/Yumeko stage backdrop near draw callbacks, original ES:DI protocol.
.386
.model large
locals
include types.inc
include symbols.inc
main_01 group BOSS_BD_AY_TEXT
BOSS_BD_AY_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @alice_backdrop_colorfill$qv, @yumeko_backdrop_colorfill$qv
public boss_backdrop_ay_end

@alice_backdrop_colorfill$qv proc near
    push di
    mov ax, ALICE_VRAM_SEG
    mov es, ax
    mov di, ALICE_LAST_ROW_LEFT
    call grcg_fill_playfield_rows
    pop di
    ret
@alice_backdrop_colorfill$qv endp

@yumeko_backdrop_colorfill$qv proc near
    push di
    mov ax, YUMEKO_VRAM_SEG
    mov es, ax
    mov di, YUMEKO_LAST_ROW_LEFT
    call grcg_fill_playfield_rows
    pop di
    ret
@yumeko_backdrop_colorfill$qv endp
boss_backdrop_ay_end label byte
BOSS_BD_AY_TEXT ends
end

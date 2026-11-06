; Private Mima backdrop worker. ES is the caller-selected band origin.
; EAX is the caller's store value; GRCG TDW ignores it and supplies the color.
; DI/CX/flags are deliberately clobbered, with DF assumed clear as originally.
.386
.model large
include types.inc
include symbols.inc

BAND_WIDTH_PIXELS equ 176
BAND_WIDTH_BYTES equ (BAND_WIDTH_PIXELS / 8)
BAND_DWORDS equ ((BAND_WIDTH_BYTES - WORD_BYTES) / DWORD_BYTES)
BAND_ROW_BACKSTEP equ (VRAM_ROW_BYTES + (BAND_DWORDS * DWORD_BYTES))

main_01 group MIMA_BANDS_TEXT
MIMA_BANDS_TEXT segment byte public 'CODE' use16
assume cs:main_01, es:nothing
public mima_bomb_bands_fill, mima_bomb_bands_end
mima_bomb_bands_fill proc near
 mov di, ((BAND_LAST_ROW * VRAM_ROW_BYTES) + (BAND_LEFT_X / 8))
@@left_row:
 mov cx, BAND_DWORDS
 rep stosd
 mov es:[di], ax
 sub di, BAND_ROW_BACKSTEP
 jge short @@left_row

 mov di, ((BAND_LAST_ROW * VRAM_ROW_BYTES) + (BAND_RIGHT_X / 8))
@@right_row:
 mov cx, BAND_DWORDS
 rep stosd
 mov es:[di], ax
 sub di, BAND_ROW_BACKSTEP
 jge short @@right_row
 ret
mima_bomb_bands_fill endp
mima_bomb_bands_end label byte
MIMA_BANDS_TEXT ends
end

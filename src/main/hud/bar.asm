; Eight-cell HUD bar, from reviewed native ASM and the ReC98 semantic donor.
; Near Pascal (row, int value, attribute); only the low value byte is read.
.386
.model large
locals
include types.inc
include symbols.inc

HUD_BAR_CAPACITY equ (HUD_BAR_CELLS * HUD_BAR_CELL_UNITS)

MAIN_01_TEXT segment word public 'CODE' use16
assume cs:MAIN_01_TEXT, ds:DGROUP
public HUD_BAR_PUT
HUD_BAR_PUT proc near
 ; Capture the incoming argument frame before saving the destination cursor.
 mov bx, sp
 push di
 push ds
 pop es
 mov di, offset _hud_gaiji_row
 ; Queue the real far string-renderer arguments before BL becomes the value.
 push HUD_COLUMN
 push word ptr ss:[bx+HUD_BAR_ARG_ROW]
 push ds
 push di
 push word ptr ss:[bx+HUD_BAR_ARG_ATTRIBUTE]
 mov al, HUD_BAR_FULL_FIRST
 mov cx, HUD_BAR_CELLS
 mov bl, ss:[bx+HUD_BAR_ARG_VALUE]
 cmp bl, HUD_BAR_CAPACITY
 jb short @@partial

 ; Saturation uses the eight distinct full-bar glyphs in screen order.
@@full_cell:
 stosb
 inc al
 loop @@full_cell
 jmp short @@put

@@partial:
 mov dl, bl
 dec al
 jmp short @@test_cell
@@filled_cell:
 stosb
@@test_cell:
 dec cx
 sub dl, HUD_BAR_CELL_UNITS
 jg short @@filled_cell
 ; Preserve the original zero-value wrap to a full first cell.
 mov al, bl
 dec al
 and al, (HUD_BAR_CELL_UNITS - 1)
 add al, HUD_BAR_PARTIAL_FIRST
 stosb
 mov al, HUD_EMPTY
 rep stosb

@@put:
 call GAIJI_PUTSA
 pop di
 ret HUD_BAR_ARGUMENT_BYTES
HUD_BAR_PUT endp
public hud_bar_end
hud_bar_end label byte
MAIN_01_TEXT ends
end

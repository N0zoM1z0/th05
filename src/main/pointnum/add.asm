; Two public ring-buffer entries share the allocation and Pascal return path.
.386
.model large
locals
include types.inc
include symbols.inc
POINTNUM_WHITE_LAST equ (POINTNUM_WHITE_COUNT - 1)
main_03 group MAIN_03_TEXT
MAIN_03_TEXT segment word public 'CODE' use16
assume cs:main_03, ds:DGROUP
public @pointnums_add_yellow$qiiui, @pointnums_add_white$qiiui
pointnums_add proc near
@@number equ word ptr [bp+4]
@@center_y equ word ptr [bp+6]
@@center_x equ word ptr [bp+8]
@pointnums_add_yellow$qiiui:
 mov bl, _pointnum_yellow_p
 inc _pointnum_yellow_p
 cmp bl, (POINTNUM_YELLOW_COUNT - 1)
 jb short @@yellow_index
 mov _pointnum_yellow_p, 0
@@yellow_index:
 xor bh, bh
 add bx, POINTNUM_WHITE_COUNT
 jmp short @@allocate
@pointnums_add_white$qiiui:
 mov bl, _pointnum_white_p
 mov bh, 0
 inc _pointnum_white_p
 cmp bl, POINTNUM_WHITE_LAST
 jb short @@allocate
 mov _pointnum_white_p, 0
@@allocate:
 shl bx, 4
 add bx, offset _pointnums
 ; Adjacent byte fields: alive flag and a newly reset age.
 mov word ptr [bx+pointnum_t.PN_flag], 1
 push bp
 mov bp, sp
 mov ax, @@center_x
 mov [bx+pointnum_t.PN_center_x], ax
 mov ax, @@center_y
 mov [bx+pointnum_t.PN_center_y], ax
 push si
 mov si, bx
 lea ax, [bx+pointnum_t.PN_digits + (POINTNUM_DIGITS - 1)]
 push ax
 push @@number
 call POINTNUM_DIGITS_SET
 mov [si+pointnum_t.PN_width], ax
 pop si
 pop bp
 ret 6
pointnums_add endp
 even
public pointnums_add_end
pointnums_add_end label byte
MAIN_03_TEXT ends
end

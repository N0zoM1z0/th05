; TH05 ZUN.COM -G: register-level PC-98 CG-RAM gaiji installer.
; Glyph pixels are NOT in this maintained source; the separate pinned
; bitmap resource is expanded by the focused native replay.
.8086
.model tiny
.code
org 100h

DOS_INT equ 021h
DOS_PRINT equ 009h
DOS_EXIT equ 04C00h
PC98_CGRAM_CONTROL equ 068h
PC98_CGRAM_CODE_LO equ 0A1h
PC98_CGRAM_CODE_HI equ 0A3h
PC98_CGRAM_PLANE equ 0A5h
PC98_CGRAM_WRITE equ 0A9h
FONT_GLYPH_BASE equ 05680h
FONT_GLYPH_COUNT equ 256
FONT_ROWS_PER_GLYPH equ 16
FONT_UPPER_HALF equ 020h

public GAIJI_INSTALL_START
GAIJI_INSTALL_START proc near
    mov dx, offset install_banner
    mov ah, DOS_PRINT
    int DOS_INT
    mov si, offset private_gaiji_pixels
    mov al, 0Bh
    out PC98_CGRAM_CONTROL, al
    xor dx, dx
@@glyph_loop:
    mov ax, dx
    add ax, FONT_GLYPH_BASE
    and al, 07Fh
    out PC98_CGRAM_CODE_LO, al
    mov al, ah
    out PC98_CGRAM_CODE_HI, al
    mov cx, FONT_ROWS_PER_GLYPH
    xor bl, bl
@@row_loop:
    mov al, bl
    or al, FONT_UPPER_HALF
    out PC98_CGRAM_PLANE, al
    lodsw
    out PC98_CGRAM_WRITE, al
    mov al, bl
    out PC98_CGRAM_PLANE, al
    mov al, ah
    out PC98_CGRAM_WRITE, al
    inc bl
    loop @@row_loop
    inc dl
    jnz short @@glyph_loop
    mov al, 0Ah
    out PC98_CGRAM_CONTROL, al
    mov dx, offset installed_message
    mov ah, DOS_PRINT
    int DOS_INT
    mov ax, DOS_EXIT
    int DOS_INT
GAIJI_INSTALL_START endp

.data
install_banner db 01Bh,'*GAIJI Setup Program                                    Version 1.00 (C)1998 ZUN',0Dh,0Ah,'$'
installed_message db '外字を定義しましたわ',0Dh,0Ah,0Dh,0Ah,'$'
private_gaiji_pixels label byte
; Generated from the independently pinned 256x256 1bpp BMP geometry.
; The only included file is private proof-local and is NEVER committed.
include gaiji_private_asset.inc

end GAIJI_INSTALL_START

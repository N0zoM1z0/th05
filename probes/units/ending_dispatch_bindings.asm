; Real addresses around both complete far dispatchers; no instructions/values.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public PALETTE_BLACK_OUT
org 00644h
PALETTE_BLACK_OUT label far
org 0ae10h
_TEXT ends
END_DISPATCH_TEXT segment byte public 'CODE' use16
assume cs:END_DISPATCH_TEXT
public @GAMEEXECL$QNXC
org (0cec2h - 0ae10h)
@GAMEEXECL$QNXC label far
org (0d71eh - 0ae10h)
END_DISPATCH_TEXT ends
END_DISPATCH_TAIL segment byte public 'CODE' use16
org (14ab0h - 0d77ch)
END_DISPATCH_TAIL ends
main_01 group END_DISPATCH_TEXT, END_DISPATCH_TAIL
SHARED segment byte public 'CODE' use16
assume cs:SHARED
public SND_KAJA_INTERRUPT
org 004ach
SND_KAJA_INTERRUPT label far
org (209d0h - 14ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _ending_binary_main
org 0143eh
_ending_binary_main label byte
public _ending_binary_extra
org 01444h
_ending_binary_extra label byte
public _continues_used
org 03702h
_continues_used label byte
public _resident
org 041fch
_resident label dword
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

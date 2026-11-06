; Original OP shared function and VSync word; foreign context only.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org (0e15eh - 0d300h)
SHARED ends
FRAME_DELAY_DGROUP_GAP segment byte public 'CODE' use16
org (0efe0h - 0e173h)
FRAME_DELAY_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _vsync_Count1
org 02e4eh
_vsync_Count1 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

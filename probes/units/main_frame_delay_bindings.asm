; Original MAIN shared function and VSync word, without helper bodies or data.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
FRAME_DELAY_MAIN01_GAP segment byte public 'CODE' use16
org (14ab0h - 0ae10h)
FRAME_DELAY_MAIN01_GAP ends
SHARED segment para public 'CODE' use16
org (15102h - 14ab0h)
SHARED ends
FRAME_DELAY_DGROUP_GAP segment byte public 'CODE' use16
org (209d0h - 15117h)
FRAME_DELAY_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _vsync_Count1
org 0267ah
_vsync_Count1 label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

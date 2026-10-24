; Original startup API addresses; no implementations, data values or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START
org 085ah
EGC_START label far
public GRAPH_400LINE
org 012b4h
GRAPH_400LINE label far
public VSYNC_START
org 02320h
VSYNC_START label far
public MEM_ASSIGN_DOS
org 024f0h
MEM_ASSIGN_DOS label far
public JS_START
org 02e46h
JS_START label far
public BGM_INIT
org 03556h
BGM_INIT label far
public PFSTART
org 03980h
PFSTART label far
org 0e800h
_TEXT ends
SHARED segment para public 'CODE' use16
org 08bah
SHARED ends
INIT_SHARED_TAIL segment byte public 'CODE' use16
org 0100eh
INIT_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _bbufsiz
org 0270h
_bbufsiz label word
public _mem_assign_paras
org 06cah
_mem_assign_paras label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

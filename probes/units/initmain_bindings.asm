; Original startup API addresses; no implementations, data values or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START
org 087eh
EGC_START label far
public GRAPH_400LINE
org 01e14h
GRAPH_400LINE label far
public VSYNC_START
org 0260eh
VSYNC_START label far
public MEM_ASSIGN_DOS
org 027aah
MEM_ASSIGN_DOS label far
public JS_START
org 0363eh
JS_START label far
public BGM_INIT
org 03d4eh
BGM_INIT label far
public PFSTART
org 04288h
PFSTART label far
org 0ae10h
_TEXT ends
INIT_MAIN01_CONTEXT segment byte public 'CODE' use16
org 09ca0h
INIT_MAIN01_CONTEXT ends
SHARED segment para public 'CODE' use16
org 04cah
SHARED ends
INIT_SHARED_TAIL segment byte public 'CODE' use16
org 02aeh
INIT_SHARED_TAIL ends
INIT_MAIN03_CONTEXT segment byte public 'CODE' use16
org 0b760h
INIT_MAIN03_CONTEXT ends
_DATA segment word public 'DATA' use16
public _bbufsiz
org 0412h
_bbufsiz label word
public _mem_assign_paras
org 0824h
_mem_assign_paras label word
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

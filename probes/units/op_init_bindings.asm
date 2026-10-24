; Actual OP startup addresses, no instruction/data payload or stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START
org 084ch
EGC_START label far
public GRAPH_CLEAR
org 01216h
GRAPH_CLEAR label far
public GRAPH_START
org 01942h
GRAPH_START label far
public KEY_BEEP_OFF
org 0196eh
KEY_BEEP_OFF label far
public TEXT_CURSOR_HIDE
org 02130h
TEXT_CURSOR_HIDE label far
public TEXT_SYSTEMLINE_HIDE
org 0213ch
TEXT_SYSTEMLINE_HIDE label far
public VSYNC_START
org 02162h
VSYNC_START label far
public MEM_ASSIGN_DOS
org 022b2h
MEM_ASSIGN_DOS label far
public JS_START
org 02bach
JS_START label far
public BGM_INIT
org 0338eh
BGM_INIT label far
public PFSTART
org 037b8h
PFSTART label far
org 0d300h
_TEXT ends
SHARED segment para public 'CODE' use16
org 0c12h
SHARED ends
OP_INIT_DATA_GAP segment byte public 'CODE' use16
org 01052h
OP_INIT_DATA_GAP ends
_DATA segment word public 'DATA' use16
public _bbufsiz
org 0586h
_bbufsiz label word
public _mem_assign_paras
org 09ech
_mem_assign_paras label word
; Known real foreign music DATA end; no supplied values or DATA credit.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Complete decoded MAINE shared cleanup72 atEC3C..EC84; realE80 frame.
; Accepted source unchanged. No foreign bodies, DATA values or artificial stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START, GRAPH_CLEAR, JS_END, TEXT_CLEAR, VSYNC_END
public MEM_UNASSIGN, BGM_FINISH, PFEND
org 0085ah
EGC_START label far
org 01302h
GRAPH_CLEAR label far
org 01b84h
JS_END label far
org 02298h
TEXT_CLEAR label far
org 023ceh
VSYNC_END label far
org 0270ch
MEM_UNASSIGN label far
org 036fah
BGM_FINISH label far
org 03a20h
PFEND label far
org 0e800h
_TEXT ends
EXIT_CORE_TEXT segment byte public 'CODE' use16
assume cs:EXIT_CORE_TEXT
org 0043ch
EXIT_CORE_TEXT ends
shared_exit group EXIT_CORE_TEXT
MAINE_GAME_EXIT_DGROUP_GAP segment byte public 'CODE' use16
org 0148ch
MAINE_GAME_EXIT_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; One complete OP game_exit72 atD7EC..D834, no other compiler-owned callback.
; No foreign bodies, image data, literal values, stack or inside-function holes.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START, GRAPH_CLEAR, JS_END, KEY_BEEP_ON, TEXT_CLEAR
public TEXT_CURSOR_SHOW, TEXT_SYSTEMLINE_SHOW, VSYNC_END, MEM_UNASSIGN
public BGM_FINISH, PFEND
org 0084ch
EGC_START label far
org 01216h
GRAPH_CLEAR label far
org 01968h
JS_END label far
org 0197ah
KEY_BEEP_ON label far
org 020feh
TEXT_CLEAR label far
org 02136h
TEXT_CURSOR_SHOW label far
org 02142h
TEXT_SYSTEMLINE_SHOW label far
org 02210h
VSYNC_END label far
org 024ceh
MEM_UNASSIGN label far
org 03532h
BGM_FINISH label far
org 03858h
PFEND label far
org 0d300h
_TEXT ends
EXIT_CORE_TEXT segment byte public 'CODE' use16
assume cs:EXIT_CORE_TEXT
org 004ech
EXIT_CORE_TEXT ends
shared_exit group EXIT_CORE_TEXT
OP_EXIT_DGROUP_GAP segment byte public 'CODE' use16
org 017ach
OP_EXIT_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
; Real foreign music DATA extent keeps OP's minimum allocation valid.
org 02817h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

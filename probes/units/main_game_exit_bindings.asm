; Complete MAIN shared cleanup72 at14DFC..14E44; accepted source unchanged.
; Actual MASTER labels and outside-only extents, no instructions/data/stack.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public EGC_START, GRAPH_CLEAR, JS_END, TEXT_CLEAR, VSYNC_END
public MEM_UNASSIGN, BGM_FINISH, PFEND
org 0087eh
EGC_START label far
org 01e62h
GRAPH_CLEAR label far
org 01fa6h
JS_END label far
org 024f6h
TEXT_CLEAR label far
org 026bch
VSYNC_END label far
org 029c6h
MEM_UNASSIGN label far
org 03ef2h
BGM_FINISH label far
org 04328h
PFEND label far
org 0ae10h
_TEXT ends
MAIN_GAME_EXIT_MAIN01_GAP segment byte public 'CODE' use16
org 09ca0h
MAIN_GAME_EXIT_MAIN01_GAP ends
EXIT_CORE_TEXT segment byte public 'CODE' use16
assume cs:EXIT_CORE_TEXT
org 0034ch
EXIT_CORE_TEXT ends
shared_exit group EXIT_CORE_TEXT
MAIN_GAME_EXIT_DGROUP_GAP segment byte public 'CODE' use16
org 0bb8ch
MAIN_GAME_EXIT_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

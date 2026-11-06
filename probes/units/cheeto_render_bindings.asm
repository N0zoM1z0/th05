; Original external symbol positions, no bodies or source-owned data.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
CHEETO_RENDER_TEXT segment byte public 'CODE' use16
assume cs:CHEETO_RENDER_TEXT
public @grcg_setcolor_direct_raw$qv, @cheeto_put
org (0c204h - 0ae10h)
@grcg_setcolor_direct_raw$qv label near
org (0de72h - 0ae10h)
@cheeto_put label near
org (12f2bh - 0ae10h)
CHEETO_RENDER_TEXT ends
main_01 group CHEETO_RENDER_TEXT
CHEETO_RENDER_DGROUP_GAP segment para public 'CODE' use16
org (209d0h - 13000h)
CHEETO_RENDER_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _custom_entities, _cheeto_trails
org 0b3f4h
_custom_entities label byte
org 0c0aah
_cheeto_trails label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

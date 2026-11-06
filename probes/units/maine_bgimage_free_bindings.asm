; Complete decoded MAINE release50 at EC0A..EC3C; foreign symbols only.
; Full planes and master allocator remain external, without initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public HMEM_FREE
org 02664h
HMEM_FREE label far
org 0a540h
_TEXT ends
BGFREE_MAIN01_GAP segment byte public 'CODE' use16
org 042c0h
BGFREE_MAIN01_GAP ends
group_01 group BGFREE_MAIN01_GAP
SHARED segment para public 'CODE' use16
org 0040ah
SHARED ends
BGFREE_DGROUP_GAP segment byte public 'CODE' use16
org (10110h - 0ec3ch)
BGFREE_DGROUP_GAP ends
_DATA segment word public 'DATA' use16
public _bgimage
org 006c2h
_bgimage label byte
; Foreign DATA/BSS end, as in the accepted MAINE graphics contexts.
org 04f0eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

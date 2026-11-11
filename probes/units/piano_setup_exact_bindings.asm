; OP real foreign Master/near piano helpers and PMD handle state.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0D894h - 0D300h)
SHARED ends
PIANO_SETUP_TAIL segment byte public 'CODE' use16
assume cs:PIANO_SETUP_TAIL
public _piano_part_keys_put_raw, @piano_label_put_raw, @grcg_setcolor_direct_raw$qv
org (0DA30h - 0D96Eh)
_piano_part_keys_put_raw label near
org (0DB0Dh - 0D96Eh)
@piano_label_put_raw label near
org (0DB21h - 0D96Eh)
@grcg_setcolor_direct_raw$qv label near
org (0EFE0h - 0D96Eh)
PIANO_SETUP_TAIL ends
PIANO_NATIVE_GROUP group SHARED, PIANO_SETUP_TAIL
_DATA segment word public 'DATA' use16
public _pmd_workadr
org 0383Ah
_pmd_workadr label word
org 0383Eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0D300h
_TEXT ends
SHARED segment byte public 'CODE' use16
org (0D96Eh-0D300h)
SHARED ends
PIANO_RENDER_TAIL segment byte public 'CODE' use16
assume cs:PIANO_RENDER_TAIL
public @piano_fm_part_put_raw, @piano_current_note_from, _piano_part_keys_put_raw, @piano_pressed_key_put, @grcg_setcolor_direct_raw$qv
org 0
@piano_fm_part_put_raw label near
org (0DA12h-0D9E2h)
@piano_current_note_from label near
org (0DA30h-0D9E2h)
_piano_part_keys_put_raw label near
org (0DA6Bh-0D9E2h)
@piano_pressed_key_put label near
org (0DB21h-0D9E2h)
@grcg_setcolor_direct_raw$qv label near
org (0EFE0h-0D9E2h)
PIANO_RENDER_TAIL ends
PIANO_RENDER_G group SHARED, PIANO_RENDER_TAIL
_DATA segment word public 'DATA' use16
public _pmd_workadr
org 0383Ah
_pmd_workadr label word
org 0383Eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA,_BSS
end

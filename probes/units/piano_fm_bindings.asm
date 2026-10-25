; Real foreign frames and external symbols only; no initialized payload.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0a390h
_TEXT ends
FOREIGN_MAIN segment byte public 'CODE' use16
org (0d300h-0a390h)
FOREIGN_MAIN ends
SHARED segment para public 'CODE' use16
org 006e2h
SHARED ends
FOREIGN_SHARED_TAIL segment byte public 'CODE' use16
assume cs:FOREIGN_SHARED_TAIL
public @piano_current_note_from
org 00000h
@piano_current_note_from label near
public _piano_part_keys_put_raw
org 0001eh
_piano_part_keys_put_raw label near
public @piano_pressed_key_put
org 00059h
@piano_pressed_key_put label near
public @grcg_setcolor_direct_raw$qv
org 0010fh
@grcg_setcolor_direct_raw$qv label near
org 015ceh
FOREIGN_SHARED_TAIL ends
_DATA segment word public 'DATA' use16
public _piano_notes_cur
org 0382ah
_piano_notes_cur label byte
public _piano_notes_prev
org 03832h
_piano_notes_prev label byte
org 03e96h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

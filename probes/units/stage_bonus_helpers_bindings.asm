; True foreign symbols and holes outside the complete305-byte helper cohort.
; The real8-byte compiler rank table belongs to source, not this context.
.386
.model large
MAIN01_BASE equ 0ae10h
SHARED_BASE equ 14ab0h
MAIN03_BASE equ 15270h
UNIT_START equ 1c669h
UNIT_END equ 1c79ah
DGROUP_BASE equ 209d0h
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
public TEXT_PUTSA
org 02598h
TEXT_PUTSA label far
org MAIN01_BASE
_TEXT ends
BONUS_HELP_MAIN01_GAP segment byte public 'CODE' use16
org (SHARED_BASE - MAIN01_BASE)
BONUS_HELP_MAIN01_GAP ends
main_01 group BONUS_HELP_MAIN01_GAP
BONUS_HELP_SHARED_GAP segment byte public 'CODE' use16
org (MAIN03_BASE - SHARED_BASE)
BONUS_HELP_SHARED_GAP ends
BONUS_HELP_TEXT segment byte public 'CODE' use16
org (UNIT_START - MAIN03_BASE)
BONUS_HELP_TEXT ends
BONUS_HELP_AFTER_TEXT segment byte public 'CODE' use16
org (DGROUP_BASE - UNIT_END)
BONUS_HELP_AFTER_TEXT ends
main_03 group BONUS_HELP_TEXT, BONUS_HELP_AFTER_TEXT
_DATA segment word public 'DATA' use16
public _STAGE_CLEAR_BONUS_DESC, _continues_used, _resident, _rank, _boss
org 1a64h
_STAGE_CLEAR_BONUS_DESC label word
org 3702h
_continues_used label byte
org 41fch
_resident label dword
org 576fh
_rank label byte
org 5abah
_boss label byte
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

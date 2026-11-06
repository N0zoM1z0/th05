; Foreign insertion entry and turbo flag only; no initialized state or code.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
SCORE_TEXT segment byte public 'CODE' use16
assume cs:SCORE_TEXT
public @hiscore_continue_enter_raw$qv
org (0c8f0h - 0ae10h)
@hiscore_continue_enter_raw$qv label near
org (0c998h - 0ae10h)
SCORE_TEXT ends
SCORE_ENTRY_TEXT segment byte public 'CODE' use16
SCORE_ENTRY_TEXT ends
SCORE_ENTRY_TAIL segment byte public 'CODE' use16
org (014ab0h - 0c9a3h)
SCORE_ENTRY_TAIL ends
main_01 group SCORE_TEXT, SCORE_ENTRY_TEXT, SCORE_ENTRY_TAIL
SHARED segment para public 'CODE' use16
org (0209d0h - 014ab0h)
SHARED ends
_DATA segment word public 'DATA' use16
public _turbo_mode
org 05776h
_turbo_mode label byte
org 05777h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

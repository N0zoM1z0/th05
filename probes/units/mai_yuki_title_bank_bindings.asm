; Outside-only context for the complete78-byte named semantic field bank.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MY_TITLE_BANK_MAIN01_SPACE segment byte public 'CODE' use16
org 09ca0h
MY_TITLE_BANK_MAIN01_SPACE ends
main_01 group MY_TITLE_BANK_MAIN01_SPACE
MY_TITLE_BANK_SHARED_SPACE segment byte public 'CODE' use16
org 07c0h
MY_TITLE_BANK_SHARED_SPACE ends
MY_TITLE_BANK_TEXT segment byte public 'CODE' use16
org 0b760h
MY_TITLE_BANK_TEXT ends
main_03 group MY_TITLE_BANK_TEXT
_DATA segment word public 'DATA' use16
org 01916h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

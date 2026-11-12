; Original MAIN code and outside-only accepted filename bank publics.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
STARTUP_RESOURCE_LINKS_TEXT segment byte public 'CODE' use16
org 09ca0h
STARTUP_RESOURCE_LINKS_TEXT ends
main_01 group STARTUP_RESOURCE_LINKS_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
STARTUP_LINKS_MAIN03 segment byte public 'CODE' use16
org 0b760h
STARTUP_LINKS_MAIN03 ends
main_03 group STARTUP_LINKS_MAIN03
_DATA segment word public 'DATA' use16
org 00a2h
_DATA ends
STARTUP_LINKS_FOREIGN_DATA segment byte public 'DATA' use16
public _main_resource_files
org 0008h
_main_resource_files label byte
public _main_session_files
org 0172h
_main_session_files label byte
STARTUP_LINKS_FOREIGN_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, STARTUP_LINKS_FOREIGN_DATA, _BSS
end

.386
.model large
_TEXT segment word public 'CODE' use16
org 0AE10h
_TEXT ends
SHARED segment para public 'CODE' use16
org (015270h - 0AE10h)
SHARED ends
ENEMY_TEMPLATE_PREFIX segment byte public 'CODE' use16
org (016BCFh - 015270h)
ENEMY_TEMPLATE_PREFIX ends
ENEMY_TEMPLATE_COPY_TEXT segment byte public 'CODE' use16
ENEMY_TEMPLATE_COPY_TEXT ends
ENEMY_TEMPLATE_TAIL segment byte public 'CODE' use16
org (0209D0h - 016BE7h)
ENEMY_TEMPLATE_TAIL ends
main_03 group ENEMY_TEMPLATE_PREFIX, ENEMY_TEMPLATE_COPY_TEXT, ENEMY_TEMPLATE_TAIL
_DATA segment word public 'DATA' use16
public _bullet_template
org 0577Eh
_bullet_template label byte
org 0A000h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

; Symbol-only foreign providers and placement. No instruction/data payload.
.386
.model large
_TEXT segment word public 'CODE' use16
assume cs:_TEXT
org 0ae10h
_TEXT ends
ENEMY_VM_MAIN01 segment byte public 'CODE' use16
assume cs:ENEMY_VM_MAIN01
org (014ab0h - 0ae10h)
ENEMY_VM_MAIN01 ends
main_01 group ENEMY_VM_MAIN01
SHARED segment para public 'CODE' use16
assume cs:SHARED
public snd_se_play
org 0232h
snd_se_play label far
org (015270h - 014ab0h)
SHARED ends
ENEMY_VM_TEXT segment byte public 'CODE' use16
assume cs:ENEMY_VM_TEXT
public @PlayfieldMotion@update_seg3$qv, @randring2_next16$qv, vector2_near
org 00ch
@PlayfieldMotion@update_seg3$qv label near
org 02ch
@randring2_next16$qv label near
org 06ah
vector2_near label near
org (01538ch - 015270h)
ENEMY_VM_TEXT ends
ENEMY_VM_MAIN03_TAIL segment byte public 'CODE' use16
assume cs:ENEMY_VM_MAIN03_TAIL
public @player_angle_from$q20%SubpixelBase$ti$ti%t1uc
org (0171cch - 015870h)
@player_angle_from$q20%SubpixelBase$ti$ti%t1uc label near
org (0209d0h - 015870h)
ENEMY_VM_MAIN03_TAIL ends
main_03 group ENEMY_VM_TEXT, ENEMY_VM_MAIN03_TAIL
_DATA segment word public 'DATA' use16
public _CosTable8, enemy_bullet_emitters, _std_seg, _enemies_gone
public _scroll_last_delta, enemy_vm_emitter_slot, _enemy_cur
public _bullet_template_tune, _rank, _playperf, _bullet_template
org 049ch
_CosTable8 label word
org 0f4ch
enemy_bullet_emitters label word
org 0f52h
_std_seg label word
org 014a4h
_enemies_gone label word
org 03518h
_scroll_last_delta label word
org 03524h
enemy_vm_emitter_slot label word
org 03f92h
_enemy_cur label word
org 041deh
_bullet_template_tune label word
org 0576fh
_rank label byte
org 05770h
_playperf label byte
org 0577eh
_bullet_template label byte
org 0c4c8h
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

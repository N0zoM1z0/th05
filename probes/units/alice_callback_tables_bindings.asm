; Real Alice callbacks are symbolic externals at complete original CODE public
; addresses; the binder owns no game instructions or initialized DATA.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0ae10h
_TEXT ends
MAIN_01_TEXT segment byte public 'CODE' use16
org 09ca0h
MAIN_01_TEXT ends
CIRCLE_TEXT segment byte public 'CODE' use16
CIRCLE_TEXT ends
main_01 group MAIN_01_TEXT, CIRCLE_TEXT
SHARED segment byte public 'CODE' use16
org 07c0h
SHARED ends
B4_UPDATE_TEXT segment byte public 'CODE' use16
assume cs:B4_UPDATE_TEXT
public @ALICE_PUPPET_INITIAL$QR11ALICEPUPPET
org 08f99h
@ALICE_PUPPET_INITIAL$QR11ALICEPUPPET label near
public @ALICE_PUPPET_SPREAD$QR11ALICEPUPPET
org 0900ah
@ALICE_PUPPET_SPREAD$QR11ALICEPUPPET label near
public @ALICE_PUPPET_AIMED_BURSTS$QR11ALICEPUPPET
org 0907ch
@ALICE_PUPPET_AIMED_BURSTS$QR11ALICEPUPPET label near
public @ALICE_PUPPET_RING_BURSTS$QR11ALICEPUPPET
org 090f1h
@ALICE_PUPPET_RING_BURSTS$QR11ALICEPUPPET label near
public @alice_pattern_opening_cycle$qv
org 09280h
@alice_pattern_opening_cycle$qv label near
public @alice_pattern_ring_stack$qv
org 0929ah
@alice_pattern_ring_stack$qv label near
public @alice_pattern_spread_stack$qv
org 09316h
@alice_pattern_spread_stack$qv label near
public @alice_pattern_laser_fan$qv
org 094f4h
@alice_pattern_laser_fan$qv label near
public @alice_pattern_paired_stacks$qv
org 095bch
@alice_pattern_paired_stacks$qv label near
public @alice_pattern_rotating_ring$qv
org 09657h
@alice_pattern_rotating_ring$qv label near
org 0b760h
B4_UPDATE_TEXT ends
ALICE_PUP_TEXT segment byte public 'CODE' use16
ALICE_PUP_TEXT ends
ALICE_OPN_TEXT segment byte public 'CODE' use16
ALICE_OPN_TEXT ends
ALICE_CHG_TEXT segment byte public 'CODE' use16
ALICE_CHG_TEXT ends
ALICE_CALLBACK_TABLE_TEXT segment byte public 'CODE' use16
ALICE_CALLBACK_TABLE_TEXT ends
main_03 group B4_UPDATE_TEXT, ALICE_PUP_TEXT, ALICE_OPN_TEXT, ALICE_CHG_TEXT, ALICE_CALLBACK_TABLE_TEXT
_DATA segment word public 'DATA' use16
org 01f7eh
_DATA ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, _BSS
end

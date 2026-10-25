; Original outside-only MAINE DATA frame. No text, assets, or instructions.
.386
.model large
_TEXT segment word public 'CODE' use16
org 0A540h
_TEXT ends
ALLCAST_LINES_DATA_TEXT segment byte public 'CODE' use16
org (0E800h - 0A540h)
ALLCAST_LINES_DATA_TEXT ends
group_01 group ALLCAST_LINES_DATA_TEXT
SHARED segment para public 'CODE' use16
org (10110h - 0E800h)
SHARED ends
_DATA segment word public 'DATA' use16
org 00820h
_DATA ends

; This genuine foreign DATA context follows the complete 202-byte CPP owner.
; All labels designate original string starts; no string contents are supplied.
ALLCAST_TEXT_CONTEXT segment byte public 'DATA' use16
public _allcast_project
org 0011Ch
_allcast_project label byte
public _allcast_th01_title
org 0014Ch
_allcast_th01_title label byte
public _allcast_th01_reimu
org 0018Dh
_allcast_th01_reimu label byte
public _allcast_th02_title
org 001C6h
_allcast_th02_title label byte
public _allcast_th02_reimu
org 00202h
_allcast_th02_reimu label byte
public _allcast_th02_rika
org 0023Bh
_allcast_th02_rika label byte
public _allcast_th02_meira
org 00275h
_allcast_th02_meira label byte
public _allcast_th02_marisa
org 002AFh
_allcast_th02_marisa label byte
public _allcast_th02_mima
org 002EAh
_allcast_th02_mima label byte
public _allcast_th03_title
org 00322h
_allcast_th03_title label byte
public _allcast_th03_reimu
org 00361h
_allcast_th03_reimu label byte
public _allcast_th03_marisa
org 0039Ah
_allcast_th03_marisa label byte
public _allcast_th03_mima
org 003D5h
_allcast_th03_mima label byte
public _allcast_th03_ellen
org 0040Eh
_allcast_th03_ellen label byte
public _allcast_th03_kotohime
org 00447h
_allcast_th03_kotohime label byte
public _allcast_th03_kana
org 00482h
_allcast_th03_kana label byte
public _allcast_th03_rikako
org 004BFh
_allcast_th03_rikako label byte
public _allcast_th03_chiyuri
org 004FAh
_allcast_th03_chiyuri label byte
public _allcast_th03_yumemi
org 0053Bh
_allcast_th03_yumemi label byte
public _allcast_th04_title
org 00576h
_allcast_th04_title label byte
public _allcast_th04_reimu
org 005B4h
_allcast_th04_reimu label byte
public _allcast_th04_marisa
org 005EDh
_allcast_th04_marisa label byte
public _allcast_th04_orange
org 00628h
_allcast_th04_orange label byte
public _allcast_th04_kurumi
org 00666h
_allcast_th04_kurumi label byte
public _allcast_th04_elly
org 006A0h
_allcast_th04_elly label byte
public _allcast_th04_yuuka
org 006DDh
_allcast_th04_yuuka label byte
public _allcast_th04_mugetsu
org 0071Bh
_allcast_th04_mugetsu label byte
public _allcast_th04_gengetsu
org 00753h
_allcast_th04_gengetsu label byte
public _allcast_th05_title
org 0078Ch
_allcast_th05_title label byte
public _allcast_th05_reimu
org 007C9h
_allcast_th05_reimu label byte
public _allcast_th05_marisa
org 00802h
_allcast_th05_marisa label byte
public _allcast_th05_mima
org 0083Dh
_allcast_th05_mima label byte
public _allcast_th05_yuuka
org 00876h
_allcast_th05_yuuka label byte
public _allcast_th05_sara
org 008B4h
_allcast_th05_sara label byte
public _allcast_th05_louise
org 008F1h
_allcast_th05_louise label byte
public _allcast_th05_alice
org 0092Ah
_allcast_th05_alice label byte
public _allcast_th05_yuki
org 00968h
_allcast_th05_yuki label byte
public _allcast_th05_mai
org 009A5h
_allcast_th05_mai label byte
public _allcast_th05_yumeko
org 009E2h
_allcast_th05_yumeko label byte
public _allcast_th05_shinki
org 00A1Ah
_allcast_th05_shinki label byte
public _allcast_credit_program
org 00A5Eh
_allcast_credit_program label byte
public _allcast_credit_graphics
org 00A9Dh
_allcast_credit_graphics label byte
public _allcast_credit_music
org 00ADCh
_allcast_credit_music label byte
public _allcast_credit_pmd
org 00B1Bh
_allcast_credit_pmd label byte
public _allcast_credit_thanks
org 00B5Bh
_allcast_credit_thanks label byte
public _allcast_credit_makers
org 00B91h
_allcast_credit_makers label byte
public _allcast_credit_players
org 00BD1h
_allcast_credit_players label byte
ALLCAST_TEXT_CONTEXT ends
_BSS segment word public 'BSS' use16
_BSS ends
DGROUP group _DATA, ALLCAST_TEXT_CONTEXT, _BSS
end

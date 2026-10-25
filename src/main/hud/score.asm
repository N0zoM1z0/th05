; Score HUD and incremental little-endian decimal tally, GAME5 semantics.
; Native ASM origin review is separate from exact producer acceptance.
.386
.model large
locals
include types.inc
include symbols.inc

SCORE_DELTA_LIMIT equ 6111

main_01 group MAIN_01_TEXT
MAIN_01_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
extrn @OVERLAY_POPUP_UPDATE_AND_RENDER$QV:near
public HUD_SCORE_PUT
HUD_SCORE_PUT proc near
 push si
 push di
 mov si, offset _hiscore[SCORE_DIGITS - 1]
 mov di, HUD_HISCORE_ROW
@@row:
 mov cx, SCORE_DIGITS
 mov bx, offset _hud_gaiji_row
@@digit:
 mov al, [si]
 add al, SCORE_DIGIT_GLYPH
 mov [bx], al
 inc bx
 dec si
 loop @@digit
 push HUD_SCORE_COLUMN
 push di
 push ds
 push offset _hud_gaiji_row
 push HUD_SCORE_WHITE
 call GAIJI_PUTSA
 add di, HUD_SCORE_ROW_STEP
 ; The current score directly precedes hiscore: SI is deliberately not reset.
 cmp di, HUD_SCORE_ROW
 jz short @@row
 ; Preserve the native reversed restore order, which swaps caller SI and DI.
 pop si
 pop di
 ret
HUD_SCORE_PUT endp

public @SCORE_UPDATE_AND_RENDER$QV
@SCORE_UPDATE_AND_RENDER$QV proc near
 mov eax, _score_delta
 or eax, eax
 jz short @@ret
 cmp _score_delta_frame, eax
 jbe short @@frame_delta
 mov word ptr _score_delta_frame, ax
@@frame_delta:
 shr eax, SCORE_DELTA_SHIFT
 or eax, eax
 jnz short @@clamp
 inc ax
 jmp short @@prefer_larger
@@clamp:
 cmp eax, SCORE_DELTA_LIMIT
 jbe short @@prefer_larger
 mov ax, SCORE_DELTA_LIMIT
@@prefer_larger:
 cmp word ptr _score_delta_frame, ax
 jnb short @@commit
 mov word ptr _score_delta_frame, ax
@@commit:
 mov dx, word ptr _score_delta_frame
 jmp short @@update

@@render:
 cmp _hiscore_popup_shown, 0
 jnz short @@subtract
 or al, al
 jz short @@subtract
 mov _hiscore_popup_shown, 1
 mov _overlay_popup_id_new, SCORE_POPUP_HISCORE
 mov _overlay2, offset @OVERLAY_POPUP_UPDATE_AND_RENDER$QV
@@subtract:
 mov eax, _score_delta_frame
 sub _score_delta, eax
 call HUD_SCORE_PUT
@@ret:
 ret
 even

@@update:
 push si
 push di
 push ds
 pop es
 ; The shared row is scratch decimal storage here, not character data yet.
 mov dword ptr _hud_gaiji_row[4], 0
 mov di, offset _hud_gaiji_row[4]
 mov bx, offset _FIVE_DIGIT_POWERS_OF_10
 mov cx, SCORE_DELTA_DIVISIONS
@@decimal:
 mov ax, dx
 xor dx, dx
 div word ptr [bx]
 add bx, SCORE_DIVISOR_BYTES
 mov [di], al
 dec di
 loop @@decimal
 mov [di], dl

 ; Digit zero is the continues-used slot, so begin tallying at digit one.
 mov si, offset _score[1]
 mov cx, (SCORE_DIGITS - 2)
 xor ah, ah
@@add_digit:
 movzx ax, byte ptr [di]
 add al, [si]
 aaa
 mov [si], al
 inc di
 inc si
 add [si], ah
 loop @@add_digit
 ; Preserve the original unadjusted highest digit and its overflow behavior.
 mov al, [di]
 add [si], al

 mov si, offset _score[SCORE_DIGITS - 1]
 mov di, offset _hiscore[SCORE_DIGITS - 1]
 xor dl, dl
 mov cx, SCORE_DIGITS
 cmp _hiscore_popup_shown, 0
 jnz short @@record
@@compare_digit:
 mov al, [si]
 cmp [di], al
 ja short @@no_record
 jb short @@record
 dec di
 dec si
 loop @@compare_digit
@@record:
 cli
 std
 rep movsb
 cld
 sti
 inc dl
@@no_record:
 mov al, dl
 pop di
 pop si
 jmp @@render
@SCORE_UPDATE_AND_RENDER$QV endp
public hud_score_end
hud_score_end label byte
MAIN_01_TEXT ends
end

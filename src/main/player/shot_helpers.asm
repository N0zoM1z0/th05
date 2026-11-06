; Allocation, angle-vector assignment and power-level selection for player shots.
; Candidate allocation/vector algorithms: ReC98 b6ba5b0a TH05/TH04 shot helpers.
.386
.model large
locals
include types.inc
include symbols.inc
SHOT_PRIMARY_PATTERN equ 20

; Initialize only the fields the allocator actually owns. Previous position,
; damage and angle remain untouched; the caller completes the new shot.
INITIALIZE_PRIMARY_SHOT macro
 mov word ptr [bx].SHOT_RECORD.SH_flag, SHOT_ALIVE
 mov eax, _player_pos
 mov dword ptr [bx].SHOT_RECORD.SH_cur_x, eax
 mov dword ptr [bx].SHOT_RECORD.SH_velocity_x, SHOT_DEFAULT_VELOCITY
 mov word ptr [bx].SHOT_RECORD.SH_patnum, SHOT_PRIMARY_PATTERN
endm

main_01 group SHOT_HELPERS_TEXT
SHOT_HELPERS_TEXT segment word public 'CODE' use16
assume cs:main_01, ds:DGROUP
public @shots_add$qv
@shots_add$qv proc near
 xor ax, ax
 mov bx, _shot_ptr
@@find_slot:
 cmp bx, offset _shots_end
 jae short @@return
 add bx, size SHOT_RECORD
 cmp [bx].SHOT_RECORD.SH_flag, SHOT_FREE
 jne short @@find_slot
 INITIALIZE_PRIMARY_SHOT
 mov ax, bx
 add bx, size SHOT_RECORD
 mov _shot_ptr, bx
@@return:
 ret
@shots_add$qv endp
even

; Snapshot entry SP before saving SI. The angle argument occupies a WORD slot.
; The nominal point pointer must really address SH_velocity_x inside a shot.
public @SHOT_VELOCITY_SET$QP7SPPOINTUC
@SHOT_VELOCITY_SET$QP7SPPOINTUC proc near
 mov bx, sp
 push si
 mov si, ss:[bx + SHOT_ARG_VELOCITY]
 movzx bx, byte ptr ss:[bx + SHOT_ARG_ANGLE]
 mov byte ptr [si + SHOT_ANGLE_FROM_VELOCITY], bl
 shl bx, 2
 mov eax, _VELOCITY_192_AT_ANGLE[bx]
 mov [si], eax
 pop si
 ret SHOT_ARGUMENT_BYTES
@SHOT_VELOCITY_SET$QP7SPPOINTUC endp

; BX is a byte offset into WORD thresholds and then the current character's
; near-function row. DX converts it into the stored byte-sized level.
; This is a descriptive public name; the historical name is not established.
; Existing C and C++ callers use both spellings for this same argumentless ABI.
public SHOT_LEVEL_UPDATE, @shot_level_update$qv
@shot_level_update$qv label far
SHOT_LEVEL_UPDATE proc far
 xor bx, bx
 xor ax, ax
 mov al, _power
 mov cx, SHOT_POWER_BOUND_COUNT
@@next_threshold:
 cmp ax, _SHOT_LEVEL_TO_POWER[bx]
 jb short @@level_found
 add bx, SHOT_FUNCTION_WORD_BYTES
 loop @@next_threshold
@@level_found:
 mov dx, bx
 shr dx, 1
 mov _shot_level, dl
 add bx, _playchar_shot_funcs
 mov ax, [bx]
 mov _playchar_shot_func, ax
 call HUD_POWER_PUT
 retf
SHOT_LEVEL_UPDATE endp
public shot_helpers_end
shot_helpers_end label byte
SHOT_HELPERS_TEXT ends
end

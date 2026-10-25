; Semantic TH05 original-ASM sound-file loader reconstruction.
; Candidate: pinned ReC98 b6ba5b0a th05/snd/load.cpp; no pseudo-C++/opcode emits.
.386
.model use16 large SHARED
locals
include types.inc
include symbols.inc

SOUND_READ_LIMIT equ 0FFFFh
BEEP_POOL_BYTES equ 2048
BEEP_EXTENSION equ ('e' or ('f' shl 8) or ('s' shl 16))

; DOS opens a filename in the original DATA segment and returns handle/error AX.
DOS_OPEN_SOUND macro
 mov dx, offset _snd_load_fn
 mov ax, DOS_OPEN_READ
 int DOS_INTERRUPT
endm

.code SHARED
public SND_LOAD
SND_LOAD proc far
 ; Far Pascal (filename16:16, load-function16): last word then far pointer.
 arg @@func:word, @@filename:dword
 push bp
 mov bp, sp
 push si
 push di
 mov dx, ds
 mov es, dx
 mov di, offset _snd_load_fn
 lds si, @@filename
 mov bp, @@func
 mov cx, SOUND_FILENAME_BYTES
 rep movsb
 mov ds, dx
 mov di, offset _snd_load_fn
 dec cx
 xor ax, ax
 repne scasb
 dec di
 mov byte ptr [di], '.'
 inc di
 cmp bp, SND_LOAD_SE
 jnz short @@song
 cmp _snd_se_mode, SND_SE_OFF
 jz short @@ret
 xor bx, bx
 cmp _snd_se_mode, SND_SE_BEEP
 jnz short @@select_extension
 mov dword ptr [di], BEEP_EXTENSION
 call BGM_FINISH
 push BEEP_POOL_BYTES
 call BGM_INIT
 push ds
 push offset _snd_load_fn
 call BGM_READ_SDATA
 jmp short @@ret
@@song:
 cmp _snd_bgm_mode, SND_BGM_OFF
 jz short @@ret
 push (KAJA_SONG_STOP shl 8)
 ; Real far Pascal provider in the same CS; retain its far return stack.
 push cs
 call near ptr SND_KAJA_INTERRUPT
 movzx bx, _snd_bgm_mode
 shl bx, 2
@@select_extension:
 ; The last dword intentionally reads one byte beyond the packed15-byte bank.
 mov eax, dword ptr _SND_LOAD_EXT[bx]
@@try_open:
 mov [di], eax
 DOS_OPEN_SOUND
 jnc short @@opened
 cmp ax, DOS_FILE_NOT_FOUND
 jnz short @@ret
 mov eax, dword ptr _SND_LOAD_EXT[4*SND_BGM_FM26]
 jmp short @@try_open
@@opened:
 mov bx, ax
 mov ax, bp
 cmp ah, KAJA_GET_SONG_ADDRESS
 jnz short @@pmd_buffer
 cmp _snd_bgm_mode, SND_BGM_MIDI
 jnz short @@pmd_buffer
 int MMD_INTERRUPT
 jmp short @@read
@@pmd_buffer:
 int PMD_INTERRUPT
@@read:
 ; Driver returns destination DS:DX. Read and close keep the file handle BX.
 mov ax, DOS_READ
 mov cx, SOUND_READ_LIMIT
 int DOS_INTERRUPT
 mov ah, DOS_CLOSE
 int DOS_INTERRUPT
 push es
 pop ds
@@ret:
 pop di
 pop si
 pop bp
 retf 6
SND_LOAD endp
public sound_load_end
sound_load_end label byte
end

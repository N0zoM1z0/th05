; TH05 performance bounds and parameter selectors, original assembly family.
; Natural semantics follow TH04 playperf/select_for_rank and TH05 playchar.
.386
.model large
locals
include types.inc
include symbols.inc

main_01 group PLAYPERF_TEXT
PLAYPERF_TEXT segment byte public 'CODE' use16
assume cs:main_01, ds:DGROUP
public PLAYPERF_RAISE, PLAYPERF_LOWER
public @SELECT_FOR_PLAYCHAR$QIIII, SELECT_FOR_RANK, playperf_select_end

PLAYPERF_RAISE proc far
    mov bx, sp
    mov al, ss:[bx+4]
    add al, _playperf
    cmp al, _playperf_max
    jbe short @@store
    mov al, _playperf_max
@@store:
    mov _playperf, al
    retf 2
PLAYPERF_RAISE endp
    even

PLAYPERF_LOWER proc far
    mov bx, sp
    mov al, _playperf
    sub al, ss:[bx+4]
    cmp al, _playperf_min
    jge short @@store
    mov al, _playperf_min
@@store:
    mov _playperf, al
    retf 2
PLAYPERF_LOWER endp

@SELECT_FOR_PLAYCHAR$QIIII proc far
    mov al, _playchar
    jmp short select_for_selector
@SELECT_FOR_PLAYCHAR$QIIII endp
    even

SELECT_FOR_RANK proc far
    mov al, _rank
select_for_selector:
    xor ah, ah
    add ax, ax
    mov bx, SELECT_ARGUMENT_DISPLACEMENT
    sub bx, ax
    add bx, sp
    mov ax, ss:[bx]
    retf 8
SELECT_FOR_RANK endp
playperf_select_end label byte
PLAYPERF_TEXT ends
end

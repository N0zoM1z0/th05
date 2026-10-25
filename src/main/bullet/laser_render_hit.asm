; Semantic reconstruction of TH05's private laser geometry/render/hit family.
; Pinned ReC98 laser_rh algorithms are references; original ASM origin is reviewed
; independently from their synthetic C++ codegen/emits and from exact replay.
.386
.model large
locals
include types.inc
include symbols.inc

HITBOX_PIXELS equ 12
HIT_STEP_PIXELS equ 16

; Signed 32-bit radius*table product, arithmetic /256, then 16-bit center wrap.
; BP addresses the SS center; DI the SS result; SI the byte table index.
POLAR_COMPONENT macro table, component
 movsx eax, bx
 movsx edx, word ptr table[si]
 imul eax, edx
 sar eax, 8
 add ax, [bp+component]
 mov ss:[di+component], ax
endm

; Convert a point and its endpoint to pixels in place, retaining word wrapping.
; The private BP contract places the displacement one point above BP.
LINE_COMPONENT macro component
 mov ax, [bp+(size point_t)+component]
 mov dx, ss:[di+component]
 add ax, dx
 sar ax, SUBPIXEL_BITS
 sar dx, SUBPIXEL_BITS
 mov ss:[bx+component], ax
 mov ss:[di+component], dx
endm

main_01 group LASER_RH_TEXT
LASER_RH_TEXT segment word public 'CODE' use16
assume cs:main_01
public laser_vector_at
laser_vector_at proc near
 push si
 mov si, cx
 add si, si
 POLAR_COMPONENT _CosTable8, point_t.x
 POLAR_COMPONENT _SinTable8, point_t.y
 pop si
 ret
laser_vector_at endp

public laser_line_to_pixels
laser_line_to_pixels proc near
 LINE_COMPONENT point_t.x
 LINE_COMPONENT point_t.y
 ret
laser_line_to_pixels endp

; Near Pascal: DS:coords, caller's word argument removed. Full 32-byte overlay.
public laser_render_ray, @LASER_RENDER_RAY$QRX14LASER_COORDS_T
@LASER_RENDER_RAY$QRX14LASER_COORDS_T label near
laser_render_ray proc near
 enter RAY_BYTES, 0
 push si
 push di
 mov si, [bp+4]
 mov bl, [si+laser_coords_t.LC_width+laser_width_t.nonshrink]
 mov bh, 0
 shl bx, (SUBPIXEL_BITS-1)
 mov ax, [si+laser_coords_t.LC_origin+point_t.x]
 add ax, (PLAYFIELD_LEFT shl SUBPIXEL_BITS)
 mov [bp+RAY_ORIGIN+point_t.x], ax
 mov ax, [si+laser_coords_t.LC_origin+point_t.y]
 add ax, (PLAYFIELD_TOP shl SUBPIXEL_BITS)
 mov [bp+RAY_ORIGIN+point_t.y], ax
 mov cl, [si+laser_coords_t.LC_angle]
 add cl, 40h
 mov ch, 0
 lea di, [bp+RAY_DELTA]
 sub bp, -(RAY_ORIGIN)
 call laser_vector_at
 ; Opposite perpendicular endpoint; turn the first endpoint into a delta.
 add cl, 80h
 sub di, size point_t
 call laser_vector_at
 sub [bp+(RAY_DELTA-RAY_ORIGIN)+point_t.y], ax
 mov ax, [bp+(RAY_ORIGIN_CCW-RAY_ORIGIN)+point_t.x]
 sub [bp+(RAY_DELTA-RAY_ORIGIN)+point_t.x], ax
 ; Move the center to origin_ccw and construct the two ray ends.
 mov cl, [si+laser_coords_t.LC_angle]
 mov bx, [si+laser_coords_t.LC_start]
 sub di, (ray_construction_t.RC_origin_ccw-ray_construction_t.RC_start_ccw)
 sub bp, (ray_construction_t.RC_origin-ray_construction_t.RC_origin_ccw)
 call laser_vector_at
 mov bx, [si+laser_coords_t.LC_end]
 add di, (ray_construction_t.RC_end_ccw-ray_construction_t.RC_start_ccw)
 call laser_vector_at
 ; Both endpoints now become screen pixels in the overlaid corner view.
 lea di, [bp+(RAY_START_CCW-RAY_ORIGIN_CCW)]
 lea bx, [bp+(ray_corners_t.start_cw-RAY_BYTES-RAY_ORIGIN_CCW)]
 call laser_line_to_pixels
 add di, (ray_corners_t.end_ccw-ray_corners_t.start_ccw)
 add bx, (ray_corners_t.end_cw-ray_corners_t.start_cw)
 call laser_line_to_pixels
 add bp, -(RAY_ORIGIN_CCW)
 lea di, [bp-RAY_BYTES]
 ; Far Pascal clipping receives two genuine SS:DI far pointers.
 push ss
 push di
 push 8
 push ss
 push di
 push 4
 call GRC_CLIP_POLYGON_N
 or ax, ax
 jz short @@offscreen
 jge short @@draw
 mov ax, 4
@@draw:
 push ss
 push di
 push ax
 call GRCG_POLYGON_CX
 xor ax, ax
 jmp short @@ret
@@offscreen:
 mov ax, 1
@@ret:
 pop di
 pop si
 leave
 ret 2
laser_render_ray endp

; Near Pascal, full Laser24 by near reference. Preserve the reversed DI/SI saves.
public laser_hittest, @LASER_HITTEST$QR5LASER
@LASER_HITTEST$QR5LASER label near
laser_hittest proc near
 enter (size hit_scratch_t), 0
 push di
 push si
 mov di, [bp+4]
 mov bx, [di+laser_t.coords+laser_coords_t.LC_end]
 mov si, [di+laser_t.coords+laser_coords_t.LC_start]
 sub bp, (size point_t)
 mov eax, dword ptr [di+laser_t.coords+laser_coords_t.LC_origin]
 mov [bp], eax
 mov cl, [di+laser_t.coords+laser_coords_t.LC_angle]
 xor ch, ch
 lea di, [bp-(size point_t)]
@@next_box:
 call laser_vector_at
 add ax, ((HITBOX_PIXELS/2) shl SUBPIXEL_BITS)
 sub ax, _player_pos.cur.y
 cmp ax, (HITBOX_PIXELS shl SUBPIXEL_BITS)
 jnb short @@advance
 mov ax, ss:[di+point_t.x]
 add ax, ((HITBOX_PIXELS/2) shl SUBPIXEL_BITS)
 sub ax, _player_pos.cur.x
 cmp ax, (HITBOX_PIXELS shl SUBPIXEL_BITS)
 jnb short @@advance
 mov _player_is_hit, 1
 jmp short @@ret
@@advance:
 sub bx, (HIT_STEP_PIXELS shl SUBPIXEL_BITS)
 cmp bx, si
 jge short @@next_box
@@ret:
 add bp, size point_t
 pop si
 pop di
 leave
 ret 2
laser_hittest endp
public laser_render_hit_end
laser_render_hit_end label byte
LASER_RH_TEXT ends
end

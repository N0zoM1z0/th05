; Full original byte-packed geometry and bullet-template records.
; Keep in agreement with shared/geometry.hpp, bullet/template.hpp and bullet/update.hpp.
; All declarations are type-only; they emit no DATA or BSS payload.
Point struc
    x dw ?
    y dw ?
Point ends
motion_t struc
    cur Point <?>
    prev Point <?>
    velocity Point <?>
motion_t ends
bullet_template_t struc
    spawn_type db ?
    patnum db ?
    BT_origin Point <?>
    BT_group db ?
    BT_special_motion db ?
    spread db ?
    spread_angle_delta db ?
    BT_stack db ?
    stack_speed_delta db ?
    BT_angle db ?
    speed db ?
bullet_template_t ends

bullet_special_angle_t union
    BSA_turn_by db ?
    BSA_target db ?
    BSA_v db ?
bullet_special_angle_t ends
bullet_t struc
    flag db ?
    age db ?
    pos motion_t <?>
    from_group db ?
    unused db ?
    speed_cur db ?
    BULLET_angle db ?
    spawn_flag db ?
    move_flag db ?
    special_motion db ?
    speed_final db ?
    decelerate_time label byte
    turns_done label byte
    BULLET_ax db ?
    decelerate_speed_delta label byte
    BULLET_SPECIAL_angle label bullet_special_angle_t
    BULLET_dx db ?
    BULLET_patnum dw ?
    BULLET_origin Point <?>
    distance dw ?
bullet_t ends
gather_template_t struc
    GT_center Point <?>
    GT_velocity Point <?>
    GT_radius dw ?
    GT_ring_points dw ?
    GT_col db ?
    GT_angle_delta db ?
gather_template_t ends
if size Point ne 4
    .err
endif
if size motion_t ne 12
    .err
endif
if size bullet_template_t ne 14
    .err
endif
if size bullet_t ne 32
    .err
endif
if size gather_template_t ne 14
    .err
endif

BGC0_STATIC = 0
BGC0_AIMED  = 1
BGCC_SPREAD = 2
BGCC_RING   = 4
BGCS_STACK  = 6
BGCF_SINGLE = 14

BG_SINGLE = (BGC0_STATIC)
BG_SINGLE_AIMED = (BGC0_AIMED)
BG_SPREAD = (BGCC_SPREAD + BGC0_STATIC)
BG_SPREAD_AIMED = (BGCC_SPREAD + BGC0_AIMED)
BG_RING = (BGCC_RING)
BG_RING_AIMED = (BGCC_RING + BGC0_AIMED)
BG_STACK = (BGCS_STACK)
BG_STACK_AIMED = (BGCS_STACK + BGC0_AIMED)
BG_SPREAD_STACK = (BGCS_STACK + BGCC_SPREAD + BGC0_STATIC)
BG_SPREAD_STACK_AIMED = (BGCS_STACK + BGCC_SPREAD + BGC0_AIMED)
BG_RING_STACK = (BGCS_STACK + BGCC_RING + BGC0_STATIC)
BG_RING_STACK_AIMED = (BGCS_STACK + BGCC_RING + BGC0_AIMED)
BG_RANDOM_ANGLE = 12
BG_RANDOM_ANGLE_AND_SPEED = 13
BG_FORCESINGLE = (BGCF_SINGLE)
BG_FORCESINGLE_AIMED = (BGCF_SINGLE + BGC0_AIMED)

BST_GATHER_NORMAL_SPECIAL_MOVE = 0FEh
BST_GATHER_ONLY = 0FFh
BST_NORMAL = 00h
BST_GATHER_PELLET = 01h
BST_CLOUD_FORWARDS = 02h
BST_CLOUD_BACKWARDS = 03h
BST_NO_DECELERATE = 10h


F_FREE equ 0
F_ALIVE equ 1
PELLET_COUNT equ 180
BULLET16_COUNT equ 220
BSF_GRAZEABLE equ 0
BSF_CLOUD_BACKWARDS equ 3
BSF_CLOUD_FORWARDS equ 4
BMF_DECELERATE equ 0
BMF_SPECIAL equ 1
BMF_REGULAR equ 2
BMF_DECELERATE_FRAMES equ 32
BMF_DECELERATE_BASE_SPEED equ (4 shl 4) + 8
PAT_BULLET16_D equ 52

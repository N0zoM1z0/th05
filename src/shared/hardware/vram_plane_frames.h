/* Original four PC-98 16-bit-planar video address-space selectors. */
#ifndef TH05_SHARED_VRAM_PLANE_FRAMES_H
#define TH05_SHARED_VRAM_PLANE_FRAMES_H

typedef unsigned char far *PC98VramPlane;
enum PC98VramSegment {
    VRAM_SEGMENT_BLUE = 0xA800,
    VRAM_SEGMENT_RED = 0xB000,
    VRAM_SEGMENT_GREEN = 0xB800,
    VRAM_SEGMENT_EXTENDED = 0xE000
};

/* Physical far pointer representation is [segment:offset] with offset zero.
 * The expression is a typed hardware address, not a copied image payload. */
#define PC98_VRAM_AT(seg) ((PC98VramPlane)((unsigned long)(seg) << 16))

#endif

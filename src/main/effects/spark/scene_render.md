# sparks_render(): draw all live sparks (original assembly)

`scene_render.asm` loops over the 64 sparks, sets GRCG color 12 and the blue
VRAM plane (ES = A800h), skips records that are not alive, converts Y with
the scroll helper, turns the subpixel X into a pixel position, and calls
`spark_render` with the spark's age in CL as the cel. It ends with one
`EVEN` alignment NOP. Same code as ReC98's `th04/main/sparks.asm`.

A plain C++ version (`render_candidate.cpp`) compiles to 71 bytes instead of
60, because Borland sets up a BP frame and spills the coordinates.

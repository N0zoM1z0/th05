# `mpn_put()`: .MPN tile renderer (ASM)

`mpn_render.asm` covers MAIN `4226..4282`: a 75-byte far Pascal
`mpn_put(left, top, image)` (`RETF 6`), one `EVEN` NOP, and a 16-byte private
near worker that copies one bitplane.

An image is four 16x16 planes of 32 bytes each, 128 bytes in total. The
wrapper checks the image number against the inclusive limit at DS `306A`
(unsigned, so the full word is compared), then calls the worker four times
in B/R/G/E order. The worker takes AX = plane segment, DS:SI = source and
DI = destination, and advances SI by one plane. `image * 128` wraps at 16
bits, as in the original. The left coordinate is divided by 8 with `SAR`.

An out-of-range image returns without drawing. On the valid path the routine
leaves ES at `E000`. ZUN landmine: there is no clipping, and the direction
flag and the VRAM plane-write state are assumed to be set up by the caller.

TH04's renderer has a different slot record and plane schedule, so it is only
a structural reference. master.lib's `OVERPUT8` is similar (four plane calls,
`y * 80`), but its pattern format and register use differ.

The replay's negative control changes the worker's row count from 16 to 15.
